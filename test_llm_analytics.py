from superu_llm import llm_analytics


# your superu analytics credentials
llm_analytics_client = llm_analytics(public_key="pk-lf-.....", 
                                        secret_key="sk-lf-....")

# Test Example for monitoring openai calls
import openai

# your openai credentials
openai.api_key = "xyz"     

# try:
messages = [
      {"role": "system", "content": "You are a very accurate calculator. You output only the result of the calculation."},
      {"role": "user", "content": "1 + 2 = "}]

openai_response = openai.chat.completions.create(
model="gpt-3.5-turbo",
messages=messages,
)

# data to be sent in the following format
data = {
    "input_messages": messages,                                         # Required - Input Messages 
    "output_messages": openai_response.choices[0].message.content,      # Required - the output from the model
    "metadata": {"user": "test-user", "context": "openai testing"},     # Optional - to give some metadata to the conversation
    "model": openai_response.model,                                     # Required - Name of the model
    "user_id": "",                                                      # Optional - if not given a user_id , a unique user_id will be generated
    "usage": openai_response.usage.model_dump(),                        # Optional - usage details to track the model usage and costs
    "name": ""                                                          # Optional - to name the given conversation 
}

# finally sending the data to superu analytics
llm_analytics_client.post_data(data)
