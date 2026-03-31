# AI-Powered Customer Segmentation

Automatically segments customers using K-Means ML and generates personalised
marketing insights and email campaigns using Claude AI — built entirely in Python.

## Features
- K-Means customer clustering (5 segments by default)
- Interactive Plotly charts and scatter maps
- Claude AI generates segment insights and campaign emails
- One-click CSV download of segmented data
- Zero JavaScript — 100% Python

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/customer-segmentation.git
cd customer-segmentation

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Mac/Linux
# venv\Scripts\activate       # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API key
cp .env.example .env
# Open .env and paste your ANTHROPIC_API_KEY

# 5. Run the app
streamlit run app.py
```

Open http://localhost:8501 in your browser.

## Tech Stack
- **UI**: Streamlit
- **ML**: Scikit-learn (K-Means clustering)
- **AI**: Anthropic Claude API
- **Charts**: Plotly
- **Data**: Pandas + NumPy

## Project Structure
```
customer-segmentation/
├── app.py              # Streamlit dashboard
├── segmentation.py     # ML clustering logic
├── ai_insights.py      # Claude API integration
├── requirements.txt    # Python dependencies
├── .env.example        # API key template
└── README.md
```

## Get Your API Key
Visit https://console.anthropic.com to get your free Anthropic API key.
