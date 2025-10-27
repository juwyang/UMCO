"""
Trading strategy implementations
"""
from .momentum import naive_momentum_strategy, slope_momentum_strategy
from .news_momentum import calculate_arma_residual_scores, run_strategy_analysis
from .simulation import simulate_event_series

__all__ = [
    'naive_momentum_strategy',
    'slope_momentum_strategy', 
    'calculate_arma_residual_scores',
    'run_strategy_analysis',
    'simulate_event_series'
]
