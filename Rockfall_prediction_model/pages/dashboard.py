import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PIL import Image
import io
import base64
import os
from dotenv import load_dotenv
from pathlib import Path
from twilio.rest import Client

# Load environment variables from the .env file located in the parent directory
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

# Page config
st.set_page_config(page_title="AI Rockfall Risk Assessment System", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        padding: 2rem 1rem;
    }
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 5rem;
        font-weight: 800;
        color: transparent;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-clip: text;
        -webkit-background-clip: text;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        letter-spacing: -0.02em;
        line-height: 1.1;
        padding: 30px 20px;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(103, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 25%, rgba(240, 147, 251, 0.1) 50%, rgba(245, 87, 108, 0.1) 75%, rgba(79, 172, 254, 0.1) 100%);
        border-radius: 20px;
        z-index: -1;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .sub-header {
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 700;
        color: transparent;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #667eea 100%);
        background-clip: text;
        -webkit-background-clip: text;
        border-bottom: 3px solid;
        border-image: linear-gradient(90deg, #667eea 0%, #764ba2 100%) 1;
        padding-bottom: 1rem;
        margin: 2.5rem 0 2rem 0;
        position: relative;
        letter-spacing: -0.01em;
    }
    
    .sub-header::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        border-radius: 2px;
    }
    
    .intro-text {
        font-family: 'Inter', sans-serif;
        font-size: 1.3rem;
        font-weight: 400;
        color: #4a5568;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    .risk-critical {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 30px 0;
        box-shadow: 0 8px 32px rgba(255, 75, 43, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.01em;
    }
    
    .risk-critical::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #ff9a56 0%, #ffad56 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 30px 0;
        box-shadow: 0 8px 32px rgba(255, 173, 86, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.01em;
    }
    
    .risk-high::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        color: #2d3436;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 30px 0;
        box-shadow: 0 8px 32px rgba(253, 203, 110, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.01em;
    }
    
    .risk-moderate::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.2) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        margin: 30px 0;
        box-shadow: 0 8px 32px rgba(0, 206, 201, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.01em;
    }
    
    .risk-low::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .mining-fit {
        background: linear-gradient(135deg, #00b894 0%, #00cec9 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin: 25px 0;
        box-shadow: 0 8px 32px rgba(0, 206, 201, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.01em;
    }
    
    .mining-conditional {
        background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
        color: #2d3436;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin: 25px 0;
        box-shadow: 0 8px 32px rgba(253, 203, 110, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.01em;
    }
    
    .mining-not-fit {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        font-family: 'Inter', sans-serif;
        font-size: 2rem;
        font-weight: 700;
        margin: 25px 0;
        box-shadow: 0 8px 32px rgba(255, 75, 43, 0.4);
        position: relative;
        overflow: hidden;
        letter-spacing: -0.01em;
    }
    
    .mining-fit::before, .mining-conditional::before, .mining-not-fit::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
        animation: shimmer 3s ease-in-out infinite;
    }
    
    .parameter-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 25px;
        border: 1px solid rgba(226, 232, 240, 0.5);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        position: relative;
        overflow: hidden;
        font-family: 'Inter', sans-serif;
    }
    
    .parameter-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 2px;
    }
    
    .parameter-box h3 {
        font-family: 'Inter', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #2d3748;
        margin-bottom: 20px;
        background: linear-gradient(135deg, #4a5568 0%, #2d3748 100%);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
    }
    
    .recommendation-box {
        background: linear-gradient(135deg, #fff5f5 0%, #fed7d7 100%);
        padding: 25px;
        border-radius: 20px;
        margin: 30px 0;
        border: 1px solid rgba(254, 215, 215, 0.5);
        color: #2d3748;
        box-shadow: 0 10px 25px rgba(254, 178, 178, 0.2);
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        border-radius: 3px;
    }
    
    .recommendation-box ul {
        color: #2d3748;
        margin-top: 15px;
        margin-bottom: 15px;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    .recommendation-box li {
        margin-bottom: 8px;
        font-weight: 500;
    }
    
    .factor-box {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        border: 1px solid rgba(226, 232, 240, 0.5);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.06);
        font-family: 'Inter', sans-serif;
        position: relative;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .factor-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
    }
    
    .progress-container {
        background: linear-gradient(135deg, #e2e8f0 0%, #cbd5e0 100%);
        border-radius: 10px;
        height: 25px;
        margin: 10px 0;
        overflow: hidden;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        text-align: right;
        padding-right: 10px;
        color: white;
        font-weight: 700;
        line-height: 25px;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        transition: width 1s ease-in-out;
    }
    
    .minimal { 
        background: linear-gradient(90deg, #48bb78 0%, #38b2ac 100%);
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    .low { 
        background: linear-gradient(90deg, #4299e1 0%, #3182ce 100%);
        box-shadow: 0 4px 15px rgba(66, 153, 225, 0.3);
    }
    .moderate { 
        background: linear-gradient(90deg, #ed8936 0%, #dd6b20 100%);
        box-shadow: 0 4px 15px rgba(237, 137, 54, 0.3);
    }
    .high { 
        background: linear-gradient(90deg, #f56565 0%, #e53e3e 100%);
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3);
    }
    .extreme { 
        background: linear-gradient(90deg, #e53e3e 0%, #c53030 100%);
        box-shadow: 0 4px 15px rgba(229, 62, 62, 0.3);
    }
    
    .factor-label {
        font-weight: 700;
        margin-bottom: 8px;
        font-size: 1.2rem;
        color: #2d3748;
        font-family: 'Inter', sans-serif;
    }
    
    .factor-value {
        font-size: 1rem;
        color: #718096;
        font-weight: 500;
        font-family: 'Inter', sans-serif;
    }
    
    .stats-box {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.5);
        font-family: 'Inter', sans-serif;
        position: relative;
        overflow: hidden;
        transition: transform 0.3s ease;
    }
    
    .stats-box:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    }
    
    .stats-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
        font-family: 'Inter', sans-serif;
        margin-bottom: 5px;
    }
    
    .stats-label {
        font-size: 1rem;
        color: #718096;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1.1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        width: 100%;
        letter-spacing: 0.02em;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
    
    .graph-container {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    .image-container {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    .image-analysis {
        background: linear-gradient(135deg, #ebf8ff 0%, #bee3f8 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 20px 0;
        border: 1px solid rgba(190, 227, 248, 0.5);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.1);
        font-family: 'Inter', sans-serif;
    }
    
    .heatmap-container {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        padding: 30px;
        border-radius: 20px;
        margin: 30px 0;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    /* Enhanced form elements */
    .stSelectbox > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 10px;
        border: 1px solid rgba(226, 232, 240, 0.5);
        font-family: 'Inter', sans-serif;
    }
    
    .stSlider > div > div > div {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 10px;
        padding: 10px 20px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🏔️ AI Rockfall Risk Assessment System</p>', unsafe_allow_html=True)
st.markdown('<p class="intro-text">Advanced geological and environmental analysis for precise rockfall probability prediction</p>', unsafe_allow_html=True)

# Initialize session state for form values
if 'rainfall' not in st.session_state:
    st.session_state.rainfall = 6
if 'snowfall' not in st.session_state:
    st.session_state.snowfall = 4
if 'wind_speed' not in st.session_state:
    st.session_state.wind_speed = 0
if 'temperature' not in st.session_state:
    st.session_state.temperature = 15
if 'elevation' not in st.session_state:
    st.session_state.elevation = 1000
if 'fracture_spacing' not in st.session_state:
    st.session_state.fracture_spacing = 50
if 'fracture_orientation' not in st.session_state:
    st.session_state.fracture_orientation = 45
if 'slope_angle' not in st.session_state:
    st.session_state.slope_angle = 30
if 'rock_type' not in st.session_state:
    st.session_state.rock_type = "Limestone"
if 'uploaded_image' not in st.session_state:
    st.session_state.uploaded_image = None
if 'image_analysis' not in st.session_state:
    st.session_state.image_analysis = {}

# Function to analyze uploaded image
def analyze_image(uploaded_image):
    # This is a placeholder function that simulates image analysis
    # In a real application, you would use computer vision techniques here
    
    analysis_results = {
        "slope_steepness": np.random.randint(30, 80),
        "rock_fractures": np.random.randint(20, 90),
        "vegetation_cover": np.random.randint(10, 80),
        "rock_type_confidence": np.random.randint(60, 95),
        "erosion_signs": np.random.randint(10, 70)
    }
    
    return analysis_results

############################################
# Twilio SMS alert helpers
############################################

def _get_twilio_client():
    """Return an authenticated Twilio Client if credentials are set, else (None, error)."""
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    # Check if credentials are missing or placeholder values
    if not account_sid or not auth_token:
        return None, "Missing TWILIO_ACCOUNT_SID or TWILIO_AUTH_TOKEN environment variables"
    
    # Check if credentials are still placeholder values
    if (account_sid == "your_account_sid_here" or 
        auth_token == "your_auth_token_here"):
        return None, "Twilio credentials are placeholder values. Please update the .env file with valid credentials."
    
    # Check if Account SID has the proper format (starts with 'AC' and is 34 characters)
    if not account_sid.startswith('AC') or len(account_sid) != 34:
        return None, "Invalid TWILIO_ACCOUNT_SID format. Should start with 'AC' and be 34 characters long."
    
    try:
        return Client(account_sid, auth_token), None
    except Exception as e:
        return None, f"Failed to create Twilio client: {str(e)}"

def _get_twilio_from_number():
    """Get the Twilio sender number from env var TWILIO_FROM_NUMBER."""
    from_number = os.getenv("TWILIO_FROM_NUMBER")
    # Check if it's missing or a placeholder value
    if not from_number or from_number == "+1234567890":
        return None
    return from_number

def send_sms_alert(to_number: str, message: str):
    """Send an SMS using Twilio. Returns (ok: bool, error: Optional[str])."""
    client, err = _get_twilio_client()
    if err:
        return False, err
    from_number = _get_twilio_from_number()
    if not from_number:
        return False, "Missing TWILIO_FROM_NUMBER environment variable"
    try:
        client.messages.create(to=to_number, from_=from_number, body=message)
        return True, None
    except Exception as e:
        return False, str(e)

def build_precaution_message(risk_level: str, risk_percentage: float, feasibility_status: str) -> str:
    """Return a concise SMS message with risk, mining feasibility, and actionable precautions."""
    base = f"Rockfall Risk: {risk_level} ({risk_percentage:.0f}%). Mining: {feasibility_status}. "
    if risk_level == "CRITICAL":
        steps = (
            "Evacuate immediately; Close access; Notify authorities; Deploy monitoring."
        )
    elif risk_level == "HIGH":
        steps = (
            "Restrict access; Increase monitoring; Install warning signs; Prepare evacuation plan."
        )
    elif risk_level == "MODERATE":
        steps = (
            "Maintain monitoring; Set warnings; Inspect bi-weekly; Be vigilant after storms."
        )
    else:  # LOW
        steps = (
            "Continue standard monitoring; Maintain safety protocols; Review plans quarterly."
        )
    return base + "Precautions: " + steps

############################################
# Alerts configuration (Sidebar)
############################################
st.sidebar.markdown("## 📱 SMS Alerts")
enable_sms = st.sidebar.checkbox("Enable SMS alerts", value=False)
default_to = os.getenv("ALERT_TO_NUMBER", "")
alert_to_number = st.sidebar.text_input("Recipient phone (E.164, e.g., +15551234567)", value=default_to)

# Persist in session state
st.session_state["enable_sms"] = enable_sms
st.session_state["alert_to_number"] = alert_to_number

if enable_sms:
    # Provide quick diagnostics on credentials
    client, cred_err = _get_twilio_client()
    from_num = _get_twilio_from_number()
    
    # Debug information
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    
    st.sidebar.markdown("**Debug Info:**")
    st.sidebar.text(f"SID loaded: {'Yes' if account_sid else 'No'}")
    st.sidebar.text(f"Token loaded: {'Yes' if auth_token else 'No'}")
    st.sidebar.text(f"From number: {'Yes' if from_num else 'No'}")
    if cred_err:
        st.sidebar.text(f"Error: {cred_err}")
    
    if cred_err or not from_num:
        st.sidebar.error("📱 **Twilio SMS Configuration Issue**")
        if cred_err:
            st.sidebar.text(f"Error details: {cred_err}")
        if not from_num:
            st.sidebar.text("From number not configured")
        
        st.sidebar.markdown("""
        **To fix SMS alerts:**
        1. Check your Twilio credentials
        2. Verify the `.env` file has valid values
        3. Restart the Streamlit app
        
        **The app works perfectly without SMS alerts!**
        """)
    else:
        st.sidebar.success(f"📱 SMS alerts ready!")
        st.sidebar.info(f"From: {from_num} → To: {alert_to_number or 'Not set'}")

# Function to calculate risk
def calculate_risk(rainfall, snowfall, wind_speed, temperature, elevation, 
                   fracture_spacing, fracture_orientation, slope_angle, rock_type, image_analysis):
    
    # Adjust parameters based on image analysis if available
    image_modifier = 1.0
    if image_analysis:
        # Use image analysis to adjust parameters
        image_modifier = 1.0 + (image_analysis.get("slope_steepness", 50) / 100 - 0.5) * 0.3
        fracture_spacing = fracture_spacing * (1.0 - image_analysis.get("rock_fractures", 50) / 200)
        slope_angle = slope_angle * (1.0 + image_analysis.get("slope_steepness", 50) / 100)
    
    # Calculate individual factor contributions (0-100 scale)
    rainfall_contrib = min(rainfall / 50 * 100, 100)  # 50mm rainfall = 100%
    snowfall_contrib = min(snowfall / 30 * 100, 100)  # 30cm snowfall = 100%
    wind_contrib = min(wind_speed / 80 * 100, 100)    # 80km/h wind = 100%
    
    # Temperature: lower temps increase risk (freeze-thaw cycles)
    if temperature <= 0:
        temp_contrib = 100  # Freezing temperatures = maximum risk
    else:
        temp_contrib = max(0, 100 - (temperature * 2))  # Higher temps decrease risk
    
    elevation_contrib = min(elevation / 2000 * 100, 100)  # 2000m elevation = 100%
    
    # Fracture density: closer spacing = higher density = higher risk
    fracture_density = 100 / fracture_spacing if fracture_spacing > 0 else 100
    fracture_contrib = min(fracture_density * 2, 100)  # Scale appropriately
    
    slope_contrib = min(slope_angle / 60 * 100, 100)  # 60° slope = 100%
    
    # Rock type factor (more susceptible rocks have higher risk)
    rock_factors = {
        "Limestone": 80,
        "Sandstone": 60,
        "Shale": 70,
        "Granite": 30,
        "Basalt": 40
    }
    rock_contrib = rock_factors.get(rock_type, 50)
    
    # Apply image analysis modifier
    if image_analysis:
        fracture_contrib *= image_modifier
        slope_contrib *= image_modifier
        rock_contrib *= (1.0 + (image_analysis.get("rock_type_confidence", 50) / 100 - 0.5) * 0.2)
    
    # Calculate individual contributions for display (as percentages)
    contributions = {
        "Rainfall Impact": rainfall_contrib,
        "Snow/Ice Impact": snowfall_contrib,
        "Fracture Density": fracture_contrib,
        "Slope Geometry": slope_contrib,
        "Elevation Effects": elevation_contrib,
        "Wind Erosion": wind_contrib,
        "Temperature Effects": temp_contrib
    }
    
    # Add image analysis factors if available
    if image_analysis:
        contributions["Image Analysis: Slope"] = image_analysis.get("slope_steepness", 0)
        contributions["Image Analysis: Fractures"] = image_analysis.get("rock_fractures", 0)
    
    # Calculate weighted risk score (0-100)
    weights = {
        'rainfall': 0.12,
        'snowfall': 0.08,
        'wind_speed': 0.05,
        'temperature': 0.08,
        'elevation': 0.08,
        'fracture_density': 0.22,
        'slope_angle': 0.18,
        'rock_type': 0.05,
        'image_analysis': 0.14 if image_analysis else 0
    }
    
    weighted_risk = (
        rainfall_contrib * weights['rainfall'] +
        snowfall_contrib * weights['snowfall'] +
        wind_contrib * weights['wind_speed'] +
        temp_contrib * weights['temperature'] +
        elevation_contrib * weights['elevation'] +
        fracture_contrib * weights['fracture_density'] +
        slope_contrib * weights['slope_angle'] +
        rock_contrib * weights['rock_type']
    )
    
    # Add image analysis contribution if available
    if image_analysis:
        image_risk = (
            image_analysis.get("slope_steepness", 0) * 0.6 +
            image_analysis.get("rock_fractures", 0) * 0.4
        ) * weights['image_analysis']
        weighted_risk += image_risk
    
    # Ensure risk is within bounds
    weighted_risk = min(max(weighted_risk, 0), 100)
    
    # Determine risk level
    if weighted_risk >= 75:
        risk_level = "CRITICAL"
        confidence = 85 + (len(image_analysis) * 2 if image_analysis else 0)
    elif weighted_risk >= 50:
        risk_level = "HIGH"
        confidence = 80 + (len(image_analysis) * 2 if image_analysis else 0)
    elif weighted_risk >= 25:
        risk_level = "MODERATE"
        confidence = 75 + (len(image_analysis) * 2 if image_analysis else 0)
    else:
        risk_level = "LOW"
        confidence = 70 + (len(image_analysis) * 2 if image_analysis else 0)
    
    return weighted_risk, risk_level, confidence, contributions

# Function to determine mining feasibility
def determine_mining_feasibility(risk_level, risk_percentage, confidence):
    """
    Determine mining feasibility based on risk level, percentage, and confidence.
    Returns: (feasibility_status, recommendation_message, css_class)
    """
    if risk_level == "LOW":
        return "FIT", "✅ Low risk environment - Suitable for mining operations with standard safety protocols", "mining-fit"
    elif risk_level == "MODERATE":
        if confidence >= 70:
            return "FIT", "✅ Moderate risk with high confidence - Mining approved with enhanced monitoring", "mining-fit"
        else:
            return "CONDITIONALLY FIT", "⚠️ Moderate risk with lower confidence - Additional geological assessment required before mining", "mining-conditional"
    elif risk_level == "HIGH":
        return "NOT FIT", "❌ High risk environment - Mining operations not recommended without major risk mitigation", "mining-not-fit"
    else:  # CRITICAL
        return "NOT FIT", "🚨 Critical risk environment - Mining operations strictly prohibited until risk is mitigated", "mining-not-fit"

# Function to get risk category
def get_risk_category(value):
    if value < 20:
        return "MINIMAL", "minimal"
    elif value < 40:
        return "LOW", "low"
    elif value < 60:
        return "MODERATE", "moderate"
    elif value < 80:
        return "HIGH", "high"
    else:
        return "EXTREME", "extreme"

# Function to create heat maps
def create_heat_maps(risk_percentage, contributions, rainfall, snowfall, wind_speed, temperature, 
                    elevation, fracture_spacing, slope_angle):
    
    # Create parameter sensitivity heatmap
    parameters = ['Rainfall', 'Snowfall', 'Wind Speed', 'Temperature', 'Elevation', 
                  'Fracture Spacing', 'Slope Angle']
    
    # Generate sensitivity matrix (how risk changes with parameter variations)
    sensitivity_matrix = []
    base_params = [rainfall, snowfall, wind_speed, temperature, elevation, fracture_spacing, slope_angle]
    
    for i, param in enumerate(parameters):
        sensitivity_row = []
        for j, variation in enumerate(np.linspace(0.5, 1.5, 10)):  # Vary from 50% to 150% of original
            modified_params = base_params.copy()
            modified_params[i] = modified_params[i] * variation
            
            # Calculate risk with modified parameter
            modified_risk, _, _, _ = calculate_risk(
                modified_params[0], modified_params[1], modified_params[2], 
                modified_params[3], modified_params[4], modified_params[5], 
                45, modified_params[6], "Limestone", {}
            )
            sensitivity_row.append(modified_risk)
        sensitivity_matrix.append(sensitivity_row)
    
    # Create parameter sensitivity heatmap
    fig_sensitivity = go.Figure(data=go.Heatmap(
        z=sensitivity_matrix,
        x=[f"{v:.1f}x" for v in np.linspace(0.5, 1.5, 10)],
        y=parameters,
        colorscale='RdYlBu_r',
        colorbar=dict(title="Risk Level (%)")
    ))
    
    fig_sensitivity.update_layout(
        title="Parameter Sensitivity Heat Map",
        xaxis_title="Parameter Variation Factor",
        yaxis_title="Parameters",
        height=500
    )
    
    # Create risk correlation heatmap
    correlation_data = []
    correlation_labels = list(contributions.keys())
    contribution_values = list(contributions.values())
    
    # Calculate correlation matrix
    for i, val1 in enumerate(contribution_values):
        row = []
        for j, val2 in enumerate(contribution_values):
            # Simulate correlation based on contribution similarity
            correlation = 1.0 - abs(val1 - val2) / 100
            row.append(correlation)
        correlation_data.append(row)
    
    fig_correlation = go.Figure(data=go.Heatmap(
        z=correlation_data,
        x=correlation_labels,
        y=correlation_labels,
        colorscale='RdBu',
        colorbar=dict(title="Correlation Coefficient"),
        zmin=-1,
        zmax=1
    ))
    
    fig_correlation.update_layout(
        title="Risk Factor Correlation Heat Map",
        height=600,
        xaxis_tickangle=45
    )
    
    # Create geographical risk distribution heatmap (simulated)
    # This simulates risk across different geographical zones
    zones = ['North Zone', 'South Zone', 'East Zone', 'West Zone', 'Central Zone']
    conditions = ['Wet Season', 'Dry Season', 'Winter', 'Spring', 'Summer', 'Autumn']
    
    # Generate simulated geographical risk data
    geo_risk_matrix = []
    for zone in zones:
        zone_risks = []
        for condition in conditions:
            # Simulate risk based on current risk and random variations
            base_risk = risk_percentage
            variation = np.random.normal(0, 15)  # Random variation
            zone_risk = max(0, min(100, base_risk + variation))
            zone_risks.append(zone_risk)
        geo_risk_matrix.append(zone_risks)
    
    fig_geo = go.Figure(data=go.Heatmap(
        z=geo_risk_matrix,
        x=conditions,
        y=zones,
        colorscale='RdYlGn_r',
        colorbar=dict(title="Risk Level (%)")
    ))
    
    fig_geo.update_layout(
        title="Geographical Risk Distribution Heat Map",
        xaxis_title="Seasonal Conditions",
        yaxis_title="Geographical Zones",
        height=400
    )
    
    # Create time-based risk heatmap (24-hour and seasonal patterns)
    hours = [f"{h:02d}:00" for h in range(24)]
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # Generate time-based risk matrix
    time_risk_matrix = []
    for month_idx, month in enumerate(months):
        month_risks = []
        for hour_idx, hour in enumerate(hours):
            # Simulate risk patterns: higher in early morning and during wet months
            seasonal_factor = 1.2 if month_idx in [0, 1, 10, 11] else 0.8  # Winter months higher
            daily_factor = 1.1 if hour_idx in range(4, 8) else 0.9  # Early morning higher
            
            time_risk = risk_percentage * seasonal_factor * daily_factor
            time_risk = max(0, min(100, time_risk + np.random.normal(0, 5)))
            month_risks.append(time_risk)
        time_risk_matrix.append(month_risks)
    
    fig_time = go.Figure(data=go.Heatmap(
        z=time_risk_matrix,
        x=hours,
        y=months,
        colorscale='Viridis',
        colorbar=dict(title="Risk Level (%)")
    ))
    
    fig_time.update_layout(
        title="Temporal Risk Pattern Heat Map (24h × Seasonal)",
        xaxis_title="Hour of Day",
        yaxis_title="Month",
        height=500
    )
    
    return fig_sensitivity, fig_correlation, fig_geo, fig_time

# Function to create analysis graph
def create_analysis_graph(contributions, risk_percentage):
    # Prepare data for the radar chart
    factors = list(contributions.keys())
    values = list(contributions.values())
    
    # Create radar chart
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values + [values[0]],  # Close the circle
        theta=factors + [factors[0]],  # Close the circle
        fill='toself',
        name='Risk Factors',
        line=dict(color='#667eea'),
        fillcolor='rgba(102, 126, 234, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False,
        title="Risk Factor Analysis",
        height=400
    )
    
    # Create bar chart for factor contributions
    fig2 = go.Figure()
    
    # Sort factors by contribution
    sorted_factors = sorted(contributions.items(), key=lambda x: x[1], reverse=True)
    factors_sorted = [x[0] for x in sorted_factors]
    values_sorted = [x[1] for x in sorted_factors]
    
    # Color mapping based on values
    colors = []
    for val in values_sorted:
        if val < 20:
            colors.append('#48bb78')
        elif val < 40:
            colors.append('#4299e1')
        elif val < 60:
            colors.append('#ed8936')
        elif val < 80:
            colors.append('#f56565')
        else:
            colors.append('#e53e3e')
    
    fig2.add_trace(go.Bar(
        x=factors_sorted,
        y=values_sorted,
        marker_color=colors,
        text=values_sorted,
        texttemplate='%{text:.0f}%',
        textposition='auto',
    ))
    
    fig2.update_layout(
        title="Risk Factor Contributions",
        xaxis_title="Factors",
        yaxis_title="Contribution (%)",
        yaxis=dict(range=[0, 100]),
        height=400
    )
    
    # Create risk gauge
    fig3 = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = risk_percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Overall Risk Score"},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#667eea"},
            'steps': [
                {'range': [0, 25], 'color': '#48bb78'},
                {'range': [25, 50], 'color': '#ed8936'},
                {'range': [50, 75], 'color': '#f56565'},
                {'range': [75, 100], 'color': '#e53e3e'}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': risk_percentage}
        }
    ))
    
    fig3.update_layout(height=300)
    
    return fig, fig2, fig3

# Create form for input parameters
with st.form("risk_assessment_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<p class="sub-header">🌦️ Environmental & Geological Parameters</p>', unsafe_allow_html=True)
        
        st.markdown('<div class="parameter-box">', unsafe_allow_html=True)
        st.markdown("### ☔ Weather Conditions")
        rainfall = st.slider("Rainfall (mm/24h)", 0, 100, st.session_state.rainfall)
        snowfall = st.slider("Snowfall (cm/24h)", 0, 50, st.session_state.snowfall)
        wind_speed = st.slider("Wind Speed (km/h)", 0, 100, st.session_state.wind_speed)
        temperature = st.slider("Temperature (°C)", -20, 40, st.session_state.temperature)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="parameter-box">', unsafe_allow_html=True)
        st.markdown("### 🗻 Geological Conditions")
        elevation = st.slider("Elevation (m)", 0, 3000, st.session_state.elevation)
        fracture_spacing = st.slider("Fracture Spacing (cm)", 1, 200, st.session_state.fracture_spacing)
        fracture_orientation = st.slider("Fracture Orientation (°)", 0, 90, st.session_state.fracture_orientation)
        slope_angle = st.slider("Slope Angle (°)", 0, 90, st.session_state.slope_angle)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="parameter-box">', unsafe_allow_html=True)
        st.markdown("### 🪨 Rock Type Selection")
        rock_type = st.selectbox(
            "Choose the predominant rock type:",
            ["Limestone", "Sandstone", "Shale", "Granite", "Basalt"],
            index=["Limestone", "Sandstone", "Shale", "Granite", "Basalt"].index(st.session_state.rock_type)
        )
        
        # Display selected rock type information - this will update dynamically
        rock_info = {
            "Limestone": "Sedimentary rock - High weathering susceptibility",
            "Sandstone": "Sedimentary rock - Moderate weathering resistance", 
            "Shale": "Sedimentary rock - High erosion potential",
            "Granite": "Igneous rock - High structural integrity",
            "Basalt": "Volcanic rock - Good structural stability"
        }
        
        # Dynamic rock type display that updates with selection
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #e6f3ff 0%, #cce7ff 100%);
            padding: 15px 20px;
            border-radius: 10px;
            margin-top: 10px;
            border-left: 4px solid #667eea;
            box-shadow: 0 2px 8px rgba(102, 126, 234, 0.1);
        ">
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 1.1rem;
                font-weight: 600;
                color: #2d3748;
                margin-bottom: 5px;
            ">
                🪨 Selected: {rock_type}
            </div>
            <div style="
                font-family: 'Inter', sans-serif;
                font-size: 1rem;
                color: #4a5568;
                line-height: 1.4;
            ">
                {rock_info[rock_type]}
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="parameter-box">', unsafe_allow_html=True)
        st.markdown("### 📸 Upload Slope Image (Optional)")
        uploaded_file = st.file_uploader("Upload an image of the slope for analysis", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            # Store the uploaded image
            st.session_state.uploaded_image = uploaded_file
            # Analyze the image
            st.session_state.image_analysis = analyze_image(uploaded_file)
            
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="📷 Uploaded Slope Image", use_column_width=True)
            
            # Display image analysis results
            st.markdown("#### 🔍 Image Analysis Results")
            st.markdown('<div class="image-analysis">', unsafe_allow_html=True)
            for factor, value in st.session_state.image_analysis.items():
                st.write(f"**{factor.replace('_', ' ').title()}**: {value}%")
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.session_state.uploaded_image = None
            st.session_state.image_analysis = {}
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Calculate button
        calculate_btn = st.form_submit_button("🔍 Calculate Risk")


# Calculate risk when button is clicked
if calculate_btn:
    risk_percentage, risk_level, confidence, contributions = calculate_risk(
        rainfall, snowfall, wind_speed, temperature, elevation, 
        fracture_spacing, fracture_orientation, slope_angle, rock_type,
        st.session_state.image_analysis
    )
    
    # Store values in session state
    st.session_state.rainfall = rainfall
    st.session_state.snowfall = snowfall
    st.session_state.wind_speed = wind_speed
    st.session_state.temperature = temperature
    st.session_state.elevation = elevation
    st.session_state.fracture_spacing = fracture_spacing
    st.session_state.fracture_orientation = fracture_orientation
    st.session_state.slope_angle = slope_angle
    st.session_state.rock_type = rock_type
    
    # Display results
    st.markdown("---")
    st.markdown('<p class="sub-header">📊 Risk Assessment Results</p>', unsafe_allow_html=True)
    
    # Display uploaded image if available
    if st.session_state.uploaded_image is not None:
        st.markdown("### 📷 Analyzed Slope Image")
        st.markdown('<div class="image-container">', unsafe_allow_html=True)
        image = Image.open(st.session_state.uploaded_image)
        st.image(image, caption="🔍 Computer Vision Analysis Complete", use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Display risk level with appropriate styling
    if risk_level == "CRITICAL":
        st.markdown(f'<div class="risk-critical">🚨 {risk_percentage:.0f}% {risk_level} RISK<br><small style="font-size: 1.2rem; opacity: 0.9;">Confidence Level: {confidence}%</small></div>', unsafe_allow_html=True)
    elif risk_level == "HIGH":
        st.markdown(f'<div class="risk-high">⚠️ {risk_percentage:.0f}% {risk_level} RISK<br><small style="font-size: 1.2rem; opacity: 0.9;">Confidence Level: {confidence}%</small></div>', unsafe_allow_html=True)
    elif risk_level == "MODERATE":
        st.markdown(f'<div class="risk-moderate">⚡ {risk_percentage:.0f}% {risk_level} RISK<br><small style="font-size: 1.2rem; opacity: 0.9;">Confidence Level: {confidence}%</small></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="risk-low">✅ {risk_percentage:.0f}% {risk_level} RISK<br><small style="font-size: 1.2rem; opacity: 0.9;">Confidence Level: {confidence}%</small></div>', unsafe_allow_html=True)
    
    # Mining Feasibility Analysis
    st.markdown("---")
    st.markdown('<p class="sub-header">⛏️ Mining Feasibility Assessment</p>', unsafe_allow_html=True)
    
    # Determine mining feasibility
    feasibility_status, recommendation_message, feasibility_css = determine_mining_feasibility(risk_level, risk_percentage, confidence)
    
    # Display mining feasibility result
    st.markdown(f'<div class="{feasibility_css}">⛏️ MINING STATUS: {feasibility_status}<br><small style="font-size: 1.2rem; opacity: 0.9;">Risk: {risk_percentage:.0f}% | Confidence: {confidence}%</small></div>', unsafe_allow_html=True)
    
    # Display recommendation message
    st.markdown(f"""
    <div class="recommendation-box" style="margin-top: 20px;">
        <h3 style="margin-top: 0;">💡 Mining Feasibility Recommendation</h3>
        <p style="font-size: 1.2rem; font-weight: 600; line-height: 1.6;">{recommendation_message}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk level indicator
    risk_labels = ["Low", "Moderate", "High", "Critical"]
    risk_colors = ["#48bb78", "#ed8936", "#f56565", "#e53e3e"]
    risk_emojis = ["✅", "⚡", "⚠️", "🚨"]
    
    risk_cols = st.columns(4)
    for i, (label, color, emoji) in enumerate(zip(risk_labels, risk_colors, risk_emojis)):
        with risk_cols[i]:
            if label.upper() == risk_level:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: {color}; font-size: 1.2rem;'>{emoji} {label}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; opacity: 0.5; font-size: 1.1rem;'>{emoji} {label}</div>", unsafe_allow_html=True)
    
    # Create analysis graphs
    radar_fig, bar_fig, gauge_fig = create_analysis_graph(contributions, risk_percentage)
    
    # Display graphs
    st.markdown("---")
    st.markdown('<p class="sub-header">📈 Risk Analysis Visualization</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        st.plotly_chart(radar_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="graph-container">', unsafe_allow_html=True)
        st.plotly_chart(bar_fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.plotly_chart(gauge_fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Create and display heat maps
    st.markdown("---")
    st.markdown('<p class="sub-header">🗺️ Risk Heat Map Analysis</p>', unsafe_allow_html=True)
    st.markdown('<div class="heatmap-container">', unsafe_allow_html=True)
    
    # Generate heat maps
    sensitivity_fig, correlation_fig, geo_fig, time_fig = create_heat_maps(
        risk_percentage, contributions, rainfall, snowfall, wind_speed, 
        temperature, elevation, fracture_spacing, slope_angle
    )
    
    # Display heat maps in tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎚️ Parameter Sensitivity", "🔗 Factor Correlation", "🌍 Geographical Risk", "⏰ Temporal Patterns"])
    
    with tab1:
        st.plotly_chart(sensitivity_fig, use_container_width=True)
        st.markdown("**Parameter Sensitivity Heat Map** shows how changes in each parameter affect overall risk. "
                   "Darker red areas indicate higher risk levels when parameters are increased.")
    
    with tab2:
        st.plotly_chart(correlation_fig, use_container_width=True)
        st.markdown("**Factor Correlation Heat Map** displays the relationship between different risk factors. "
                   "Red indicates positive correlation, blue indicates negative correlation.")
    
    with tab3:
        st.plotly_chart(geo_fig, use_container_width=True)
        st.markdown("**Geographical Risk Distribution** shows risk patterns across different zones and seasonal conditions. "
                   "This helps identify high-risk areas and optimal monitoring strategies.")
    
    with tab4:
        st.plotly_chart(time_fig, use_container_width=True)
        st.markdown("**Temporal Risk Patterns** displays risk variations throughout the day and across seasons. "
                   "This helps in scheduling monitoring activities and planning preventive measures.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Risk factor contributions with visual indicators
    st.markdown("---")
    st.markdown('<p class="sub-header">📋 Risk Factor Contributions</p>', unsafe_allow_html=True)
    
    # Calculate statistics
    active_factors = sum(1 for value in contributions.values() if value > 5)  # Consider factors > 5% as active
    avg_impact = sum(contributions.values()) / len(contributions)
    max_impact = max(contributions.values())
    
    # Display statistics
    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-value">📊 {max_impact:.0f}%</div>
            <div class="stats-label">Highest Factor</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-value">📈 {avg_impact:.0f}%</div>
            <div class="stats-label">Average Impact</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-value">⚡ {active_factors}/{len(contributions)}</div>
            <div class="stats-label">Active Factors</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display each factor with progress bar
    for factor, value in contributions.items():
        category, css_class = get_risk_category(value)
        
        st.markdown(f"""
        <div class="factor-box">
            <div class="factor-label">📌 {factor}</div>
            <div class="factor-value">{category} - {value:.0f}% Impact</div>
            <div class="progress-container">
                <div class="progress-bar {css_class}" style="width: {value}%">{value:.0f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommended actions
    st.markdown("---")
    st.markdown('<p class="sub-header">💡 Recommended Actions</p>', unsafe_allow_html=True)
    
    if risk_level == "CRITICAL":
        st.markdown("""
        <div class="recommendation-box">
            <h3 style="margin-top: 0;">🚨 <b>IMMEDIATE ACTION REQUIRED</b></h3>
            <p style="font-size: 1.2rem; font-weight: 600;">Immediate evacuation and area closure required. Deploy emergency monitoring systems.</p>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li>🚁 <strong>Evacuate all personnel</strong> from the risk zone immediately</li>
                <li>🚧 <strong>Close access roads</strong> and establish safety perimeters</li>
                <li>📡 <strong>Deploy real-time monitoring</strong> equipment with emergency alerts</li>
                <li>📞 <strong>Notify emergency response teams</strong> and local authorities</li>
                <li>👷 <strong>Schedule immediate geotechnical</strong> assessment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_level == "HIGH":
        st.markdown("""
        <div class="recommendation-box">
            <h3 style="margin-top: 0;">⚠️ <b>HIGH PRIORITY ACTIONS</b></h3>
            <p style="font-size: 1.2rem; font-weight: 600;">High risk of rockfall. Restrict access and increase monitoring frequency.</p>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li>🚫 <strong>Restrict access</strong> to high-risk areas</li>
                <li>👁️ <strong>Increase monitoring frequency</strong> to daily inspections</li>
                <li>⚠️ <strong>Install warning signs</strong> and barriers</li>
                <li>🛡️ <strong>Evaluate protective measures</strong> (nets, fences)</li>
                <li>📋 <strong>Develop evacuation plan</strong> for affected areas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_level == "MODERATE":
        st.markdown("""
        <div class="recommendation-box">
            <h3 style="margin-top: 0;">⚡ <b>MODERATE RISK MANAGEMENT</b></h3>
            <p style="font-size: 1.2rem; font-weight: 600;">Maintain vigilance and implement enhanced monitoring protocols.</p>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li>📊 <strong>Continue standard monitoring</strong> procedures</li>
                <li>🔔 <strong>Implement warning systems</strong> for personnel</li>
                <li>📅 <strong>Schedule bi-weekly inspections</strong></li>
                <li>🌦️ <strong>Increase vigilance</strong> after significant weather events</li>
                <li>📋 <strong>Review safety protocols</strong> regularly</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="recommendation-box">
            <h3 style="margin-top: 0;">✅ <b>STANDARD MONITORING PROTOCOL</b></h3>
            <p style="font-size: 1.2rem; font-weight: 600;">Low risk level. Maintain regular safety protocols and monitoring schedule.</p>
            <ul style="font-size: 1.1rem; line-height: 1.8;">
                <li>📈 <strong>Continue standard monitoring</strong> schedule</li>
                <li>🛡️ <strong>Maintain existing safety</strong> protocols</li>
                <li>📊 <strong>Quarterly risk assessment</strong> reviews</li>
                <li>👥 <strong>Train personnel</strong> on rockfall recognition</li>
                <li>📋 <strong>Update emergency plans</strong> annually</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Send SMS alert after every prediction when SMS is enabled
    if st.session_state.get("enable_sms"):
        to_num = st.session_state.get("alert_to_number", "").strip()
        if to_num:
            alert_message = build_precaution_message(risk_level, risk_percentage, feasibility_status)
            ok, err = send_sms_alert(to_num, alert_message)
            if ok:
                st.success(f"📱 SMS alert sent to {to_num}")
            else:
                st.error(f"❌ Failed to send SMS alert: {err}")
        else:
            st.warning("⚠️ SMS alerts enabled, but no recipient number provided.")
# ... (rest of your dashboard.py code, including all your analysis and graphs) ...

# Add the navigation button at the end
st.markdown("---")
st.markdown('<div style="text-align: center; margin-top: 3rem;">', unsafe_allow_html=True)
st.page_link("pages/contour_map.py", label="Show Contour Maps", icon="🗺️", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)