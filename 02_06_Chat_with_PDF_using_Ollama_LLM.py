import streamlit as st
from litellm import completion
from dotenv import load_dotenv
import fitz  # pip install PyMuPDF
import os

# Load environment variables
load_dotenv()

# Function to extract text from PDF
def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

st.title("Chat with PDF")
uploaded_file = st.file_uploader("Upload your PDF file", type="pdf")

if uploaded_file is not None:
    # Extract text from the uploaded PDF
    with st.spinner("Extracting text from PDF..."):
        pdf_text = extract_text_from_pdf(uploaded_file)
    
    st.success(f"PDF loaded successfully! ({len(pdf_text)} characters)")
    
    # Optional: Show preview
    with st.expander("Preview PDF content"):
        st.text(pdf_text[:1000] + "..." if len(pdf_text) > 1000 else pdf_text)

    # Input for user prompt
    prompt = st.text_area(label="Ask a question based on the PDF content.")
    button = st.button("Okay")

    if button:
        if prompt:
            # Combine the prompt with PDF content for context
            combined_prompt = f"Based on the following content: {pdf_text}\n\nQuestion: {prompt}"
            
            with st.spinner("Generating response..."):
                response = completion(
                    model="openai/gpt-5.2",
                    messages=[{"role": "user", "content": combined_prompt}]
                )
            
            st.markdown("### 📝 Answer:")
            st.markdown(response['choices'][0]['message']['content'])
