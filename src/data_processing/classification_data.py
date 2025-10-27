import pandas as pd
import re


def extract_theme_scores(df_reason, df_price, categories):
    """
    Extract theme scores from classification data.
    
    Args:
        df_reason: DataFrame with key drivers and classifications
        df_price: DataFrame with price changes
        categories: List of category names to extract
        
    Returns:
        pd.DataFrame: DataFrame with theme scores
    """
    df_reason['date'] = pd.to_datetime(df_reason['date'], format='%Y-%m-%d')
    df_price['Date'] = pd.to_datetime(df_price['Date'])
    
    merged_df = pd.merge(df_reason, df_price, left_on='date', right_on='Date', how='inner')
    
    results = []
    
    for index, row in merged_df.iterrows():
        key_drivers_text = row['key drivers']
        price_change = row['%Chg']
        
        # Extract categories mentioned in parentheses
        mentioned_categories = set(re.findall(r'\((.*?)\)', key_drivers_text))
        mentioned_categories = mentioned_categories.intersection(categories)
        num_categories = len(mentioned_categories)
        
        if num_categories > 0:
            fractional_score = price_change / num_categories
        else:
            fractional_score = 0
        
        row_scores = {
            'date': row['date'],
            'commodity': row['commodity'],
            'price_change': price_change
        }
        
        for cat in categories:
            if cat in mentioned_categories:
                row_scores[f'{cat}_sym'] = 1
            else:
                row_scores[f'{cat}_sym'] = 0
                
        results.append(row_scores)
    
    return pd.DataFrame(results)
