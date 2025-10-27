import pandas as pd
import numpy as np
from pathlib import Path


def load_and_prepare_data(price_csv_path, classification_csv_path, commodity_name):
    """
    Loads, preprocesses, and merges price and classification data.
    
    Args:
        price_csv_path: Path to price data CSV/Excel
        classification_csv_path: Path to classification CSV
        commodity_name: Name of commodity to filter
        
    Returns:
        pd.DataFrame: Merged dataframe with price and classification data
    """
    print(f"Loading price data from: {price_csv_path}")
    try:
        # Handle both CSV and Excel formats
        if str(price_csv_path).endswith('.xlsx'):
            price_df = pd.read_excel(price_csv_path, engine='openpyxl')
            if 'Exchange Date' in price_df.columns:
                price_df.rename(columns={'Exchange Date': 'Date'}, inplace=True)
        else:
            price_df = pd.read_csv(price_csv_path)
            
        price_df['Date'] = pd.to_datetime(price_df['Date'])
        
        # Handle price change column
        if 'Change %' in price_df.columns:
            price_df['price_change'] = price_df['Change %'].astype(str).str.rstrip('%').astype('float') / 100.0
        elif '%Chg' in price_df.columns:
            price_df['price_change'] = price_df['%Chg']
            
        price_df = price_df[['Date', 'price_change']].sort_values(by='Date').reset_index(drop=True)
    except Exception as e:
        print(f"Error loading price data: {e}")
        return None

    print(f"Loading classification data from: {classification_csv_path}")
    try:
        classification_df = pd.read_csv(classification_csv_path)
        classification_df['date'] = pd.to_datetime(classification_df['date'], format='%Y%m%d')
        
        # Filter for specific commodity
        commodity_df = classification_df[
            classification_df['commodity'].str.contains(commodity_name, case=False, na=False)
        ].copy()
        
        if commodity_df.empty:
            print(f"No data found for commodity '{commodity_name}'")
            return None
            
        commodity_df = commodity_df[['date', 'numeric_classification']].rename(columns={'date': 'Date'})
    except Exception as e:
        print(f"Error loading classification data: {e}")
        return None

    print("Merging price and classification data...")
    merged_df = pd.merge(price_df, commodity_df, on='Date', how='inner')
    
    if merged_df.empty:
        print("No data after merging. Check date alignment.")
        return None

    merged_df['numeric_classification'] = merged_df['numeric_classification'].astype(int)
    merged_df.dropna(subset=['price_change', 'numeric_classification'], inplace=True)
    
    print(f"Successfully loaded and merged data. Shape: {merged_df.shape}")
    return merged_df.sort_values(by='Date').reset_index(drop=True)


def load_combined_classification_data(data_dir, years):
    """
    Load and combine classification data from multiple years.
    
    Args:
        data_dir: Directory containing classification CSV files
        years: List of years to load
        
    Returns:
        pd.DataFrame: Combined classification data
    """
    dfs = []
    for year in years:
        file_path = Path(data_dir) / f'{year}_combined_price_movement.csv'
        if file_path.exists():
            df = pd.read_csv(file_path)
            dfs.append(df)
        else:
            print(f"Warning: {file_path} not found")
    
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    return pd.DataFrame()
