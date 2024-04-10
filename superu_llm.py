import httpx
import uuid
import datetime
from superuClient import SuperUClient
class llm_analytics:

    def __init__(self, public_key: str, secret_key: str , version: str = "latest", timeout: int = 10):
        self.public_key = public_key
        self.secret_key = secret_key
        self.host = "https://analytics.superu.ai"
        self.version = version
        self.timeout = timeout
        self.session = httpx.Client(timeout=10)
        self.langfuse_client = SuperUClient(
                                public_key=self.public_key,
                                secret_key=self.secret_key,
                                base_url=self.host,
                                version=self.version,
                                timeout=self.timeout,
                                session=self.session
                    )

    def post_data(self, data):

        data = self.format_data(data)
        response = self.langfuse_client.post(**data)
        if response.status_code == 200:
            return response
        return {"user_id": data["batch"][0]["body"]["userId"]}

    def format_data(self, data):

        trace_id = str(uuid.uuid4())
        generation_id = str(uuid.uuid4())

        output_messages = data.get("output_messages")
        output = {
            "role": "assistant",
            "content": output_messages
        }
        input_messages = data.get("input_messages")
        metadata = data.get("metadata")
        model = data.get("model")

        model_usage_data = data.get("model_usage")
        model_usage = None
        if model_usage_data:
            model_usage = {
                "input": model_usage_data.get("prompt_tokens", 0),
                "output": model_usage_data.get("completion_tokens", 0),
                "total": model_usage_data.get("total_tokens", 0)
            }

        user_id = data.get("user_id", str(uuid.uuid4()))
        name = data.get("name", "chat_session")
        formated_data = {
            "batch":[
            {
                "id": str(uuid.uuid4()),
                "type":"trace-create",
                "body":{
                    "id":trace_id,
                    "timestamp": data.get('timestamp' , datetime.datetime.now()),
                    "name": name,
                    "input": input_messages,
                    "output": output,
                    "metadata": metadata,
                    "userId": user_id,
                },
                "timestamp":data.get('timestamp' , datetime.datetime.now())
            },
            {
                "id":str(uuid.uuid4()),
                "type":"generation-create",
                "body":{
                    "traceId":trace_id,
                    "name":name,
                    "startTime": data.get('timestamp' , datetime.datetime.now()),
                    "input":input_messages,
                    "id":generation_id,
                    "model":model,
                    "modelParameters":{
                        "temperature":1,
                        "max_tokens":"inf",
                        "top_p":1,
                        "frequency_penalty":0,
                        "presence_penalty":0
                    }
                },
                "timestamp": data.get('timestamp' , datetime.datetime.now())
            },
            {
                
                "id":str(uuid.uuid4()),
                "type":"generation-update",
                "body":{
                    "output": output_messages,
                    "id": generation_id,
                    "endTime": data.get('timestamp' , datetime.datetime.now()),
                    "model": model,
                    "usage": model_usage
                },
                "timestamp":data.get('timestamp' , datetime.datetime.now())
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

        return formated_data