# Source Code Structure

This directory contains the core implementation of the commodity news momentum research project.

## Modules

### `data_processing/`
- `load_data.py`: Load and merge price and classification data
- `price_data.py`: Price data specific processing
- `classification_data.py`: News classification and theme extraction

### `strategies/`
- `momentum.py`: Traditional momentum strategies (naive and slope-based)
- `news_momentum.py`: News-enhanced momentum using ARMA residuals
- `simulation.py`: Event-driven price simulation framework

### `analysis/`
- `statistics.py`: Statistical calculations and descriptive stats
- `performance.py`: Performance metrics (Sharpe, drawdown, etc.)

### `visualization/`
- `plots.py`: Plotting functions for analysis and reports

### `utils/`
- `config.py`: Configuration management and API key handling

## Usage Example

```python
from src.data_processing import load_and_prepare_data
from src.strategies import run_strategy_analysis
from src.visualization import generate_interactive_report

# Load data
df = load_and_prepare_data(
    price_csv_path='data/price/crude_oil.csv',
    classification_csv_path='data/price/2024_combined_price_movement.csv',
    commodity_name='Crude'
)

# Run analysis
categories = ['currency', 'demand', 'supply', 'geopolitics']
results = run_strategy_analysis(
    df, 
    categories=categories,
    beta=0.8, 
    middle_weight=0.2
)

# Generate report
generate_interactive_report(df, results['climate_df'])
```

## Configuration

Create a `config.yml` file in the project root (copy from `config.example.yml`) to customize settings.

## API Keys

Set API keys as environment variables:
```bash
export OPENAI_API_KEY="your-key-here"
export ANTHROPIC_API_KEY="your-key-here"
```

Never commit actual API keys to the repository!
