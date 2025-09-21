# CorrelHeatmap - Stock Correlation Analysis System

A professional-grade correlation analysis system for stock tickers, built with institutional-quality Python architecture and designed for scalable quantitative research.

## 🎯 Project Overview

This system provides sophisticated correlation analysis capabilities for stock portfolios, enabling:
- Dynamic correlation matrix computation across multiple timeframes
- Interactive heatmap visualizations
- Risk assessment and portfolio optimization insights
- Integration with Interactive Brokers (IBKR) API for real-time data
- Institutional-grade data handling and analysis

## 🏗️ Architecture

### Core Components
- **Data Layer**: Robust data ingestion and preprocessing
- **Analysis Engine**: Statistical correlation computations
- **Visualization**: Interactive heatmaps and correlation matrices
- **Risk Management**: Portfolio risk metrics and alerts
- **API Integration**: IBKR connectivity for live market data

### Design Principles
- **Scalability**: Built to handle large portfolios and high-frequency data
- **Modularity**: Clean separation of concerns with dependency injection
- **Performance**: Optimized for institutional-scale computations
- **Reliability**: Comprehensive error handling and logging
- **Maintainability**: Type hints, documentation, and testing

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- IBKR TWS/Gateway running (for live data)
- Required Python packages (see requirements.txt)

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd CorrelHeatmap

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up configuration
cp config/config.example.yaml config/config.yaml
# Edit config.yaml with your IBKR credentials and preferences
```

### Basic Usage
```python
from correlheatmap import CorrelationAnalyzer
from correlheatmap.data import IBKRDataProvider

# Initialize data provider
data_provider = IBKRDataProvider(config_path="config/config.yaml")

# Create analyzer
analyzer = CorrelationAnalyzer(
    data_provider=data_provider,
    tickers=["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"],
    timeframe="1Y"
)

# Generate correlation matrix
correlation_matrix = analyzer.compute_correlation()

# Create interactive heatmap
analyzer.visualize_heatmap(correlation_matrix)
```

## 📊 Features

### Correlation Analysis
- **Multiple Timeframes**: Daily, weekly, monthly correlations
- **Rolling Correlations**: Dynamic correlation tracking over time
- **Statistical Significance**: P-values and confidence intervals
- **Regime Detection**: Identify correlation regime changes

### Visualization
- **Interactive Heatmaps**: Zoom, pan, and hover for detailed insights
- **Time Series Plots**: Correlation evolution over time
- **Portfolio Risk Metrics**: VaR, CVaR, and correlation-based risk measures
- **Export Capabilities**: High-resolution charts for presentations

### Data Management
- **Multiple Data Sources**: IBKR, Yahoo Finance, Alpha Vantage
- **Data Validation**: Automated data quality checks
- **Caching**: Intelligent caching for performance optimization
- **Real-time Updates**: Live correlation monitoring

## 🛠️ Development

### Project Structure
```
CorrelHeatmap/
├── src/
│   ├── correlheatmap/
│   │   ├── core/           # Core analysis engine
│   │   ├── data/           # Data providers and handlers
│   │   ├── visualization/  # Plotting and visualization
│   │   ├── risk/          # Risk management tools
│   │   └── utils/          # Utility functions
│   └── tests/             # Comprehensive test suite
├── config/                # Configuration files
├── notebooks/             # Jupyter notebooks for research
├── docs/                  # Documentation
└── scripts/               # Utility scripts
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=correlheatmap

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
```

### Code Quality
```bash
# Format code
black src/
isort src/

# Lint code
flake8 src/
mypy src/

# Security scan
bandit -r src/
```

## 📈 Trading Applications

### Portfolio Construction
- Identify uncorrelated assets for diversification
- Optimize portfolio weights based on correlation structure
- Monitor correlation breakdowns for rebalancing signals

### Risk Management
- Real-time correlation monitoring
- Stress testing under correlation regime changes
- Dynamic hedging strategies based on correlation patterns

### Research Applications
- Sector rotation analysis
- Market regime identification
- Cross-asset correlation studies

## 🔧 Configuration

### IBKR Setup
1. Install TWS or IB Gateway
2. Enable API connections in TWS settings
3. Configure port and client ID in config.yaml
4. Test connection with provided utilities

### Data Sources
- **Primary**: Interactive Brokers (real-time, historical)
- **Backup**: Yahoo Finance, Alpha Vantage
- **Custom**: Add your own data providers

## 📚 Documentation

- [API Reference](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Trading Strategies](docs/strategies.md)
- [Performance Optimization](docs/performance.md)

## 🤝 Contributing

This project follows institutional development standards:

1. **Code Review**: All changes require peer review
2. **Testing**: Maintain >90% test coverage
3. **Documentation**: Update docs for all new features
4. **Performance**: Benchmark critical paths
5. **Security**: Regular security audits

## 📄 License

Proprietary - Internal Trading Research Tool

## ⚠️ Disclaimer

This software is for research and educational purposes only. Past performance does not guarantee future results. Always conduct thorough backtesting and risk assessment before deploying any trading strategies.

## 📞 Support

For technical issues or feature requests, please contact the development team or create an issue in the project repository.

---

*Built with institutional-grade Python for serious quantitative research.*
