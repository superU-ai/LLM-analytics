from langfuse.client import LangfuseClient
import httpx
import uuid
import datetime

class SuperuAnalysisService:

    def __init__(self, public_key: str, secret_key: str, host: str, version: str = "latest", timeout: int = 10):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = host
        self.version = version
        self.timeout = timeout
        self.session = httpx.Client(timeout=10)
        self.langfuse_client = LangfuseClient(
                                public_key=self.public_key,
                                secret_key=self.secret_key,
                                base_url=self.host,
                                version=self.version,
                                timeout=self.timeout,
                                session=self.session
                    )
        self.model_type_map = { "openai": self.format_openai_data,
                                "llama_index": self.format_llama_index_data}

    
    def post_data(self, data):

        data = self.model_type_map[data["type"]](data)
        response = self.langfuse_client.post(**data)
        if response.status_code == 200:
            return response
        return response

    def format_openai_data(self, data):

        # trace_id = 
        trace_id = str(uuid.uuid4())
        generation_id = str(uuid.uuid4())

        output_data = data.get("output_data")
        output_message = {
            "content" : output_data.choices[0].message.content,
            "role": output_data.choices[0].message.role
        }
        model_usage_data = output_data.usage
        model_usage = {
            "input": model_usage_data.prompt_tokens,
            "output": model_usage_data.completion_tokens,
            "total": model_usage_data.total_tokens
        }
        input_messages = data.get("input_data")
        model_name = output_data.model
        
        data = {
            "batch":[
            {
                "id": str(uuid.uuid4()),
                "type":"trace-create",
                "body":{
                    "id":trace_id,
                    "timestamp":datetime.datetime.now(),
                    "name":f"openai_trace",
                    "input": input_messages[1],
                    "output": output_message["content"],
                    "metadata": data.get("metadata", None)
                },
                "timestamp":datetime.datetime.now()
            },
            {
                "id":str(uuid.uuid4()),
                "type":"generation-create",
                "body":{
                    "traceId":trace_id,
                    "name":f"openai_converation",
                    "startTime":datetime.datetime.now(),
                    "input":input_messages,
                    "id":generation_id,
                    "model":model_name,
                    "modelParameters":{
                        "temperature":1,
                        "max_tokens":"inf",
                        "top_p":1,
                        "frequency_penalty":0,
                        "presence_penalty":0
                    }
                },
                "timestamp":datetime.datetime.now()
            },
            {
                
                "id":str(uuid.uuid4()),
                "type":"generation-update",
                "body":{
                    "output": output_message,
                    "id": generation_id,
                    "endTime": datetime.datetime.now(),
                    "model": model_name,
                    "usage": model_usage
                },
                "timestamp":datetime.datetime.now()
            }
            ],
            "metadata":{
            "batch_size":3,
            "sdk_integration":"openai",
            "sdk_name":"python",
            "sdk_version":"2.20.0",
            "public_key":self.public_key
            }
        }

        return data
    
    def format_llama_index_data(data):
        pass