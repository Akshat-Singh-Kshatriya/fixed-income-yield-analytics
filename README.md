# Fixed Income Portfolio Modeling & Yield Analysis

## Overview
This repository contains a quantitative pricing and risk-assessment model for fixed-income securities. Designed around passive investing strategies and green bond integration, the framework extracts macroeconomic data to construct a live US Treasury yield curve and calculates core fixed-income metrics for a simulated ESG corporate bond portfolio.

## Key Features
* **Live Yield Curve Construction:** Programmatically extracts current US Treasury yields (13-week to 30-year) to establish a baseline risk-free rate environment.
* **Bond Pricing Engine:** Calculates the Present Value (PV) of future cash flows, applying dynamic discount rates based on maturity and ESG-driven credit spreads.
* **Interest Rate Risk Modeling:** Calculates Macaulay Duration to quantify portfolio sensitivity to Federal Reserve interest rate movements.
* **ESG Integration:** Incorporates climate impact scores and ESG ratings directly into the credit spread logic, modeling cheaper borrowing costs for AAA-rated sustainable initiatives.

## Tech Stack 
* **Language:** Python (Pandas, Numpy)
* **Data Visualization:** Matplotlib, Seaborn
* **APIs:** Yahoo Finance (`yfinance`)

## Technical Insights
The model effectively demonstrates the inverse relationship between interest rates and bond prices, highlighting duration risk. For example, in the current high-yield environment, the model correctly prices long-duration (16.5 years) infrastructure bonds at a deep discount (~$756 against a $1000 par value), illustrating the severe impact of duration risk compared to short-term corporate paper.

## Installation & Usage
1. Clone the repository:
```bash
   git clone [https://github.com/Akshat-Singh-Kshatriya/fixed-income-yield-analytics.git](https://github.com/Akshat-Singh-Kshatriya/fixed-income-yield-analytics.git)
   cd fixed-income-yield-analytics
```
2. Install the Dependencies
```bash
pip install -r requirements.txt
```
3. Run the Model
```bash
python fixed_income.py
```
