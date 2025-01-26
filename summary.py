from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("API key not found. Please set OPENAI_API_KEY in your .env file.")

client = OpenAI(api_key=api_key)

def summarize_text(text):
    """Summarizes long text with a structured, professional tone."""
    try:
        prompt = (
            "You are a professional assistant tasked with summarizing meeting notes or reports. The summary must be structured, concise, factual, and positive in tone."
            " Organize the output in the following format:\n"
            "1. Meeting Highlights:\n   - [List of key discussion points]\n"
            "2. Key Takeaways:\n   - [List of important conclusions]\n"
            "3. Action Items:\n   - Action 1: 'Description of the action' [Owner, Due Date]\n"
            "   - Action 2: 'Description of the action' [Owner, Due Date]\n"
            "4. Due Dates and Owners:\n   - Owner 1: Due Date\n   - Owner 2: Due Date\n"
            "5. Next Steps:\n   - [Succinct description of next steps]\n"
            "Ensure the output is professional and grounded."
            f" Here is the input text: {text}"
        )

        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "developer", "content": "You are a structured summarization assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        summary = completion.choices[0].message.content
        return summary.strip()
    except Exception as e:
        return f"Error during summarization: {e}"

# Streamlit app setup
st.title("Professional Text Summarization Tool")
st.write("This tool summarizes long texts like meeting notes or reports into a structured, professional format.")

# File upload functionality
uploaded_file = st.file_uploader("Upload a text file for summarization:", type=["txt"])

file_content = ""
if uploaded_file is not None:
    file_content = uploaded_file.read().decode("utf-8")
    st.write("### Uploaded File Content:")
    st.write(file_content)

# Input text
user_input = st.text_area("Or enter the text to summarize:", value=file_content, height=300)

# Summarize button
if st.button("Summarize"):
    if user_input.strip():
        with st.spinner("Summarizing..."):
            summary = summarize_text(user_input)
        if "Error" in summary:
            st.error(summary)
        else:
            st.success("Summarization Complete!")
            st.write("### Structured Summary:")
            st.write(summary)
    else:
        st.warning("Please enter text to summarize or upload a file.")

# Footer
st.write("---")
st.caption("Powered by OpenAI and Streamlit.")
