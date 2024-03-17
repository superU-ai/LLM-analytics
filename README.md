# superU LLM analytics

Welcome to superU LLM analytics Hosting! This service allows you to obtain Langfuse API keys for accessing the Langfuse API. Langfuse is an open-source project designed for natural language processing tasks.

## Getting Started

To start using the superU's Free Langfuse API Hosting service, follow these steps:

1. Visit [analytics.superu.ai](https://analytics.superu.ai).
2. Sign up for a free account or log in if you already have one.
3. Navigate to the API keys section.
4. Generate your Langfuse API keys.

## Installation

To integrate Langfuse API keys into your Python projects, follow these steps:

1. Clone the GitHub repository:

```bash
git clone https://github.com/GuptaAk07/superu-llm-analytics.git
```

2. Navigate to the directory:

```bash
cd superu-llm-analytics
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

After obtaining your Langfuse API keys, you can integrate them into your projects to access the Langfuse API. Below is an example of how to use Langfuse API keys with the Superu Analysis Service, along with an OpenAI integration:

## Iterate through this procedure for all your prompts and responses to thoroughly analyze user interactions with your LLM.

```python
from superu_llm import SuperuAnalysisService
import openai

# Initialize the service client
service_client = SuperuAnalysisService(public_key="your_public_key", secret_key="your_secret_key", host="langfuse_host")

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
