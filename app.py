import streamlit as st
import requests

st.title("Prompt Builder")

st.header("Step 1: Define Your Prompt")
role = st.text_input("Role (e.g., 'Expert Data Scientist')", "Expert Prompt Engineer")
objective = st.text_area("Objective (What should the AI do?)", "Generate a detailed prompt for a given task.")
target_user = st.text_input("Target User (e.g., 'AI Agent', 'Student')", "AI Agent")
examples = st.text_area("Examples (Optional)", "")
constraints = st.text_area("Constraints/Requirements (Optional)", "")

st.header("Step 2: Preview Your Prompt")
prompt = f"""
Role: {role}
Objective: {objective}
Target User: {target_user}
"""
if examples:
    prompt += f"\nExamples:\n{examples}"
if constraints:
    prompt += f"\nConstraints/Requirements:\n{constraints}"

st.code(prompt, language="markdown")

st.header("Step 3: Export or Test Your Prompt")
col1, col2 = st.columns(2)
with col1:
    st.download_button("Export Prompt as .txt", prompt, file_name="prompt.txt")

with col2:
    if st.button("Test Prompt with Hugging Face Model"):
        st.info("Sending prompt to Hugging Face Inference API (distilGPT2)...")
        api_url = "https://api-inference.huggingface.co/models/distilgpt2"
        headers = {"Accept": "application/json"}
        response = requests.post(api_url, headers=headers, json={"inputs": prompt})
        if response.status_code == 200:
            result = response.json()
            generated = result[0]["generated_text"] if result and isinstance(result, list) and "generated_text" in result[0] else str(result)
            st.success("Model Output:")
            st.write(generated)
        else:
            st.error(f"Error from Hugging Face API: {response.status_code}")
