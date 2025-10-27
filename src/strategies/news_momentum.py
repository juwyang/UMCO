import pandas as pd
import numpy as np
import pmdarima as pm
from tqdm import tqdm


def calculate_arma_residual_scores(df: pd.DataFrame, 
                                   categories: list,
                                   window: int = 20, 
                                   beta: float = 0.7) -> pd.DataFrame:
    """
    Calculate residual-based theme scores using ARMA models.
    
    Args:
        df: DataFrame with price_change and category symbols
        categories: List of theme categories
        window: Rolling window size for ARMA fitting
        beta: Penalty coefficient for inactive themes
        
    Returns:
        pd.DataFrame: DataFrame with added score columns
    """
    df_copy = df.copy()
    residuals = []
    oos_preds = []
    
    print(f"\nCalculating residual scores (beta={beta}, window={window})...")
    
    for i in tqdm(range(window, len(df_copy))):
        train_data = df_copy['price_change'].iloc[i - window : i-1]
        
        try:
            # Fit ARMA model
            model = pm.auto_arima(
                train_data, start_p=0, start_q=0,
                max_p=0, max_q=0,
                d=0, seasonal=False,
                trace=False, error_action='ignore', 
                suppress_warnings=True
            )
            ins_pred = train_data.mean()
            actual = df_copy['price_change'].iloc[i-1]
            residual = actual - ins_pred
            oos_pred = model.predict(n_periods=1).values[0]
            
        except Exception:
            ins_pred = train_data.mean()
            actual = df_copy['price_change'].iloc[i-1]
            residual = actual - ins_pred
            oos_pred = ins_pred

        residuals.append(residual)
        oos_preds.append(oos_pred)
        
    fill_indices = df_copy.index[window:]
    df_copy['residual'] = np.nan
    df_copy['oos_pred'] = np.nan
    df_copy.loc[fill_indices, 'residual'] = residuals
    df_copy.loc[fill_indices, 'oos_pred'] = oos_preds
    
    # Calculate theme scores
    for score_type in categories:
        sym_col = f'{score_type}_sym'
        score_col = f'{score_type}_score'
        
        prev_day_sym_values = df_copy[sym_col].shift(1).loc[fill_indices]
        multiplier = np.where(prev_day_sym_values != 0, prev_day_sym_values, -beta)
        df_copy.loc[fill_indices, score_col] = df_copy.loc[fill_indices, 'residual'] * multiplier
    
    return df_copy


def calculate_max_drawdown(cumulative_returns: pd.Series) -> float:
    """Calculate maximum drawdown from cumulative returns."""
    returns_plus_one = 1 + cumulative_returns
    wealth_index = pd.concat([pd.Series([1.0]), returns_plus_one])
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    return drawdowns.min()


def run_strategy_analysis(df: pd.DataFrame, 
                         categories: list,
                         beta: float, 
                         middle_weight: float, 
                         window: int = 5):
    """
    Run complete news-enhanced momentum strategy analysis.
    
    Args:
        df: Input DataFrame with price and theme data
        categories: List of theme categories
        beta: ARMA residual penalty coefficient
        middle_weight: Weight for middle period in aggregation
        window: Aggregation window size
        
    Returns:
        dict: Strategy performance metrics and processed DataFrame
    """
    # Calculate scores
    df_with_scores = calculate_arma_residual_scores(df, categories, window=window, beta=beta)
    
    cate_scores = [f'{cat}_score' for cat in categories]
    df_processed = df_with_scores[['price_change', 'oos_pred', 'residual'] + cate_scores].copy()
    df_processed.dropna(inplace=True)

    if df_processed.empty:
        return None

    # Calculate rolling weighted average
    weights = np.array([0.2, middle_weight, 1.0])
    weights = weights / np.sum(weights)

    climate = df_processed[cate_scores].rolling(window=len(weights)).apply(
        lambda x: np.sum(x * weights), raw=True
    )
    climate.dropna(inplace=True)
    climate['price_change'] = df_processed['price_change']
    climate['oos_pred'] = df_processed['oos_pred']
    climate['residual'] = df_processed['residual']

    # Generate signals
    climate['dominant_signal_source'] = climate[cate_scores].abs().idxmax(axis=1)
    raw_signal = [row[row['dominant_signal_source']] for _, row in climate.iterrows()]
    climate['raw_signal'] = raw_signal
    
    abs_scores = climate[cate_scores].abs()
    norm_weights = abs_scores.div(abs_scores.sum(axis=1), axis=0)
    climate['weighted_mean'] = (climate[cate_scores] * norm_weights).sum(axis=1)

    # Define position strategies
    positions = {
        'raw_signal': np.sign(climate['raw_signal']),
        'mean_signal': np.sign(climate[cate_scores].mean(axis=1)),
        'momentum_signal': np.sign(climate['oos_pred']),
        'residual_signal': np.sign(climate['residual']),
        'weighted_mean_signal': np.sign(climate['weighted_mean']),
        'long_only': pd.Series(1, index=climate.index),
    }

    # Calculate performance metrics
    sharpe_ratios = {}
    cumulative_returns = {}
    max_drawdowns = {}
    
    RISK_FREE_RATE = 0.05
    TRADING_DAYS = 252

    for name, pos in positions.items():
        daily_returns = pos * climate['price_change']
        
        excess_returns = daily_returns - (RISK_FREE_RATE / TRADING_DAYS)
        mean_excess = excess_returns.mean()
        std_excess = excess_returns.std()
        
        if std_excess != 0:
            annual_sharpe = (mean_excess / std_excess) * np.sqrt(TRADING_DAYS)
        else:
            annual_sharpe = 0.0
        sharpe_ratios[name] = annual_sharpe
        
        cum_ret = (1 + daily_returns).cumprod() - 1
        climate[f'cumulative_{name}_return'] = cum_ret
        cumulative_returns[name] = cum_ret.iloc[-1] if not cum_ret.empty else 0.0
        max_drawdowns[name] = calculate_max_drawdown(cum_ret)

    return {
        "sharpe_ratios": sharpe_ratios,
        "cumulative_returns": cumulative_returns,
        "max_drawdowns": max_drawdowns,
        "climate_df": climate
    }
