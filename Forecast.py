import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Load data cleaned
df = pd.read_csv('Global_Inflation_Cleaned.csv')

# Filter years and compute global average
df_filtered = df[(df['Year'] >= 2000) & (df['Year'] <= 2024)]
df_avg = df_filtered.groupby('Year')['Inflation (%)'].mean().reset_index()
df_avg.rename(columns={'Year': 'ds', 'Inflation (%)': 'y'}, inplace=True)

#Convert 'ds' to datetime, ensuring proper format
df_avg['ds'] = pd.to_datetime(df_avg['ds'].astype(str), format='%Y', errors='coerce')

# Check for any NaT values 'ds'
if df_avg['ds'].isnull().any():
    print("There are invalid dates in the 'ds' column.")

# Initialize and fit the model 
model = Prophet(yearly_seasonality=False)
model.fit(df_avg)

# Forecast from 2026-2030
future = model.make_future_dataframe(periods=6, freq='Y')
forecast = model.predict(future)

# Display 
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(6))

#Plot the forecast
plt.figure(figsize=(12, 6))
model.plot(forecast)
plt.title("Forecasted Global Inflation (2025-2030)")
plt.xlabel("Year")
plt.ylabel("Inflation (%)")
plt.grid(True)

# Save the plot to a file 
output_path = "Global_Inflation_forecast.png"
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close() #Close the plot to free memory

print(f"Forecast plot saved to:{output_path}")