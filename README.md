# RockFall Prediction System

A machine learning-based dashboard for predicting and monitoring rockfall incidents. This system helps in early detection and notification of potential rockfall events to enhance safety measures.

## Features

- Real-time rockfall prediction
- Interactive dashboard using Streamlit
- Data visualization with Plotly
- SMS notification system using Twilio
- Machine learning model for prediction

## Project Structure

```
rockfall_prototype/
├── dashboard.py          # Main Streamlit dashboard
├── train_model.py       # Model training script
├── requirements.txt     # Project dependencies
├── data/
│   └── balanced_synthetic_rockfall_data.csv
└── model/
    └── rockfall_model.pkl
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. Clone the repository:
```bash
git clone https://github.com/SouCoder9/SIH-25-RockFallPrediction.git
cd SIH-25-RockFallPrediction
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
```

3. Install the required dependencies:
```bash
cd rockfall_prototype
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the `rockfall_prototype` directory with the following contents:
```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
TO_PHONE_NUMBER=recipient_phone_number
```

### Running the Application

1. Start the Streamlit dashboard:
```bash
streamlit run dashboard.py
```

2. Open your web browser and navigate to:
- Local URL: http://localhost:8501
- Network URL: http://your-ip:8501

## Usage

1. The dashboard will display various visualizations and predictions based on the rockfall data
2. You can interact with different components to analyze the data
3. The system will send SMS alerts when potential rockfall risks are detected

## Development

To train a new model or update the existing one:
```bash
python train_model.py
```

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Smart India Hackathon 2025
- Contributors and team members