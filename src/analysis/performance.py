import numpy as np
import pandas as pd


def calculate_performance_metrics(returns: pd.Series, 
                                  risk_free_rate: float = 0.05,
                                  trading_days: int = 252):
    """
    Calculate comprehensive performance metrics.
    
    Args:
        returns: Series of daily returns
        risk_free_rate: Annual risk-free rate
        trading_days: Trading days per year
        
    Returns:
        dict: Performance metrics
    """
    excess_returns = returns - (risk_free_rate / trading_days)
    
    # Sharpe Ratio
    if excess_returns.std() != 0:
        sharpe = (excess_returns.mean() / excess_returns.std()) * np.sqrt(trading_days)
    else:
        sharpe = 0.0
    
    # Cumulative Return
    cum_return = (1 + returns).cumprod().iloc[-1] - 1
    
    # Maximum Drawdown
    cum_ret_series = (1 + returns).cumprod()
    running_max = np.maximum.accumulate(cum_ret_series)
    drawdowns = cum_ret_series / running_max - 1
    max_dd = drawdowns.min()
    
    # Win Rate
    win_rate = (returns > 0).sum() / len(returns)
    
    # Volatility
    annual_vol = returns.std() * np.sqrt(trading_days)
    
    return {
        'sharpe_ratio': sharpe,
        'cumulative_return': cum_return,
        'max_drawdown': max_dd,
        'win_rate': win_rate,
        'annual_volatility': annual_vol,
        'total_trades': len(returns)
    }


def compare_strategies(strategy_returns: dict, 
                      risk_free_rate: float = 0.05):
    """
    Compare multiple strategies.
    
    Args:
        strategy_returns: Dict of {strategy_name: returns_series}
        risk_free_rate: Annual risk-free rate
        
    Returns:
        pd.DataFrame: Comparison table
    """
    results = []
    
    for name, returns in strategy_returns.items():
        metrics = calculate_performance_metrics(returns, risk_free_rate)
        metrics['strategy'] = name
        results.append(metrics)
    
    df = pd.DataFrame(results)
    df = df.set_index('strategy')
    
    return df
