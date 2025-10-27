import numpy as np
import pandas as pd


def simulate_event_series(num_days_total: int = 252, 
                          lookback_period: int = 5, 
                          initial_weights: list = None,
                          annual_volatility: float = 0.2, 
                          trading_days_per_year: int = 252,
                          prob_mixture_c: float = 0.1,
                          mean_reversion_beta: float = 0.4):
    """
    Simulate a multi-theme event-driven price series.
    
    Args:
        num_days_total: Total simulation days
        lookback_period: Days for moving average calculation
        initial_weights: Weights for weighted average (None = linear)
        annual_volatility: Annual volatility for random shocks
        trading_days_per_year: Trading days per year
        prob_mixture_c: Random probability mixing coefficient (0-1)
        mean_reversion_beta: Mean reversion factor for inactive themes
        
    Returns:
        pd.DataFrame: Simulated data with theme scores and realizations
    """
    num_events = 3
    daily_std = annual_volatility / np.sqrt(trading_days_per_year)
    
    # Initialize history
    data_history = [
        np.random.normal(0, daily_std, size=num_events) 
        for _ in range(lookback_period)
    ]
    score_means = [[0] * num_events for _ in range(lookback_period)]
    
    # Setup weights
    if initial_weights is None:
        weights = np.arange(1, lookback_period + 1)
    else:
        weights = np.array(initial_weights)
        if len(weights) != lookback_period:
            raise ValueError("Length of initial_weights must equal lookback_period")
            
    weights = weights / np.sum(weights)
    weights = weights.reshape(-1, 1)
    
    realization_history = [0] * lookback_period

    # Simulation loop
    for _ in range(lookback_period, num_days_total):
        recent_data = np.array(data_history[-lookback_period:])
        current_mean = np.sum(weights * recent_data, axis=0)
        score_means.append(current_mean)
        
        abs_mean = np.abs(current_mean)
        sum_abs_mean = np.sum(abs_mean)

        if sum_abs_mean > 1e-9:
            event_probabilities = abs_mean / sum_abs_mean
        else:
            event_probabilities = np.ones(num_events) / num_events
            
        # Mix with random probability
        random_prob = np.ones(num_events) / num_events
        event_probabilities = ((1 - prob_mixture_c) * event_probabilities + 
                              prob_mixture_c * random_prob)
        
        # Select event and generate increment
        next_event_idx = np.random.choice(np.arange(num_events), p=event_probabilities)
        new_increment = np.random.normal(current_mean[next_event_idx], daily_std)
        realization_history.append(new_increment)
        
        # Apply mean reversion to inactive themes
        new_day_data = np.ones(num_events) * (-mean_reversion_beta) * new_increment
        new_day_data[next_event_idx] = new_increment
        
        data_history.append(new_day_data)
    
    # Compile results
    data = pd.DataFrame(data_history)
    data['realization'] = pd.Series(realization_history, index=data.index)
    data = pd.concat([
        data, 
        pd.DataFrame(score_means, columns=['Ascore', 'Bscore', 'Cscore'])
    ], axis=1)
    
    return data
