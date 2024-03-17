from superu_llm import SuperuAnalysisService

# replace with the host of the service in case of local deployment
# langfuse_host = "hhttp://localhost:3000"
langfuse_host = "https://analytics.superu.ai" 

service_client = SuperuAnalysisService(public_key="", 
                                        secret_key="",
                                        host=langfuse_host)

# Test Example for monitoring openai calls
import openai
openai.api_key = ""

# try:
messages = [
      {"role": "system", "content": "You are a very accurate calculator. You output only the result of the calculation."},
      {"role": "user", "content": "1 + 1 = "}]

openai_response = openai.chat.completions.create(
model="GPT-turbo-3.5",
messages=messages,
)

# data to be sent in the following format
data = {
    "input_data": messages,
    "output_data": openai_response,
    "type": "openai",  # openai or llama_index,
    "metadata": {"user": "test-user", "context": "openai testing"} # optional
}

res = service_client.post_data(data) # capturing openai call
print(res.content)