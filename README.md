# Indian Quant Research Platform

An institutional-grade quantitative research platform for Indian stock markets focused on discovering and validating predictive edge with rigorous research standards.

---

## Objectives

This platform is designed to:

- Research market inefficiencies
- Evaluate predictive signals
- Test Gann methodologies scientifically
- Build machine learning models
- Perform robust backtesting
- Conduct walk-forward validation
- Run Monte Carlo simulations
- Measure risk-adjusted performance

This platform is **NOT** a stock tip generator.

---

## Research Integrity Principles

### Never

- Assume profitability
- Assume Gann methods work
- Use look-ahead bias
- Use future information
- Hide poor performance
- Optimize solely for historical returns

### Always

- Report uncertainty
- Report confidence intervals
- Report out-of-sample performance
- Report benchmark comparisons
- Report transaction-cost-adjusted performance
- Report model degradation
- Report feature importance

---

## Benchmark Requirements

Every strategy must be compared against:

- Nifty 50 Buy & Hold
- Bank Nifty Buy & Hold
- Stock Buy & Hold

Metrics:

- Excess Return
- Alpha
- Beta
- Tracking Error
- Information Ratio

---

## Performance Metrics

### Performance Summary

- CAGR
- Annual Return
- Sharpe Ratio
- Sortino Ratio
- Calmar Ratio
- Max Drawdown
- Profit Factor
- Win Rate
- Average Trade
- Exposure

### Statistical Summary

- Precision
- Recall
- F1 Score
- ROC AUC
- Brier Score
- Calibration Curve

### Explainability

- SHAP Values
- Feature Importance
- Top Predictive Features

### Robustness

- Walk Forward Results
- Monte Carlo Results
- Stress Test Results
- Sensitivity Analysis

---

## Technology Stack

### Backend

- Python 3.12+
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis

### Data Science

- Pandas
- NumPy
- SciPy
- Scikit-Learn
- XGBoost
- LightGBM
- SHAP

### Infrastructure

- Docker
- Docker Compose
- GitHub Actions

### Frontend

- React
- TypeScript

---

## Project Structure

```text
indian-quant-research-platform/

├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── domain/
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── ml/
│   │   ├── gann/
│   │   ├── backtesting/
│   │   ├── reporting/
│   │   └── main.py
│   │
│   └── tests/
│
├── frontend/
│
├── infrastructure/
│
├── docs/
│
├── scripts/
│
└── data/
```

---

## Setup

### Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/indian-quant-research-platform.git

cd indian-quant-research-platform
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## Run Backend

```bash
cd backend

uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

---

## Testing

```bash
pytest
```

---

## Expected Research Outcome

The platform is expected to report both successful and failed hypotheses.

If a strategy does not outperform:

- Buy & Hold
- Nifty 50
- Bank Nifty

after transaction costs and out-of-sample validation, the report should clearly state:

```text
NO RELIABLE EDGE DETECTED
```

Research integrity is more important than attractive performance results.

---

## License

MIT License
