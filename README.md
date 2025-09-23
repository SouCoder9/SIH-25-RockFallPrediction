# 🏔️ AI Rockfall Risk Assessment System

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Smart India Hackathon 2025](https://img.shields.io/badge/SIH-2025-orange)](https://sih.gov.in/)

An advanced AI-powered system for predicting and assessing rockfall risks using machine learning, environmental analysis, and computer vision. This comprehensive solution helps in early detection, risk assessment, and mining feasibility analysis to enhance safety measures in mountainous and mining regions.

## ✨ Key Features

- 🤖 **AI-Powered Risk Prediction** - Advanced machine learning algorithms for accurate rockfall risk assessment
- 📊 **Interactive Dashboard** - Beautiful, responsive Streamlit interface with real-time parameter adjustment
- 🗺️ **Risk Heat Maps** - Visual risk assessment with contour mapping and geographical analysis
- 📷 **Computer Vision Analysis** - Image-based slope analysis and rock fracture detection
- ⛏️ **Mining Feasibility Assessment** - Integrated mining safety evaluation based on risk levels
- 📱 **SMS Alert System** - Twilio-powered emergency notifications for critical risk scenarios
- 📈 **Advanced Visualizations** - Interactive charts, radar plots, and gauge meters using Plotly
- 🌦️ **Environmental Monitoring** - Real-time weather and geological parameter integration

## 🏗️ Project Structure

```
SIH-25-RockFallPrediction/
├── Rockfall_prediction_model/
│   ├── intro.py                    # Welcome page with stunning UI
│   ├── pages/
│   │   ├── dashboard.py            # Main risk assessment dashboard
│   │   └── contour_map.py         # Risk heat mapping interface
│   ├── data/
│   │   └── balanced_synthetic_rockfall_data.csv
│   ├── model/
│   │   └── rockfall_model.pkl     # Trained Random Forest model
│   ├── images/
│   │   └── icon.png               # Application icons and assets
│   ├── .env                       # Environment variables (Twilio config)
│   ├── requirements.txt           # Python dependencies
│   └── train_model.py            # ML model training script
├── README.md                      # Project documentation
└── requirements.txt              # Main project dependencies
```

## 🚀 Getting Started

### 📴 Prerequisites

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **pip** (Python package installer)
- **Git** (for cloning the repository)
- **Internet connection** (for downloading dependencies)

### 🛠️ Installation

1. **Clone the repository:**
```bash
git clone https://github.com/SouCoder9/SIH-25-RockFallPrediction.git
cd SIH-25-RockFallPrediction
```

2. **Create and activate a virtual environment:**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install the required dependencies:**
```bash
cd Rockfall_prediction_model
pip install -r requirements.txt
```

4. **Configure SMS alerts (Optional):**
Update the `.env` file in the `Rockfall_prediction_model` directory:
```env
# Twilio SMS Configuration (Optional)
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_FROM_NUMBER=+1234567890
ALERT_TO_NUMBER=+1234567890
```
> ⚠️ **Note**: The app works perfectly without SMS configuration!

### 🏃 Running the Application

1. **Start the application:**
```bash
streamlit run intro.py
```

2. **Access the application:**
- **Local URL**: http://localhost:8501
- **Network URL**: http://your-ip:8501

3. **Navigate the system:**
   - Start from the welcome page
   - Click "Get Started" to access the dashboard
   - Explore risk assessment and heat mapping features

## 📈 Usage Guide

### 🏠 Main Dashboard Features

1. **🌦️ Environmental Parameters**:
   - Adjust rainfall, snowfall, wind speed, and temperature
   - Set elevation and geological conditions
   - Select rock types (Limestone, Sandstone, Shale, Granite, Basalt)

2. **📷 Image Analysis** (Optional):
   - Upload slope images for computer vision analysis
   - Get AI-powered insights on slope conditions
   - Receive fracture density and erosion assessments

3. **⚙️ Risk Assessment**:
   - Click "Calculate Risk" to get comprehensive analysis
   - View risk levels: Low, Moderate, High, Critical
   - Get confidence scores and detailed breakdowns

4. **⛏️ Mining Feasibility**:
   - Receive mining safety recommendations
   - Get feasibility status: Suitable, Conditional, Not Suitable
   - View detailed precautionary measures

5. **📈 Visualizations**:
   - Interactive radar charts showing risk factors
   - Bar charts with contribution analysis
   - Risk gauge meters with color-coded alerts
   - Heat maps for geographical risk assessment

6. **📱 SMS Alerts** (If configured):
   - Enable automatic SMS notifications
   - Receive alerts for high-risk scenarios
   - Get actionable safety recommendations

## 📦 Technology Stack

### Core Technologies
- **Frontend**: Streamlit (Interactive web application)
- **Backend**: Python 3.8+
- **Machine Learning**: Scikit-learn (Random Forest Classifier)
- **Data Visualization**: Plotly, Matplotlib
- **Computer Vision**: PIL (Python Imaging Library)
- **SMS Integration**: Twilio API
- **Data Processing**: Pandas, NumPy

### Key Dependencies
```txt
streamlit>=1.49.1
pandas>=2.3.2
scikit-learn>=1.7.2
plotly>=6.3.0
pillow>=11.3.0
twilio>=9.8.1
python-dotenv>=1.1.1
numpy>=2.3.3
joblib>=1.5.2
```

## 🧑‍💻 Development

### Training a New Model

To train a new model or update the existing one:
```bash
cd Rockfall_prediction_model
python train_model.py
```

### Model Details
- **Algorithm**: Random Forest Classifier
- **Features**: 8 environmental and geological parameters
- **Output**: Risk percentage (0-100%) and risk level classification
- **Accuracy**: ~85-90% on validation data
- **Training Data**: Synthetic balanced dataset with 10,000+ samples

### Adding New Features
1. Modify the risk calculation function in `pages/dashboard.py`
2. Update the UI components for new parameters
3. Retrain the model with new features
4. Test thoroughly with various scenarios

## 🚫 Troubleshooting

### Common Issues

**🚨 Issue**: Streamlit not starting
```bash
# Solution: Check Python version and virtual environment
python --version  # Should be 3.8+
which python     # Should point to your virtual environment
```

**🚨 Issue**: Dependencies not installing
```bash
# Solution: Upgrade pip and try again
pip install --upgrade pip
pip install -r requirements.txt
```

**🚨 Issue**: Twilio SMS not working
- Verify credentials in `.env` file
- Check Twilio account balance
- Ensure phone numbers are in E.164 format (+1234567890)
- Test with the debug information in the sidebar

**🚨 Issue**: Model not loading
```bash
# Solution: Retrain the model
python train_model.py
```

### Performance Optimization
- Use `@st.cache_data` for expensive computations
- Optimize image processing for large uploads
- Consider model quantization for faster inference

## 📊 API Reference

### Key Functions

#### `calculate_risk(parameters...)`
Calculates rockfall risk based on environmental and geological parameters.

**Parameters:**
- `rainfall` (float): 24-hour rainfall in mm
- `snowfall` (float): 24-hour snowfall in cm
- `wind_speed` (float): Wind speed in km/h
- `temperature` (float): Temperature in Celsius
- `elevation` (float): Elevation in meters
- `fracture_spacing` (float): Rock fracture spacing in cm
- `fracture_orientation` (float): Fracture orientation in degrees
- `slope_angle` (float): Slope angle in degrees
- `rock_type` (str): Rock type classification
- `image_analysis` (dict): Computer vision analysis results

**Returns:**
- `risk_percentage` (float): Risk score 0-100%
- `risk_level` (str): LOW/MODERATE/HIGH/CRITICAL
- `confidence` (float): Model confidence percentage
- `contributions` (dict): Individual factor contributions

## 🔒 Security Considerations

- Store Twilio credentials securely in `.env` file
- Never commit sensitive credentials to version control
- Use environment variables for production deployment
- Implement rate limiting for SMS alerts
- Validate all user inputs
- Use HTTPS in production environments

## 🚀 Deployment

### Streamlit Cloud
```bash
# Deploy to Streamlit Cloud
1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Set environment variables in Streamlit Cloud dashboard
4. Deploy automatically
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501
CMD ["streamlit", "run", "intro.py"]
```

## 🏆 Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository
2. **Create** a new branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where appropriate

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🏆 **Smart India Hackathon 2025** - For providing the platform and challenge
- 🔬 **Scientific Community** - For rockfall research and methodologies
- 📚 **Open Source Libraries** - Streamlit, Scikit-learn, Plotly, and others
- 👥 **Contributors and Team Members** - For their dedicated work
- 🏭 **Educational Institutions** - For supporting innovation

## 📞 Contact & Support

For questions, suggestions, or support:
- 📧 **Email**: [your-email@domain.com]
- 🐦 **GitHub Issues**: [Create an Issue](https://github.com/SouCoder9/SIH-25-RockFallPrediction/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/SouCoder9/SIH-25-RockFallPrediction/discussions)

---

<div align="center">

**🏔️ Built for Smart India Hackathon 2025 🏆**

*Enhancing safety in mountainous regions through AI-powered risk assessment*

[![⭐ Star this repo](https://img.shields.io/github/stars/SouCoder9/SIH-25-RockFallPrediction?style=social)](https://github.com/SouCoder9/SIH-25-RockFallPrediction)

</div>
