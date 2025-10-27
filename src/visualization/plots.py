import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_cumulative_returns(strategies_df: pd.DataFrame, 
                           title: str = "Cumulative Returns Comparison"):
    """
    Plot cumulative returns for multiple strategies.
    
    Args:
        strategies_df: DataFrame with cumulative return columns
        title: Plot title
    """
    fig, ax = plt.subplots(figsize=(14, 7))
    
    for col in strategies_df.columns:
        if col.startswith('cumulative_'):
            label = col.replace('cumulative_', '').replace('_', ' ').title()
            ax.plot(strategies_df.index, strategies_df[col], label=label, linewidth=2)
    
    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Cumulative Return', fontsize=12)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def plot_theme_analysis(climate_df: pd.DataFrame, categories: list):
    """
    Create interactive theme score analysis plot.
    
    Args:
        climate_df: DataFrame with theme scores
        categories: List of category names
        
    Returns:
        plotly.graph_objects.Figure
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Price Change', 'Theme Scores')
    )
    
    # Price change
    fig.add_trace(go.Scatter(
        x=climate_df.index,
        y=climate_df['price_change'],
        mode='lines',
        name='Price Change',
        line=dict(color='navy')
    ), row=1, col=1)
    
    # Theme scores
    colors = ['red', 'blue', 'green', 'orange']
    for cat, color in zip(categories, colors):
        score_col = f'{cat}_score'
        if score_col in climate_df.columns:
            fig.add_trace(go.Scatter(
                x=climate_df.index,
                y=climate_df[score_col],
                mode='lines',
                name=cat.capitalize(),
                line=dict(color=color)
            ), row=2, col=1)
    
    fig.update_layout(
        height=600,
        title_text='Theme Score Analysis',
        hovermode='x unified'
    )
    
    return fig


def generate_interactive_report(df_reason, climate_df, output_path='interactive_report.html'):
    """
    Generate comprehensive interactive HTML report.
    
    Args:
        df_reason: DataFrame with news drivers
        climate_df: DataFrame with theme scores
        output_path: Path to save HTML file
    """
    # Prepare data
    df_reason_ = df_reason.copy()
    climate_df_ = climate_df.copy()
    df_reason_.reset_index(inplace=True)
    climate_df_.reset_index(inplace=True)
    
    merged_df = pd.merge(df_reason_, climate_df_, on='date', how='inner')
    merged_df.set_index('date', inplace=True)
    merged_df.sort_index(inplace=True)
    
    if 'price_change_x' in merged_df.columns:
        merged_df.rename(columns={'price_change_x': 'price_change'}, inplace=True)
    
    merged_df['cumulative_price_change'] = (1 + merged_df['price_change']).cumprod()
    
    # Create hover text
    merged_df['hover_text'] = (
        '<b>Date</b>: ' + merged_df.index.strftime('%Y-%m-%d') + '<br>' +
        '<b>Price Change</b>: ' + merged_df['price_change'].apply(lambda x: f'{x:.2%}') + '<br>' +
        '<b>Key Drivers</b>: ' + merged_df['key drivers'].fillna('N/A') + '<br>' +
        '<b>Reverse Factors</b>: ' + merged_df['reverse factors'].fillna('N/A')
    )
    
    # Create figure
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=(
            "Cumulative Price with Thematic Drivers",
            "Daily Price Change vs. Signal",
            "Theme Scores"
        )
    )
    
    # Plot 1: Cumulative returns
    fig.add_trace(go.Scatter(
        x=merged_df.index,
        y=merged_df['cumulative_price_change'],
        mode='lines',
        name='Cumulative Price',
        hovertext=merged_df['hover_text'],
        hoverinfo='text',
        line=dict(color='navy', width=2)
    ), row=1, col=1)
    
    # Plot 2: Price change vs signal
    fig.add_trace(go.Bar(
        x=merged_df.index,
        y=merged_df['price_change'],
        name='Price Change',
        marker_color='lightsalmon'
    ), row=2, col=1)
    
    if 'raw_signal' in merged_df.columns:
        fig.add_trace(go.Bar(
            x=merged_df.index,
            y=merged_df['raw_signal'],
            name='Raw Signal',
            marker_color='steelblue'
        ), row=2, col=1)
    
    # Plot 3: Theme scores
    score_colors = {
        'currency_score': 'green',
        'demand_score': 'blue',
        'supply_score': 'red',
        'geopolitics_score': 'orange'
    }
    
    for score, color in score_colors.items():
        if score in merged_df.columns:
            fig.add_trace(go.Scatter(
                x=merged_df.index,
                y=merged_df[score],
                mode='lines',
                name=score.replace('_', ' ').title(),
                line=dict(color=color, width=2)
            ), row=3, col=1)
    
    fig.update_layout(
        height=900,
        title_text='Interactive Commodity Analysis Report',
        title_x=0.5,
        hovermode='x unified',
        barmode='overlay'
    )
    
    fig.update_yaxes(title_text="Cumulative Return", row=1, col=1)
    fig.update_yaxes(title_text="Value", row=2, col=1)
    fig.update_yaxes(title_text="Score", row=3, col=1)
    fig.update_xaxes(title_text="Date", row=3, col=1)
    
    # Save to file
    html_report = fig.to_html(full_html=True, include_plotlyjs='cdn')
    with open(output_path, 'w') as f:
        f.write(html_report)
    
    print(f"Report saved to {output_path}")
    return fig
