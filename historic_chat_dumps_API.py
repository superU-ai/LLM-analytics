from superu_llm import llm_analytics
from datetime import datetime
# first connect to your database


# get all chat ready for processing and adding it to analytis platform

chats = [
    {
        "input_messages": [
        {"role": "system", "content": "You are a very accurate calculator. You output only the result of the calculation."},
        {"role": "user", "content": "1 + 2 = "}
        ],
        "output_messages": "3",
        'timestamp': '09/19/23 13:55:26',
        "mobile_number": "+91 98782937642"
    }
]   # from database


# your superu analytics credentials
llm_analytics_client = llm_analytics(public_key="pk-lf-38af4424-14b0-4b88-b346-edea2b824b1c", 
                                        secret_key="sk-lf-b255ddaa-e32d-4c1d-a211-48319feda7ac")


for chat in chats:
    input_messages = chat['input_messages']
    output_messages = chat['output_messages']
    mobile_number = chat['mobile_number']
    timestamp = datetime.strptime(chat['timestamp'], '%m/%d/%y %H:%M:%S')

    datetime_str = '09/19/22 13:55:26'

    # data to be sent in the following format
    data = {
        "input_messages": input_messages,                                       # Required - Input Messages 
        "output_messages": output_messages ,                     # Required - the output from the model
        "model": "gpt-3.5-turbo",                                               # Required - Name of the model
        "user_id": mobile_number,                                           # Optional - if not given a user_id , a unique user_id will be generated
        "name": "historic test 1",                                                             # Optional - to name the given conversation 
        "timestamp": timestamp       # If historic chat then time stamp is complusory - to give the timestamp of the conversation in datetime format
    }

    # finally sending the data to superu analytics
    llm_analytics_client.post_data(data)
