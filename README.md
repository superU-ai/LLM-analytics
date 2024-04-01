# superU LLM analytics

Welcome to superU LLM analytics Hosting! This service allows you to track metrics (cost, latency, quality) and gain insights about your users.
## Getting Started

To start using the superU's Free Analytics API service, follow these steps:

1. Visit [analytics.superu.ai](https://analytics.superu.ai).
2. Sign up for a free account or log in if you already have one.
3. Create a new Project.
4. Navigate to the Settings > API keys section.
5. Generate your superU API keys.

## Installation

To integrate superU's Analytics with your Python projects, follow these steps:

1. Clone the GitHub repository:

```bash
git clone https://github.com/superU-ai/LLM-analytics.git
```

2. Navigate to the directory:

```bash
cd superu-llm-analytics
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

After obtaining your superU API keys, you can integrate them into your projects to access the API. Below is an example of how to use the API keys with the Superu Analysis Service, along with an OpenAI integration:

## Iterate through this procedure for all your prompts and responses to thoroughly analyze user interactions with your LLM.

```python
from superu_llm import SuperuAnalysisService
import openai

# Initialize the service client
superU_host = "https://analytics.superu.ai" 

service_client = SuperuAnalysisService(public_key="", secret_key="",host=superU_host)

# Set up OpenAI API key
openai.api_key = "your_openai_api_key"

# Define messages for OpenAI chat completion
input_messages = [
    {"role": "system", "content": "You are a very accurate calculator. You output only the result of the calculation."},
    {"role": "user", "content": "1 + 1 = "}
]

# Request chat completion from OpenAI
openai_response = openai.chat.completions.create(
    # change model as per requirments
    model="GPT-turbo-3.5",
    messages=input_messages,
)

# Prepare data to be sent to Superu Analysis Service
data = {
    "input_data": input_messages,
    "output_data": openai_response,
    "type": "openai",  # Specify the type of model (openai or llama_index)
    "metadata": {"user": "test-user", "context": "openai testing"}  # Optional metadata
}

# Post data to the analysis service
res = service_client.post_data(data)
print(res.content)
```
