import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="German Auto-Tutor",
    page_icon="🇩🇪",
    layout="centered"
)

# --- SECURITY CHECK ---
# This looks for the API key in the cloud's secure storage
if "GEMINI_API_KEY" not in st.secrets:
    st.error("⚠️ API Key missing. Please set it in Streamlit Secrets.")
    st.stop()

# --- CONFIGURE AI ---
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# --- THE TEACHER PERSONA ---
system_prompt = """
You are a strict, efficient, and helpful German language teacher (C1+ level). 
A student has uploaded a text or handwritten image. 

Your Output Protocol:
1. **Transcribe & Correct**: 
   - If image: Transcribe the German handwriting first. 
   - Then, provide the *Corrected Version* of the text below it.
   
2. **Analysis (The "Why"):**
   - Identify the 3 biggest mistakes (grammar, spelling, or word choice).
   - Explain *why* it is wrong simply (e.g., "Dative case required after 'mit'").

3. **Improvement Tip**:
   - Give one specific thing the student should study based on these errors.

Language: Respond in English (so the explanation is clear), but keep the German text in German.
"""

# --- UI LAYOUT ---
st.title("🇩🇪 Deutsche Hausaufgaben Korrektur")
st.markdown("""
*Upload your homework. Get instant feedback. No waiting.*
""")

# Input Method Selection
tab1, tab2 = st.tabs(["📝 Type Text", "📷 Upload Photo"])

# TAB 1: TEXT INPUT
with tab1:
    text_input = st.text_area("Paste your German text here:", height=150)
    if st.button("Check Text", key="text_btn"):
        if not text_input:
            st.warning("Bitte schreiben Sie etwas! (Please write something)")
        else:
            with st.spinner("Analyzing grammar..."):
                try:
                    response = model.generate_content([system_prompt, f"Student Text: {text_input}"])
                    st.markdown("### 📝 Correction & Feedback")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# TAB 2: IMAGE INPUT
with tab2:
    uploaded_file = st.file_uploader("Upload handwriting (JPG/PNG)", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption='Your Upload', use_column_width=True)
        
        if st.button("Analyze Handwriting", key="img_btn"):
            with st.spinner("Reading handwriting & correcting..."):
                try:
                    response = model.generate_content([system_prompt, image])
                    st.markdown("### 📝 Correction & Feedback")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("System Status: Online | Focus: German Grammar & Syntax")
