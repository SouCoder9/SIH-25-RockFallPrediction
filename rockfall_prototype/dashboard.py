import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(page_title="AI Rockfall Risk Assessment System", layout="wide")

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f3d7a;
        text-align: center;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #1f3d7a;
        border-bottom: 2px solid #1f3d7a;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
        background: linear-gradient(90deg, #f5f7fa 0%, transparent 100%);
        padding-left: 10px;
    }
    .risk-critical {
        background: linear-gradient(135deg, #ff4b4b 0%, #cc0000 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
    }
    .risk-high {
        background: linear-gradient(135deg, #ff8c4b 0%, #e67300 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(255, 140, 75, 0.3);
    }
    .risk-moderate {
        background: linear-gradient(135deg, #ffc44b 0%, #e6ac00 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(255, 196, 75, 0.3);
    }
    .risk-low {
        background: linear-gradient(135deg, #4caf50 0%, #2e7d32 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        font-size: 2rem;
        margin: 20px 0;
        box-shadow: 0 4px 8px rgba(76, 175, 80, 0.3);
    }
    .parameter-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 15px;
        border-left: 4px solid #1f3d7a;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .recommendation-box {
        background: linear-gradient(135deg, #fff4f4 0%, #ffe9e9 100%);
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 5px solid #ff4b4b;
        color: #333333;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .recommendation-box ul {
        color: #333333;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .recommendation-box li {
        margin-bottom: 5px;
    }
    .factor-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 10px;
        border-left: 4px solid #6c757d;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    .progress-container {
        background-color: #e9ecef;
        border-radius: 5px;
        height: 20px;
        margin: 5px 0;
        overflow: hidden;
    }
    .progress-bar {
        height: 100%;
        border-radius: 5px;
        text-align: right;
        padding-right: 5px;
        color: white;
        font-weight: bold;
        line-height: 20px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .minimal { background: linear-gradient(90deg, #28a745 0%, #20c997 100%); }
    .low { background: linear-gradient(90deg, #7cc3ff 0%, #4da6ff 100%); }
    .moderate { background: linear-gradient(90deg, #ffc107 0%, #ffb300 100%); }
    .high { background: linear-gradient(90deg, #fd7e14 0%, #ff8c00 100%); }
    .extreme { background: linear-gradient(90deg, #dc3545 0%, #c82333 100%); }
    .factor-label {
        font-weight: bold;
        margin-bottom: 5px;
        color: #1f3d7a;
    }
    .factor-value {
        font-size: 0.9rem;
        color: #6c757d;
    }
    .stats-box {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 15px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        border: 1px solid #dee2e6;
    }
    .stats-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f3d7a;
    }
    .stats-label {
        font-size: 0.9rem;
        color: #6c757d;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1f3d7a 0%, #2c5282 100%);
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: 5px;
        font-weight: bold;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2c5282 0%, #1f3d7a 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .reset-button>button {
        background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
    }
    .reset-button>button:hover {
        background: linear-gradient(135deg, #5a6268 0%, #6c757d 100%);
    }
    .graph-container {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">AI Rockfall Risk Assessment System</p>', unsafe_allow_html=True)
st.markdown("Enter geological and environmental parameters to predict rockfall probability")

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

# Function to calculate risk
def calculate_risk(rainfall, snowfall, wind_speed, temperature, elevation, fracture_spacing, fracture_orientation, slope_angle, rock_type):
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
    
    # Calculate weighted risk score (0-100)
    weights = {
        'rainfall': 0.15,
        'snowfall': 0.10,
        'wind_speed': 0.05,
        'temperature': 0.10,
        'elevation': 0.10,
        'fracture_density': 0.25,
        'slope_angle': 0.20,
        'rock_type': 0.05
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
    
    # Determine risk level
    if weighted_risk >= 75:
        risk_level = "CRITICAL"
        confidence = 85
    elif weighted_risk >= 50:
        risk_level = "HIGH"
        confidence = 80
    elif weighted_risk >= 25:
        risk_level = "MODERATE"
        confidence = 75
    else:
        risk_level = "LOW"
        confidence = 70
    
    return weighted_risk, risk_level, confidence, contributions

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
        line=dict(color='#1f3d7a'),
        fillcolor='rgba(31, 61, 122, 0.3)'
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
            colors.append('#28a745')
        elif val < 40:
            colors.append('#7cc3ff')
        elif val < 60:
            colors.append('#ffc107')
        elif val < 80:
            colors.append('#fd7e14')
        else:
            colors.append('#dc3545')
    
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
            'bar': {'color': "#1f3d7a"},
            'steps': [
                {'range': [0, 25], 'color': '#4caf50'},
                {'range': [25, 50], 'color': '#ffc44b'},
                {'range': [50, 75], 'color': '#ff8c4b'},
                {'range': [75, 100], 'color': '#ff4b4b'}],
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
        st.markdown('<p class="sub-header">Environmental & Geological Parameters</p>', unsafe_allow_html=True)
        
        st.markdown("### Weather Conditions")
        st.markdown('<div class="parameter-box">', unsafe_allow_html=True)
        rainfall = st.slider("Rainfall (mm/24h)", 0, 100, st.session_state.rainfall)
        snowfall = st.slider("Snowfall (cm/24h)", 0, 50, st.session_state.snowfall)
        wind_speed = st.slider("Wind Speed (km/h)", 0, 100, st.session_state.wind_speed)
        temperature = st.slider("Temperature (°C)", -20, 40, st.session_state.temperature)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### Geological Conditions")
        st.markdown('<div class="parameter-box">', unsafe_allow_html=True)
        elevation = st.slider("Elevation (m)", 0, 3000, st.session_state.elevation)
        fracture_spacing = st.slider("Fracture Spacing (cm)", 1, 200, st.session_state.fracture_spacing)
        fracture_orientation = st.slider("Fracture Orientation (°)", 0, 90, st.session_state.fracture_orientation)
        slope_angle = st.slider("Slope Angle (°)", 0, 90, st.session_state.slope_angle)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Rock Type")
        rock_type = st.selectbox(
            "Select Rock Type",
            ["Limestone", "Sandstone", "Shale", "Granite", "Basalt"],
            index=0 if st.session_state.rock_type == "Limestone" else 
                  1 if st.session_state.rock_type == "Sandstone" else
                  2 if st.session_state.rock_type == "Shale" else
                  3 if st.session_state.rock_type == "Granite" else 4
        )
        
        # Calculate and Reset buttons
        calc_col, reset_col = st.columns(2)
        with calc_col:
            calculate_btn = st.form_submit_button("Calculate Risk")
        with reset_col:
            if st.form_submit_button("Reset"):
                st.session_state.rainfall = 6
                st.session_state.snowfall = 4
                st.session_state.wind_speed = 0
                st.session_state.temperature = 15
                st.session_state.elevation = 1000
                st.session_state.fracture_spacing = 50
                st.session_state.fracture_orientation = 45
                st.session_state.slope_angle = 30
                st.session_state.rock_type = "Limestone"
                st.experimental_rerun()

# Calculate risk when button is clicked
if calculate_btn:
    risk_percentage, risk_level, confidence, contributions = calculate_risk(
        rainfall, snowfall, wind_speed, temperature, elevation, 
        fracture_spacing, fracture_orientation, slope_angle, rock_type
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
    st.markdown('<p class="sub-header">Risk Assessment Results</p>', unsafe_allow_html=True)
    
    # Display risk level with appropriate styling
    if risk_level == "CRITICAL":
        st.markdown(f'<div class="risk-critical">{risk_percentage:.0f}% {risk_level} RISK<br>Confidence Level: {confidence}%</div>', unsafe_allow_html=True)
    elif risk_level == "HIGH":
        st.markdown(f'<div class="risk-high">{risk_percentage:.0f}% {risk_level} RISK<br>Confidence Level: {confidence}%</div>', unsafe_allow_html=True)
    elif risk_level == "MODERATE":
        st.markdown(f'<div class="risk-moderate">{risk_percentage:.0f}% {risk_level} RISK<br>Confidence Level: {confidence}%</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="risk-low">{risk_percentage:.0f}% {risk_level} RISK<br>Confidence Level: {confidence}%</div>', unsafe_allow_html=True)
    
    # Risk level indicator
    risk_labels = ["Low", "Moderate", "High", "Critical"]
    risk_colors = ["#4caf50", "#ffc44b", "#ff8c4b", "#ff4b4b"]
    
    risk_cols = st.columns(4)
    for i, (label, color) in enumerate(zip(risk_labels, risk_colors)):
        with risk_cols[i]:
            if label.upper() == risk_level:
                st.markdown(f"<div style='text-align: center; font-weight: bold; color: {color};'>{label}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center;'>{label}</div>", unsafe_allow_html=True)
    
    # Create analysis graphs
    radar_fig, bar_fig, gauge_fig = create_analysis_graph(contributions, risk_percentage)
    
    # Display graphs
    st.markdown("---")
    st.markdown("### Risk Analysis Visualization")
    
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(radar_fig, use_container_width=True)
    with col2:
        st.plotly_chart(bar_fig, use_container_width=True)
    
    st.plotly_chart(gauge_fig, use_container_width=True)
    
    # Risk factor contributions with visual indicators
    st.markdown("---")
    st.markdown("### Risk Factor Contributions")
    
    # Calculate statistics
    active_factors = sum(1 for value in contributions.values() if value > 5)  # Consider factors > 5% as active
    avg_impact = sum(contributions.values()) / len(contributions)
    max_impact = max(contributions.values())
    
    # Display statistics
    stat_cols = st.columns(3)
    with stat_cols[0]:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-value">{max_impact:.0f}%</div>
            <div class="stats-label">Highest Factor</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[1]:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-value">{avg_impact:.0f}%</div>
            <div class="stats-label">Average Impact</div>
        </div>
        """, unsafe_allow_html=True)
    with stat_cols[2]:
        st.markdown(f"""
        <div class="stats-box">
            <div class="stats-value">{active_factors}/{len(contributions)}</div>
            <div class="stats-label">Active Factors</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display each factor with progress bar
    for factor, value in contributions.items():
        category, css_class = get_risk_category(value)
        
        st.markdown(f"""
        <div class="factor-box">
            <div class="factor-label">{factor}</div>
            <div class="factor-value">{category} {value:.0f}%</div>
            <div class="progress-container">
                <div class="progress-bar {css_class}" style="width: {value}%">{value:.0f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommended actions
    st.markdown("---")
    st.markdown("### Recommended Actions")
    
    if risk_level == "CRITICAL":
        st.markdown("""
        <div class="recommendation-box">
            <b>Immediate evacuation and area closure required.</b> Deploy emergency monitoring systems.
            Implement slope stabilization measures as soon as conditions allow.
            <ul>
                <li>Evacuate all personnel from the risk zone immediately</li>
                <li>Close access roads and establish safety perimeters</li>
                <li>Deploy real-time monitoring equipment with emergency alerts</li>
                <li>Notify emergency response teams and local authorities</li>
                <li>Schedule immediate geotechnical assessment</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_level == "HIGH":
        st.markdown("""
        <div class="recommendation-box">
            <b>High risk of rockfall.</b> Restrict access to the area. Increase monitoring frequency.
            Implement protective measures such as rockfall nets or barriers.
            <ul>
                <li>Restrict access to high-risk areas</li>
                <li>Increase monitoring frequency to daily inspections</li>
                <li>Install warning signs and barriers</li>
                <li>Evaluate need for protective measures (nets, fences)</li>
                <li>Develop evacuation plan for affected areas</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif risk_level == "MODERATE":
        st.markdown("""
        <div class="recommendation-box">
            <b>Moderate risk level.</b> Continue regular monitoring. Implement warning systems.
            Schedule regular inspections, especially after heavy rainfall or freeze-thaw cycles.
            <ul>
                <li>Continue standard monitoring procedures</li>
                <li>Implement warning systems for personnel</li>
                <li>Schedule bi-weekly inspections</li>
                <li>Increase vigilance after significant weather events</li>
                <li>Review and update safety protocols</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="recommendation-box">
            <b>Low risk level.</b> Maintain regular monitoring schedule. Continue standard safety protocols.
            Review and update emergency response plans as needed.
            <ul>
                <li>Continue standard monitoring schedule</li>
                <li>Maintain existing safety protocols</li>
                <li>Quarterly review of risk assessment</li>
                <li>Train personnel on rockfall recognition and response</li>
                <li>Update emergency response plans annually</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)