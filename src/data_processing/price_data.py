import pandas as pd
import numpy as np


def load_price_data(file_path):
    """Load price data from CSV or Excel file."""
    if str(file_path).endswith('.xlsx'):
        df = pd.read_excel(file_path, engine='openpyxl')
        if 'Exchange Date' in df.columns:
            df.rename(columns={'Exchange Date': 'Date'}, inplace=True)
    else:
        df = pd.read_csv(file_path)
    
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def calculate_price_features(df):
    """Calculate various price-based features."""
    df = df.copy()
    
    # Cumulative returns
    df['cumulative_return'] = (1 + df['price_change']).cumprod()
    
    # Rolling statistics
    for window in [5, 20, 60]:
        df[f'rolling_mean_{window}'] = df['price_change'].rolling(window=window).mean()
        df[f'rolling_std_{window}'] = df['price_change'].rolling(window=window).std()
    
    return df
