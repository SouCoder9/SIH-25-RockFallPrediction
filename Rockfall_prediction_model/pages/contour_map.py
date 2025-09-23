import streamlit as st
import numpy as np
import plotly.graph_objects as go
import hashlib
from scipy.ndimage import zoom

# Set page configuration for the contour map page
st.set_page_config(page_title="Contour Maps", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 4rem;
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
    
    .stPlotlyChart {
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(226, 232, 240, 0.5);
    }
    
    .go-back-button a button {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1.1rem;
        font-family: 'Inter', sans-serif;
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        position: relative;
        overflow: hidden;
    }
    
    .go-back-button a button:hover {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<p class="main-header">🗺️ Contour Map & Terrain Analysis</p>', unsafe_allow_html=True)

# Function to generate realistic mine-like terrain data
def generate_terrain_data(image_analysis):
    # Get values from session state
    slope_steepness = image_analysis.get('slope_steepness', 50) 
    rock_fractures = image_analysis.get('rock_fractures', 50)   
    vegetation_cover = image_analysis.get('vegetation_cover', 50)
    erosion_signs = image_analysis.get('erosion_signs', 50)
    rock_type_confidence = image_analysis.get('rock_type_confidence', 50)
    
    # Create a unique seed based on the image analysis values
    seed_string = f"{slope_steepness}_{rock_fractures}_{vegetation_cover}_{erosion_signs}_{rock_type_confidence}"
    seed = int(hashlib.md5(seed_string.encode()).hexdigest()[:8], 16)
    np.random.seed(seed)
    
    x = np.linspace(-5, 5, 100)
    y = np.linspace(-5, 5, 100)
    X, Y = np.meshgrid(x, y)
    
    # Base elevation - mines typically have significant elevation changes
    base_elevation = 800  # Higher base for mine-like terrain
    
    # 1. PRIMARY TERRAIN SHAPE (Most significant factor)
    # Slope steepness determines the overall mountain shape
    steepness_factor = 0.5 + (slope_steepness / 100) * 2.0
    
    # Create a central peak or ridge based on slope
    if slope_steepness > 70:
        # Steep mountain peak
        Z = base_elevation + 300 * steepness_factor * np.exp(-(X**2 + Y**2)/2)
    elif slope_steepness > 40:
        # Ridgeline terrain
        ridge_angle = (rock_fractures / 100) * np.pi  # Fractures influence ridge orientation
        Z = base_elevation + 200 * np.exp(-((X*np.cos(ridge_angle) + Y*np.sin(ridge_angle))**2)/1.5)
    else:
        # Gentle slopes - more plateau-like
        Z = base_elevation + 100 * np.exp(-(X**2 + Y**2)/3)
    
    # 2. ROCK FRACTURE PATTERNS (Creates realistic mine terrain features)
    fracture_intensity = rock_fractures / 100
    
    # Add fault lines and fracture patterns
    if rock_fractures > 30:
        # Multiple fracture lines at different angles
        for i in range(int(3 + fracture_intensity * 5)):
            angle = (i / max(1, int(3 + fracture_intensity * 5))) * np.pi
            fracture_line = 20 * fracture_intensity * np.sin(5*(X*np.cos(angle) + Y*np.sin(angle)))
            Z += fracture_line * np.exp(-((X*np.cos(angle) + Y*np.sin(angle))**2)/4)
    
    # 3. EROSION PATTERNS (Valleys, gullies, drainage patterns)
    erosion_intensity = erosion_signs / 100
    
    if erosion_signs > 40:
        # Create dendritic drainage patterns (like real terrain)
        for freq in [2, 3, 4]:
            erosion_valley = -50 * erosion_intensity * (
                np.sin(freq*X) * np.cos(freq*Y/2) + 
                np.sin(freq*Y) * np.cos(freq*X/2)
            )
            Z += erosion_valley * np.exp(-(X**2 + Y**2)/6)
    
    # 4. BENCHES AND TERRACES (Typical in mining areas)
    # Rock confidence influences how structured the benches are
    if rock_type_confidence > 60:
        # Create stepped bench patterns
        bench_spacing = 1.0 + (100 - slope_steepness) / 50
        bench_pattern = 30 * (rock_type_confidence / 100) * (
            np.sin(X * bench_spacing) * np.sin(Y * bench_spacing)
        )
        Z += bench_pattern * np.exp(-(X**2 + Y**2)/8)
    
    # 5. VEGETATION SMOOTHING AND SURFACE TEXTURE
    vegetation_smoothing = vegetation_cover / 100
    
    # Vegetation smooths sharp edges but adds micro-topography
    if vegetation_cover > 30:
        # Smoothing effect
        smooth_noise = np.random.normal(0, 5 * (1 - vegetation_smoothing), Z.shape)
        Z += smooth_noise
        
        # Add gentle rolling hills from root systems
        if vegetation_cover > 60:
            micro_topography = 8 * vegetation_smoothing * (
                np.sin(8*X) * np.cos(8*Y) + 
                np.sin(6*Y) * np.cos(6*X)
            )
            Z += micro_topography * np.exp(-(X**2 + Y**2)/10)
    
    # 6. MINING-SPECIFIC FEATURES
    # Add pit-like depressions or waste rock piles based on analysis
    mining_feature_intensity = (slope_steepness + rock_fractures) / 200
    
    # Potential open pit depression
    if slope_steepness > 60 and rock_fractures > 50:
        pit_depth = -80 * mining_feature_intensity
        pit = pit_depth * np.exp(-(X**2 + Y**2)/1.2)
        Z += pit
    
    # Waste rock piles or spoil tips
    if erosion_signs > 70:
        waste_pile = 40 * mining_feature_intensity * np.exp(-((X-2)**2 + (Y-2)**2)/1.5)
        Z += waste_pile
    
    # 7. FIXED FRACTAL NOISE GENERATION (Proper array sizing)
    fractal_noise = np.zeros(Z.shape)
    target_shape = Z.shape
    
    for octave in range(4):
        scale_factor = 2 ** octave
        # Calculate the base shape for this octave
        base_shape = (max(1, target_shape[0] // scale_factor), 
                     max(1, target_shape[1] // scale_factor))
        
        # Generate noise for this octave
        octave_noise = np.random.normal(0, 3.0/(octave+1), base_shape)
        
        # Resize to target shape using proper interpolation
        if base_shape != target_shape:
            # Calculate zoom factors
            zoom_factors = (target_shape[0] / base_shape[0], 
                          target_shape[1] / base_shape[1])
            octave_noise_resized = zoom(octave_noise, zoom_factors, order=1)
            
            # Ensure the resized array matches the target shape exactly
            if octave_noise_resized.shape != target_shape:
                # Trim if larger
                octave_noise_resized = octave_noise_resized[:target_shape[0], :target_shape[1]]
                # Pad if smaller (shouldn't happen with zoom, but just in case)
                if octave_noise_resized.shape != target_shape:
                    pad_rows = target_shape[0] - octave_noise_resized.shape[0]
                    pad_cols = target_shape[1] - octave_noise_resized.shape[1]
                    octave_noise_resized = np.pad(octave_noise_resized, 
                                                ((0, pad_rows), (0, pad_cols)), 
                                                mode='edge')
        else:
            octave_noise_resized = octave_noise
        
        fractal_noise += octave_noise_resized
    
    # Apply fractal noise with vegetation smoothing
    Z += fractal_noise * (1 - vegetation_smoothing * 0.5)
    
    # Ensure realistic elevation range for mine terrain
    Z = np.maximum(Z, 600)  # Minimum elevation
    Z = np.minimum(Z, 1200) # Maximum elevation
    
    return X, Y, Z

# Create interactive 3D contour map with contour lines
def create_contour_map(X, Y, Z, image_analysis):
    # Choose colorscale based on terrain characteristics
    slope_steepness = image_analysis.get('slope_steepness', 50)
    vegetation_cover = image_analysis.get('vegetation_cover', 50)
    
    if vegetation_cover > 60:
        colorscale = 'Earth'
    elif slope_steepness > 70:
        colorscale = 'RdBu_r'
    else:
        colorscale = 'Viridis'
    
    # Create the 3D surface plot
    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=colorscale, 
                                   opacity=0.9, showscale=True)])
    
    # Add contour lines to the surface for better topography reading
    fig.update_traces(contours_z=dict(show=True, usecolormap=True,
                                    highlightcolor="limegreen", project_z=True))
    
    # Add analysis info to title
    analysis_info = ""
    if image_analysis:
        analysis_info = f" (Slope: {image_analysis.get('slope_steepness', 0)}%, Fractures: {image_analysis.get('rock_fractures', 0)}%)"

    fig.update_layout(
        title=f'3D Mine Terrain Contour Map{analysis_info}',
        scene=dict(
            xaxis_title='Distance (km)',
            yaxis_title='Distance (km)',
            zaxis_title='Elevation (m)',
            aspectratio=dict(x=1.2, y=1.2, z=0.8),
            bgcolor="rgba(0,0,0,0)",
            camera=dict(
                eye=dict(x=1.8, y=1.8, z=1.2)
            ),
            zaxis=dict(range=[500, 1300])  # Fixed elevation range for consistency
        ),
        margin=dict(l=0, r=0, t=80, b=0),
        height=700,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#2d3748", family="Inter")
    )
    return fig

# Create 2D contour map for additional perspective
def create_2d_contour_map(X, Y, Z, image_analysis):
    fig = go.Figure(data=
        go.Contour(
            z=Z,
            x=np.linspace(0, 10, 100),  # Convert to km scale
            y=np.linspace(0, 10, 100),
            colorscale='Viridis',
            contours=dict(
                showlabels=True,
                labelfont=dict(size=12, color='white')
            ),
            line_width=2
        )
    )
    
    fig.update_layout(
        title='2D Topographic Contour Map',
        xaxis_title='Distance (km)',
        yaxis_title='Distance (km)',
        height=400,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    return fig

# Main logic to display the map
if 'image_analysis' in st.session_state and st.session_state.image_analysis:
    st.markdown('<p class="intro-text">This terrain map reflects the geological characteristics derived from your uploaded image analysis.</p>', unsafe_allow_html=True)
    
    # Generate terrain data using the analysis results
    analysis_data = st.session_state.image_analysis
    X, Y, Z = generate_terrain_data(analysis_data)
    
    # Display analysis summary
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Slope Steepness", f"{analysis_data.get('slope_steepness', 0)}%")
        st.metric("Rock Fractures", f"{analysis_data.get('rock_fractures', 0)}%")
    with col2:
        st.metric("Vegetation Cover", f"{analysis_data.get('vegetation_cover', 0)}%")
        st.metric("Erosion Signs", f"{analysis_data.get('erosion_signs', 0)}%")
    with col3:
        st.metric("Rock Type Confidence", f"{analysis_data.get('rock_type_confidence', 0)}%")
        st.metric("Terrain Complexity", 
                 f"{(analysis_data.get('slope_steepness', 0) + analysis_data.get('rock_fractures', 0)) // 2}%")
    
    # Create and display the 3D contour map
    fig_3d = create_contour_map(X, Y, Z, analysis_data)
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # Display 2D contour map below
    fig_2d = create_2d_contour_map(X, Y, Z, analysis_data)
    st.plotly_chart(fig_2d, use_container_width=True)
    
    # Add detailed terrain interpretation
    st.markdown("### 🔍 Detailed Terrain Analysis")
    
    interpretation = []
    slope = analysis_data.get('slope_steepness', 0)
    fractures = analysis_data.get('rock_fractures', 0)
    erosion = analysis_data.get('erosion_signs', 0)
    vegetation = analysis_data.get('vegetation_cover', 0)
    
    # Slope analysis
    if slope > 80:
        interpretation.append("⛰️ **Extremely steep terrain** - Sharp peak morphology with rapid elevation changes")
    elif slope > 60:
        interpretation.append("🏔️ **Steep mountainous terrain** - Pronounced ridges and significant slopes")
    elif slope > 40:
        interpretation.append("🌄 **Moderate slopes** - Rolling hills with gradual elevation changes")
    else:
        interpretation.append("🏞️ **Gentle terrain** - Plateau-like features with minimal slope")
    
    # Fracture analysis
    if fractures > 70:
        interpretation.append("🪨 **Highly fractured bedrock** - Complex terrain with multiple fault lines and discontinuities")
    elif fractures > 50:
        interpretation.append("⛏️ **Moderate fracturing** - Visible joint patterns influencing terrain shape")
    else:
        interpretation.append("💎 **Competent rock mass** - Relatively uniform terrain with few fractures")
    
    # Erosion analysis
    if erosion > 60:
        interpretation.append("🌊 **Active erosion processes** - Well-developed drainage patterns and valleys")
    elif erosion > 40:
        interpretation.append("💧 **Moderate erosion signs** - Some gully formation and surface weathering")
    
    # Vegetation analysis
    if vegetation > 70:
        interpretation.append("🌿 **Dense vegetation cover** - Smoothed terrain morphology with organic matter accumulation")
    elif vegetation > 40:
        interpretation.append("🍃 **Moderate vegetation** - Partial terrain stabilization with some surface roughness")
    else:
        interpretation.append("🏜️ **Sparse vegetation** - Exposed bedrock with sharp topographic features")
    
    for item in interpretation:
        st.markdown(f"• {item}")

else:
    st.markdown('<p class="intro-text">Please upload an image and calculate the risk on the main dashboard to generate a custom mine terrain contour map.</p>', unsafe_allow_html=True)
    
    # Generate a default map with neutral analysis
    default_analysis = {
        'slope_steepness': 55,
        'rock_fractures': 45,
        'vegetation_cover': 35,
        'erosion_signs': 40,
        'rock_type_confidence': 60
    }
    X, Y, Z = generate_terrain_data(default_analysis)
    fig_3d = create_contour_map(X, Y, Z, default_analysis)
    st.plotly_chart(fig_3d, use_container_width=True)
    
    st.markdown("### 📋 Sample Mine Terrain Display")
    st.markdown("This shows a typical mining terrain profile. Upload an image on the main dashboard to see terrain analysis based on your specific geological conditions.")

st.markdown("""
<div class="go-back-button">
    <a href="." target="_self">
        <button>← Go Back to Dashboard</button>
    </a>
</div>
""", unsafe_allow_html=True)