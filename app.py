import streamlit as st
import google.generativeai as genai

# Load Gemini API Key
api_key = st.secrets["api_keys"]["google_api_key"]
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# UI Config
st.set_page_config(page_title="Request Analyzer")
st.title("Request Analyzer")
st.write("Paste a raw HTTP request below. The system will inspect for injection attempts, API abuse, or suspicious patterns.")

# Input field
request_data = st.text_area(
    "HTTP Request (Raw)",
    height=300,
    placeholder="POST /login HTTP/1.1\nHost: example.com\nUser-Agent: curl/7.81.0\nContent-Type: application/x-www-form-urlencoded\nContent-Length: 35\n\nusername=admin&password=' OR '1'='1"
)

if st.button("Analyze Request") and request_data.strip():
    with st.spinner("Analyzing request..."):
        prompt = f"""
You are a request pattern analyzer used in a WAF system.

Analyze the following HTTP request for:
- Potential threats (e.g., SQLi, XSS, command injection)
- API misuse
- Anomalous patterns

Respond in this format:

Verdict: <Benign | Suspicious | Malicious>  
Attack Type: <If detected>  


Request:
\"\"\"{request_data}\"\"\"
"""
        response = model.generate_content(prompt)
        result = response.text.strip()

        st.subheader("Inspection Result")
        st.text(result)
