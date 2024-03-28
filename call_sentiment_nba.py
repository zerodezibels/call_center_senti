
import openai
import os
import streamlit as st



os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

openai.api_key = os.environ['OPENAI_API_KEY']

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"

from openai import OpenAI
client = OpenAI()

st.set_page_config(page_title="Call Center Sentiment and Next Best Action", page_icon=":robot:", layout = "wide")



# With magic:
#st.session_state

common_prompt = """In the below conversion between an Health Care Company Call Center Agent and Customer, extract the reason for calling and call sentiment. Provide any recommended actions that need to be taken by the customer and provide detailed next best actions for the agent to earn customer trust. Also provide a formatted summary of the conversation \
\
The conversion is enclosed in ``` and is in the style of Agent X: and Customer:. The X in Agent Name is a number.\
\
Provide the response in the following format:\
\
Reason for the Call: Provide justification in parantheses\
\

Call Sentiment: Provide justification in parantheses\
\

Customer Follow-up:\
\

Next best action for Agent:\
\

Reason should in the following categories [Inquiry, Billing, Payment, Feedback, Cancellation, New Sales, Renewal, Care ]. \
\

Call Sentiment should in the following categories [Positive, Negative, Neutral]\
\

Summary:\


"""

def get_completion(prompt, model=llm_model):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content



st.header("GenAI VoC Sentiment Demo")

#option_search_type = st.radio('Search Type',['Text', 'Image'])

if 'qry' not in st.session_state:
    st.session_state['qry'] = 'dummy'


input_text = st.text_area(label="Enter Call Transcript Here...", label_visibility='collapsed', placeholder="Paste Transcript Here...", key="transcript_input")
#format_option = st.radio('Output Format', ['Descriptive', 'Short'])
button_clicked = st.button('Get Call Feedback', type='primary')



if button_clicked:
    if input_text != st.session_state['qry']:
        st.session_state['qry'] = input_text
        call_transcript = input_text

        final_prompt =  common_prompt + call_transcript + ' . Return the response in well formatted markdown table.'

        #st.write("Actual Query submitted to ChatGPT")
        #st.write(query_append)

        with st.spinner('Fetching Response....'):
            response = get_completion(final_prompt)
            st.session_state['response'] = response

        st.success('Here is the feedback:')

        st.markdown(response)

    else:
        st.write("No New Transcript Submitted. Displaying Last Result")
        st.markdown(st.session_state['response'])
