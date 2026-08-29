# streamlit run 04_Gemma_simple_UI.py
import streamlit as st
from litellm import completion
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.title("Gemma 3 Chat via LiteLLM")
prompt = st.text_area(label="Write your prompt.")
button = st.button("Okay")

if button:
    if prompt:
        response = completion(
            model="ollama/gemma3:4b",
            messages=[{"role": "user", "content": prompt}]
        )
        st.markdown(response['choices'][0]['message']['content'])
