import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

treasury_tickers = {"13 Week": "^IRX", "5 Year": "^FVX", "10 Year": "^TNX", "30 Year": "^TYX"}
yield_curve_data = {}

for label, ticker in treasury_tickers.items():
    data = yf.Ticker(ticker).history(period="1d")
    if not data.empty:

        yield_curve_data[label] = data['Close'].iloc[-1] / 100

bond_data = {
    'Bond_ID': ['Corp_Green_A', 'Corp_Green_B', 'Corp_Trad_C', 'Muni_Green_D', 'Gov_Trad_E'],
    'Sector': ['Tech', 'Energy', 'Industrial', 'Infrastructure', 'Government'],
    'ESG_Rating': ['AAA', 'AA', 'BBB', 'AAA', 'A'],
    'Face_Value': [1000, 1000, 1000, 1000, 1000],
    'Coupon_Rate': [0.045, 0.052, 0.060, 0.038, 0.040], # Annual coupon rate
    'Years_to_Maturity': [5, 10, 5, 30, 10],
    'Climate_Impact_Score': [95, 88, 40, 92, 75] # Scale 0-100 (Higher = better impact)
}

portfolio = pd.DataFrame(bond_data)


esg_portfolio = portfolio[portfolio['Climate_Impact_Score'] > 70].copy()


def calculate_bond_price(face_value, coupon_rate, yield_to_maturity, years):
    cash_flows = np.array([face_value * coupon_rate] * years)
    cash_flows[-1] += face_value # Add principal repayment to final year
    discount_factors = np.array([1 / ((1 + yield_to_maturity) ** t) for t in range(1, years + 1)])
    return np.sum(cash_flows * discount_factors)

def calculate_macaulay_duration(face_value, coupon_rate, yield_to_maturity, years, price):
    
    times = np.arange(1, years + 1)
    cash_flows = np.array([face_value * coupon_rate] * years)
    cash_flows[-1] += face_value
    discounted_cash_flows = cash_flows / ((1 + yield_to_maturity) ** times)
    duration = np.sum(times * discounted_cash_flows) / price
    return duration

maturity_to_yield_key = {5: "5 Year", 10: "10 Year", 30: "30 Year"}

prices = []
durations = []

for index, row in esg_portfolio.iterrows():
    
    current_yield = yield_curve_data[maturity_to_yield_key[row['Years_to_Maturity']]]
    
    
    credit_spread = 0.005 if row['ESG_Rating'] == 'AAA' else 0.01
    discount_rate = current_yield + credit_spread
    
 
    price = calculate_bond_price(row['Face_Value'], row['Coupon_Rate'], discount_rate, row['Years_to_Maturity'])
    duration = calculate_macaulay_duration(row['Face_Value'], row['Coupon_Rate'], discount_rate, row['Years_to_Maturity'], price)
    
    prices.append(price)
    durations.append(duration)

esg_portfolio['Calculated_Price'] = prices
esg_portfolio['Mac_Duration'] = durations

print(esg_portfolio[['Bond_ID', 'Sector', 'Calculated_Price', 'Mac_Duration']].to_string(index=False))


sns.set_theme(style="darkgrid")
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

axes[0].plot(list(yield_curve_data.keys()), [y * 100 for y in yield_curve_data.values()], marker='o', color='crimson', linewidth=2)
axes[0].set_title('Live US Treasury Yield Curve', fontsize=14)
axes[0].set_xlabel('Maturity')
axes[0].set_ylabel('Yield (%)')

scatter = sns.scatterplot(
    data=esg_portfolio, 
    x='Mac_Duration', 
    y='Calculated_Price', 
    hue='Sector', 
    s=300, 
    ax=axes[1],
    palette='viridis'
)

for i, row in esg_portfolio.iterrows():
    axes[1].text(row['Mac_Duration'] + 0.2, row['Calculated_Price'], row['Bond_ID'], fontsize=10)

axes[1].set_title('Interest Rate Risk (Duration) vs. Price', fontsize=14)
axes[1].set_xlabel('Macaulay Duration (Years)')
axes[1].set_ylabel('Bond Price ($)')
axes[1].axhline(y=1000, color='gray', linestyle='--', label='Par Value ($1000)')
axes[1].legend()

plt.tight_layout()
plt.show()