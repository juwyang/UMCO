import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis


def calculate_stats(series: pd.Series):
    """
    Calculate key statistics for a time series.
    
    Args:
        series: Input time series
        
    Returns:
        dict: Dictionary of statistics
    """
    stats = {
        'count': len(series),
        'mean': series.mean(),
        'std': series.std(),
        'autocorr_lag1': series.autocorr(lag=1),
        'autocorr_lag2': series.autocorr(lag=2),
        'autocorr_lag3': series.autocorr(lag=3),
        'skew': series.skew(),
        'kurtosis': series.kurt()
    }
    return stats


def calculate_descriptive_stats(df: pd.DataFrame, 
                                themes: list,
                                trading_days: int = 252):
    """
    Calculate descriptive statistics for theme-based returns.
    
    Args:
        df: DataFrame with price_change and theme symbols
        themes: List of theme column names (e.g., ['currency_sym', 'demand_sym'])
        trading_days: Trading days per year for annualization
        
    Returns:
        pd.DataFrame: Table of descriptive statistics
    """
    def theme_stats(series: pd.Series) -> dict:
        s = series.dropna()
        count = int(s.shape[0])
        if count == 0:
            return {
                'Count': 0, 'Mean (in %)': np.nan, 'SD (Ann.)': np.nan,
                'Skew': np.nan, 'Kurt': np.nan, 'AC(1)': np.nan, 'AC(2)': np.nan
            }
        mean_pct = s.mean() * 100.0
        sd_ann = s.std(ddof=1) * np.sqrt(trading_days)
        sk = skew(s, bias=False) if count > 2 else np.nan
        kur = kurtosis(s, fisher=True, bias=False) if count > 3 else np.nan
        ac1 = s.autocorr(lag=1) if count > 1 else np.nan
        ac2 = s.autocorr(lag=2) if count > 2 else np.nan
        return {
            'Count': count, 'Mean (in %)': mean_pct, 'SD (Ann.)': sd_ann,
            'Skew': sk, 'Kurt': kur, 'AC(1)': ac1, 'AC(2)': ac2
        }
    
    # Full return statistics
    result = pd.DataFrame(theme_stats(df['price_change']), index=['Return']).T
    
    # Theme statistics
    theme_readable = [c.replace('_sym', '').capitalize() for c in themes]
    stats_dict = {}
    
    for sym_col, name in zip(themes, theme_readable):
        ret_col = sym_col.replace('_sym', '_ret')
        if ret_col not in df.columns:
            df[ret_col] = df['price_change'] * df[sym_col]
        
        active_mask = df[sym_col] == 1
        condensed = df.loc[active_mask, ret_col]
        stats_dict[name] = theme_stats(condensed)
    
    theme_table = pd.DataFrame(stats_dict)
    final_table = pd.concat([result, theme_table], axis=1)
    
    row_order = ['Count', 'Mean (in %)', 'SD (Ann.)', 'Skew', 'Kurt', 'AC(1)', 'AC(2)']
    final_table = final_table.reindex(row_order)
    
    return final_table
