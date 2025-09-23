import streamlit as st

st.set_page_config(page_title="AI Rockfall Prediction System", layout="centered")

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    /* Global background and layout with enhanced gradient */
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #1e3a8a 100%);
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
        margin: 0;
        padding: 0;
    }
    
    /* Animated background particles */
    body::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 25% 25%, rgba(59, 130, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 75% 25%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 25% 75%, rgba(236, 72, 153, 0.15) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(245, 158, 11, 0.15) 0%, transparent 50%);
        animation: particleMove 20s ease-in-out infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes particleMove {
        0%, 100% { opacity: 0.3; transform: scale(1); }
        50% { opacity: 0.6; transform: scale(1.1); }
    }
    
    /* Hide streamlit elements */
    .stApp > header {
        background-color: transparent;
        display: none;
    }
    
    .stApp {
        background: transparent;
    }
    
    [data-testid="stToolbar"] {
        display: none;
    }
    
    [data-testid="stHeader"] {
        display: none;
    }
    
    [data-testid="stDecoration"] {
        display: none;
    }
    
    /* Main container with reduced top spacing */
    .main-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 100vh;
        padding: 1rem 2rem;
        text-align: center;
        position: relative;
        margin-top: -10vh;
    }
    
    /* Enhanced card styling with glassmorphism */
    .welcome-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 32px;
        padding: 4rem 3rem;
        box-shadow: 
            0 25px 50px rgba(0, 0, 0, 0.4),
            0 0 0 1px rgba(255, 255, 255, 0.05),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
        max-width: 900px;
        width: 100%;
        position: relative;
        transition: all 0.4s ease;
        overflow: hidden;
    }
    
    .welcome-card:hover {
        transform: translateY(-5px) scale(1.01);
        box-shadow: 
            0 35px 70px rgba(0, 0, 0, 0.5),
            0 0 0 1px rgba(255, 255, 255, 0.08),
            inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* Enhanced glow effect with multiple layers */
    .welcome-card::before {
        content: '';
        position: absolute;
        top: -3px;
        left: -3px;
        right: -3px;
        bottom: -3px;
        background: linear-gradient(45deg, 
            #3b82f6 0%, 
            #8b5cf6 25%, 
            #ec4899 50%, 
            #f59e0b 75%, 
            #3b82f6 100%);
        border-radius: 35px;
        z-index: -1;
        opacity: 0.4;
        filter: blur(15px);
        animation: borderGlow 4s ease-in-out infinite;
        background-size: 200% 200%;
    }
    
    @keyframes borderGlow {
        0%, 100% { background-position: 0% 50%; opacity: 0.3; }
        50% { background-position: 100% 50%; opacity: 0.6; }
    }
    
    /* Enhanced typography with text effects */
    .welcome-title {
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 50%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 1.5rem 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
        text-shadow: 0 0 30px rgba(255, 255, 255, 0.5);
        animation: titleGlow 3s ease-in-out infinite;
        position: relative;
        text-align: center;
    }
    
    @keyframes titleGlow {
        0%, 100% { text-shadow: 0 0 30px rgba(255, 255, 255, 0.3); }
        50% { text-shadow: 0 0 50px rgba(255, 255, 255, 0.6); }
    }
    
    .subtitle {
        font-size: 2.2rem;
        font-weight: 500;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(255, 255, 255, 0.7) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0 0 3rem 0;
        line-height: 1.3;
        letter-spacing: 0.01em;
    }
    
    /* Enhanced image styling with 3D effects */
    img {
        margin: 2rem 0 1rem 0 !important;
        filter: 
            drop-shadow(0 0 25px rgba(255, 255, 255, 0.4))
            drop-shadow(0 10px 20px rgba(0, 0, 0, 0.3));
        animation: float3D 4s ease-in-out infinite;
        transition: all 0.3s ease;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.05);
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    @keyframes float3D {
        0%, 100% { 
            transform: translateY(0px) rotateY(0deg); 
            filter: drop-shadow(0 0 25px rgba(255, 255, 255, 0.4)) drop-shadow(0 10px 20px rgba(0, 0, 0, 0.3));
        }
        50% { 
            transform: translateY(-15px) rotateY(5deg); 
            filter: drop-shadow(0 0 35px rgba(255, 255, 255, 0.6)) drop-shadow(0 15px 30px rgba(0, 0, 0, 0.4));
        }
    }
    
    img:hover {
        transform: scale(1.1) rotateY(10deg) !important;
        filter: 
            drop-shadow(0 0 40px rgba(255, 255, 255, 0.7))
            drop-shadow(0 20px 40px rgba(0, 0, 0, 0.5)) !important;
    }
    
    /* Enhanced tagline with gradient text and subtle movements */
    .tagline {
        font-size: 2rem;
        font-weight: 600;
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1.5rem 0 3rem 0;
        letter-spacing: 0.1em;
        text-align: center;
        text-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        position: relative;
        animation: taglineFloat 4s ease-in-out infinite;
    }
    
    @keyframes taglineFloat {
        0%, 100% { 
            transform: translateY(0px) scale(1); 
            text-shadow: 0 0 20px rgba(59, 130, 246, 0.3);
        }
        33% { 
            transform: translateY(-3px) scale(1.01); 
            text-shadow: 0 0 25px rgba(139, 92, 246, 0.4);
        }
        66% { 
            transform: translateY(-1px) scale(1.005); 
            text-shadow: 0 0 22px rgba(236, 72, 153, 0.35);
        }
    }
    
    .tagline::after {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
        animation: taglineShine 5s ease-in-out infinite;
    }
    
    @keyframes taglineShine {
        0%, 100% { left: -100%; }
        50% { left: 100%; }
    }
    
    /* Enhanced button styling with advanced effects */
    .stButton {
        display: flex;
        justify-content: center;
        margin: 3rem 0;
        text-align: center;
    }
    
    div[data-testid="column"] {
        display: flex;
        justify-content: center;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 30%, #be185d 70%, #dc2626 100%);
        color: white;
        font-weight: 700;
        font-size: 1.3rem;
        padding: 1.2rem 4rem;
        border: none;
        border-radius: 60px;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 
            0 15px 35px rgba(59, 130, 246, 0.4),
            0 5px 15px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 2px solid rgba(255, 255, 255, 0.1);
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
        transition: left 0.6s ease;
    }
    
    .stButton > button::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, transparent 100%);
        border-radius: 60px;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-5px) scale(1.05);
        box-shadow: 
            0 25px 50px rgba(59, 130, 246, 0.6),
            0 10px 25px rgba(0, 0, 0, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.3);
        background: linear-gradient(135deg, #2563eb 0%, #8b5cf6 30%, #db2777 70%, #ef4444 100%);
        border-color: rgba(255, 255, 255, 0.2);
    }
    
    .stButton > button:active {
        transform: translateY(-2px) scale(1.02);
    }
    
    /* Enhanced copyright with fade effect */
    .copyright {
        font-size: 1rem;
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.6) 0%, rgba(255, 255, 255, 0.3) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-top: 4rem;
        text-align: center;
        letter-spacing: 0.5px;
        animation: fadeInOut 4s ease-in-out infinite;
    }
    
    @keyframes fadeInOut {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    /* Enhanced responsive design */
    @media (max-width: 768px) {
        .welcome-title {
            font-size: 3.5rem;
        }
        
        .subtitle {
            font-size: 1.8rem;
            margin-bottom: 2rem;
        }
        
        .welcome-card {
            padding: 2.5rem 2rem;
            margin: 1rem;
            border-radius: 24px;
        }
        
        .tagline {
            font-size: 1.6rem;
            margin: 1rem 0 2rem 0;
        }
        
        .stButton > button {
            padding: 1rem 3rem;
            font-size: 1.1rem;
        }
        
        img {
            padding: 15px;
        }
    }
    
    @media (max-width: 480px) {
        .welcome-title {
            font-size: 2.8rem;
        }
        
        .subtitle {
            font-size: 1.5rem;
        }
        
        .welcome-card {
            padding: 2rem 1.5rem;
            margin: 0.5rem;
        }
        
        .tagline {
            font-size: 1.4rem;
        }
    }
    
    /* Scroll indicator */
    .scroll-indicator {
        position: absolute;
        bottom: 2rem;
        left: 50%;
        transform: translateX(-50%);
        width: 2px;
        height: 40px;
        background: linear-gradient(to bottom, rgba(255, 255, 255, 0.8), transparent);
        border-radius: 2px;
        animation: scrollPulse 2s ease-in-out infinite;
    }
    
    @keyframes scrollPulse {
        0%, 100% { opacity: 0.5; height: 40px; }
        50% { opacity: 1; height: 60px; }
    }
</style>
""", unsafe_allow_html=True)

# Create a container for centering
container = st.container()

with container:
    # Title first, then logo below
    st.markdown("""
    <div class="main-container">
        <div class="welcome-card">
            <h1 class="welcome-title">AI Rockfall Risk Assessment System</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Icon image (centered) - positioned below the title
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image("images/icon.png", width=220)
    
    # Close the main container div
    st.markdown("""
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced tagline
    st.markdown("""
    <div class="tagline">Predict. Monitor. Secure.</div>
    """, unsafe_allow_html=True)
    
    # Enhanced button with better centering
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started"):
            st.switch_page("pages/dashboard.py")
    
    # Enhanced copyright
    st.markdown("""
    <div class="copyright">© 2024 Your Company</div>
    """, unsafe_allow_html=True)
    
    # Subtle scroll indicator
    st.markdown("""
    <div class="scroll-indicator"></div>
    """, unsafe_allow_html=True)