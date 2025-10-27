import numpy as np
import pandas as pd
from scipy.stats import linregress


def naive_momentum_strategy(df: pd.DataFrame, lookback: int) -> np.array:
    """
    Implement naive momentum strategy based on cumulative returns.
    
    Args:
        df: DataFrame with 'price_change' column
        lookback: Lookback period in days
        
    Returns:
        np.array: Position signals (-1, 0, 1)
    """
    cum_ret = (1 + df['price_change']).cumprod()
    momentum = cum_ret / cum_ret.shift(lookback)
    positions = np.where(momentum > 1.0, 1, -1)
    positions = np.roll(positions, 1)
    positions[:lookback+1] = 0
    return positions


def slope_momentum_strategy(df: pd.DataFrame, lookback: int) -> np.array:
    """
    Implement slope momentum strategy using linear regression.
    
    Args:
        df: DataFrame with 'price_change' column
        lookback: Lookback period for regression
        
    Returns:
        np.array: Position signals (-1, 0, 1)
    """
    slopes = df['price_change'].rolling(window=lookback).apply(
        lambda x: linregress(range(len(x)), x).slope,
        raw=False
    )
    positions = np.where(slopes > 0, 1, -1)
    positions = np.roll(positions, 1)
    positions[:lookback+1] = 0
    return positions


def calculate_metrics(returns: np.array, risk_free_rate: float = 0.05):
    """
    Calculate performance metrics for a return series.
    
    Args:
        returns: Array of returns
        risk_free_rate: Annual risk-free rate
        
    Returns:
        dict: Dictionary with Sharpe ratio, cumulative return, and max drawdown
    """
    # Annualized Sharpe Ratio
    excess_returns = returns - risk_free_rate / 252
    sharpe = np.sqrt(252) * np.mean(excess_returns) / np.std(returns)
    
    # Cumulative Return
    cum_ret = (1 + returns).cumprod()[-1] - 1
    
    # Maximum Drawdown
    cum_ret_series = (1 + returns).cumprod()
    running_max = np.maximum.accumulate(cum_ret_series)
    drawdowns = cum_ret_series / running_max - 1
    max_drawdown = np.min(drawdowns)
    
    return {
        'sharpe': sharpe,
        'cumulative_return': cum_ret,
        'max_drawdown': max_drawdown
    }
