# 🚀 Stock Pitch AI

> **Advanced Financial Analysis & Automated Presentation Generator**

A comprehensive stock analysis platform that combines sophisticated financial modeling with automated PowerPoint generation. Built for investors, analysts, and finance professionals who need quick, professional-grade stock pitches.

## ✨ Key Features

### 🔬 Advanced Financial Analysis
- **DCF Valuation** with customizable parameters
- **WACC Calculations** using market data
- **Financial Statement Analysis** with comprehensive ratios
- **Risk Assessment** and sensitivity analysis
- **Peer Comparison** and industry benchmarking

### 🎯 Dual Analysis Modes
- **Free Mode**: Advanced rule-based analysis (No API required)
- **Premium Mode**: AI-powered insights with OpenAI GPT

### 📊 Interactive Dashboard
- Real-time stock data visualization
- Interactive charts and metrics
- Customizable analysis parameters
- Professional UI with gradient designs

### 📎 Automated Presentations
- Professional PowerPoint generation
- Comprehensive investment thesis
- Financial charts and visualizations
- Ready-to-present format

## 🚀 Quick Start

### Option 1: One-Click Launch
```bash
./start_app.sh
```

### Option 2: Manual Launch
```bash
cd "/path/to/Stock Pitch Project"
source venv/bin/activate && streamlit run app.py
```

Open your browser to `http://localhost:8501`

## 📋 Requirements

- Python 3.8+
- Internet connection for stock data
- OpenAI API key (optional, for premium features)

## 🛠️ Installation

### Automated Setup
```bash
git clone https://github.com/emnet-4/Stock-Pitch-AI.git
cd "Stock Pitch Project"
chmod +x setup.sh
./setup.sh
```

### Manual Setup
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## 💡 How to Use

1. **Launch the Application**
   - Use the one-click launcher or terminal commands
   - Navigate to http://localhost:8501

2. **Select Analysis Mode**
   - **Professional**: Advanced financial analysis (FREE)
   - **Premium**: AI-powered insights (requires OpenAI API key)

3. **Enter Stock Symbol**
   - Type any valid stock ticker (e.g., AAPL, MSFT, GOOGL)

4. **Customize Parameters**
   - Adjust DCF projection years
   - Set risk-free rate and market risk premium
   - Configure analysis depth

5. **Generate Analysis**
   - Click "Generate Comprehensive Analysis"
   - Review results in interactive tabs

6. **Download Presentation**
   - Generate professional PowerPoint
   - Download for immediate use

## 🔧 Technical Architecture

### Core Components
- **Financial Calculator**: Advanced valuation models
- **Data Analysis Engine**: Rule-based and AI-powered analysis
- **Presentation Generator**: Automated PowerPoint creation
- **Web Interface**: Interactive Streamlit dashboard

### Data Sources
- **Yahoo Finance**: Real-time stock data
- **Financial Statements**: Income statement, balance sheet, cash flow
- **Market Data**: Price history, volatility, beta calculations

### Analysis Methods
- **DCF Modeling**: Discounted cash flow valuation
- **WACC Calculation**: Weighted average cost of capital
- **Ratio Analysis**: Profitability, liquidity, efficiency metrics
- **Risk Assessment**: Beta, volatility, sensitivity analysis

## 📊 Analysis Output

### Executive Summary
- Company overview and investment thesis
- Key financial highlights
- Valuation summary and recommendation

### Financial Analysis
- Revenue and profitability trends
- Balance sheet strength
- Cash flow analysis
- Financial ratios and benchmarks

### Valuation
- DCF model with detailed assumptions
- Multiple valuation approaches
- Sensitivity analysis
- Upside/downside scenarios

### Risk Analysis
- Business and financial risks
- Market and competitive risks
- Regulatory and operational risks
- Risk mitigation strategies

## 🎨 UI Features

### Modern Design
- Gradient color schemes
- Professional card layouts
- Interactive metrics display
- Responsive design

### Enhanced UX
- Real-time data loading
- Progress indicators
- Error handling
- Intuitive navigation

### Custom Styling
- Unique visual identity
- Professional color palette
- Consistent typography
- Polished animations

## 🔐 Security & Privacy

- No data storage or logging
- Secure API key handling
- Local processing only
- No external data sharing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

### Common Issues
- **Port busy**: Streamlit auto-selects available ports
- **Module errors**: Ensure virtual environment is activated
- **API limits**: Check OpenAI API key and usage limits

### Troubleshooting
```bash
# Check installation
ls -la app.py start_app.sh venv/

# Verify dependencies
source venv/bin/activate
pip list | grep -E "(streamlit|yfinance|openai)"

# Test basic functionality
python -c "import streamlit; print('✅ Streamlit OK')"
```

## 📁 Project Structure

```
Stock Pitch AI/
├── app.py                 # Main application (Streamlit interface)
├── requirements.txt       # Python dependencies
├── start_app.sh          # One-click launcher
├── setup.sh              # Environment setup script
├── .env.template         # Environment variables template
├── src/                  # Source code modules
│   ├── data_analysis/    # Financial analysis engines
│   ├── presentation/     # PowerPoint generation
│   └── utils/           # Configuration and logging
├── tests/               # Unit tests
├── logs/                # Application logs
└── output/              # Generated presentations
```

## 🎯 Future Enhancements

- [ ] Options pricing models
- [ ] Monte Carlo simulations
- [ ] ESG scoring integration
- [ ] Multi-currency support
- [ ] Custom report templates
- [ ] API endpoint for integration

---

**Built for fun. Finace Bros it might not be accurate !!

