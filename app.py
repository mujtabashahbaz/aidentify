import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import time

# --- CONFIGURATION ---
st.set_page_config(
    page_title="AIdentify | Dental X-Ray Diagnostics",
    page_icon="🦷",
    layout="centered"
)

# Set up the API Key (In production, use st.secrets or environment variables)
API_KEY = "" # Replace with your actual Gemini API Key
genai.configure(api_key=API_KEY)

# --- STYLING ---
st.markdown("""
    <style>
    .main {
        background-color: #0a0c10;
        color: #f1f5f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #0891b2;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stTextArea>div>div>textarea {
        background-color: #0d1117;
        color: white;
        border: 1px solid #30363d;
    }
    .report-card {
        background-color: #0d1117;
        padding: 2rem;
        border-radius: 2rem;
        border: 1px solid #30363d;
        margin-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def analyze_xray(image_bytes, notes):
    """Calls the Gemini 2.5 Flash model for analysis."""
    model = genai.GenerativeModel('gemini-2.5-flash-preview-09-2025')
    
    system_prompt = """You are a professional Dental Radiologist AI. Analyze this OPG dental X-ray. 
    Format your response in clean Markdown. Include the following sections:
    ### 🦷 Findings
    ### 📋 Diagnosis
    ### 🛠️ Suggested Treatment Plan
    
    Use bold text for emphasis. End with a disclaimer that this is an AI suggestion."""
    
    user_prompt = f"Please analyze this dental OPG image. Patient note: {notes}"
    
    # Process image for Gemini
    img = Image.open(io.BytesIO(image_bytes))
    
    response = model.generate_content([system_prompt, user_prompt, img])
    return response.text

# --- UI LAYOUT ---
st.title("🦷 AIdentify")
st.subheader("Secure AI analysis for dental radiometry")

# Upload Section
uploaded_file = st.file_uploader("Drop OPG Scan Here", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # Display Image Preview
    img_display = Image.open(uploaded_file)
    st.image(img_display, caption="Uploaded X-Ray", use_column_width=True)
    
    # Notes Section
    voice_note = st.text_area(
        "Patient Observations", 
        placeholder="Enter notes on pain, sensitivity, or medical history..."
    )
    
    # Analysis Button
    if st.button("START AI DIAGNOSIS"):
        with st.spinner("Sequencing Scan Data..."):
            try:
                # Read file as bytes
                image_bytes = uploaded_file.getvalue()
                
                # Run Analysis
                result = analyze_xray(image_bytes, voice_note)
                
                # Display Results
                st.markdown("---")
                st.success("Analysis Engine Complete")
                
                with st.container():
                    st.markdown('<div class="report-card">', unsafe_allow_html=True)
                    st.markdown(result)
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Disclaimer
                st.warning("**DENTAL DISCLAIMER:** This report is AI-generated and requires professional verification.")
                
            except Exception as e:
                st.error(f"Analysis failed: {str(e)}")

else:
    st.info("Please upload a dental X-ray image to begin.")

# --- SIDEBAR HISTORY (MOCKUP) ---
with st.sidebar:
    st.title("Records")
    st.write("Recent Scans")
    if uploaded_file:
        st.write(f"📄 Scan_{int(time.time())}.jpg")
    else:
        st.write("No records yet.")