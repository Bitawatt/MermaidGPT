import openai
import streamlit as st
import os

# Configure openai api key
def set_openai_api_key():
    # Try to get the API key from the environment
    openai_api_key = os.getenv("OPENAI_API_KEY")
    print(openai_api_key)

    # If it's not found in the environment, get it from the streamlit session state
    if openai_api_key is None:
        openai_api_key = st.session_state.get("OPENAI_API_KEY")

    # Set the API key
    openai.api_key = openai_api_key

def generate_prompt(prompt, chart_type, direction):
    # Preset instruction messages for the model
    messages = [{"role": "user", "content": "You are a bot that only communicates in Mermaid.js formatted markdown."},
                {"role": "user", "content": "Do not provide any additional information or notes, ONLY markdown."}]

    # Generate prompt using OpenAI model
    prompt_formatted = f"""
    Generate markdown for mermaid.js for a chart of type {chart_type}
with the following details and only return the markdown that can be pasted into a mermaid.js viewer:
{prompt}
"""

    # Add prompt to messages
    messages.append({"role": "user", "content": prompt_formatted})

    return messages

# Generate response using OpenAI model
def SendChatRequest(prompt, chart_type, direction):

    # Assemble the prompt
    full_prompt = generate_prompt(prompt, chart_type, direction)

    # Send prompt to OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=full_prompt,
        max_tokens=1000,
        temperature=0.9,
    )
    graph = response.get('choices')[0].get('message').get('content')

    # Remove ```mermaid and ``` from the response
    graph = graph.replace('```mermaid', '')
    graph = graph.replace('```', '')

    print(graph)
    return graph