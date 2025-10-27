import os
from pathlib import Path


def get_project_root():
    """Get the project root directory."""
    return Path(__file__).parent.parent.parent


def get_data_paths():
    """
    Get common data file paths.
    
    Returns:
        dict: Dictionary of data paths
    """
    root = get_project_root()
    data_dir = root / 'data'
    
    return {
        'price_dir': data_dir / 'price',
        'output_dir': root / 'outputs',
        'reports_dir': root / 'docs' / 'reports',
        'figures_dir': root / 'outputs' / 'figures'
    }


def load_config(config_file='config.yml'):
    """
    Load configuration from YAML file.
    
    Args:
        config_file: Path to config file
        
    Returns:
        dict: Configuration dictionary
    """
    # Default configuration
    default_config = {
        'data': {
            'commodity_name': 'Crude',
            'trading_days_per_year': 252,
            'categories': ['currency', 'demand', 'supply', 'geopolitics']
        },
        'strategy': {
            'lookback_naive': 75,
            'lookback_slope': 5,
            'arma_window': 20,
            'beta': 0.8,
            'middle_weight': 0.2
        },
        'risk': {
            'risk_free_rate': 0.05
        }
    }
    
    # Try to load from file if it exists
    config_path = get_project_root() / config_file
    if config_path.exists():
        try:
            import yaml
            with open(config_path, 'r') as f:
                file_config = yaml.safe_load(f)
            # Merge with defaults
            default_config.update(file_config)
        except ImportError:
            print("PyYAML not installed. Using default config.")
        except Exception as e:
            print(f"Error loading config: {e}. Using default config.")
    
    return default_config


# API key management (never commit actual keys!)
def get_api_key(service_name):
    """
    Get API key from environment variable.
    
    Args:
        service_name: Name of the service (e.g., 'OPENAI', 'ANTHROPIC')
        
    Returns:
        str: API key or None
    """
    key_name = f'{service_name.upper()}_API_KEY'
    return os.getenv(key_name)
