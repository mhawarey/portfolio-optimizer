# utils/visualizations.py - Visualization utilities

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

def create_allocation_pie_chart(portfolio, title="Portfolio Allocation"):
    """Create a pie chart of portfolio allocations."""
    holdings = portfolio.get_holdings()
    
    # Get symbols and weights
    symbols = list(holdings.keys())
    weights = list(holdings.values())
    
    # Create figure
    fig = Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        weights, 
        labels=symbols,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 8}
    )
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    ax.set_title(title)
    
    # Create canvas
    canvas = FigureCanvas(fig)
    
    return canvas

def create_sector_allocation_pie_chart(portfolio, stocks, title="Sector Allocation"):
    """Create a pie chart of sector allocations."""
    holdings = portfolio.get_holdings()
    
    # Calculate sector weights
    sector_weights = {}
    for symbol, weight in holdings.items():
        if symbol in stocks:
            sector = stocks[symbol].get_sector()
            if sector in sector_weights:
                sector_weights[sector] += weight
            else:
                sector_weights[sector] = weight
    
    # Get sectors and weights
    sectors = list(sector_weights.keys())
    weights = list(sector_weights.values())
    
    # Create figure
    fig = Figure(figsize=(6, 5), dpi=100)
    ax = fig.add_subplot(111)
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(
        weights, 
        labels=sectors,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 8}
    )
    
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax.axis('equal')
    ax.set_title(title)
    
    # Create canvas
    canvas = FigureCanvas(fig)
    
    return canvas

def create_performance_chart(portfolio, benchmark=None, days=252, title="Portfolio Performance"):
    """Create a performance chart comparing portfolio to benchmark."""
    # Get returns
    portfolio_returns = portfolio.get_returns()
    
    if portfolio_returns is None:
        # Create empty figure with message
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "No return data available", ha='center', va='center', fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        canvas = FigureCanvas(fig)
        return canvas
    
    # Calculate cumulative returns
    portfolio_cum_returns = (1 + portfolio_returns).cumprod()
    
    # Create figure
    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)
    
    # Plot portfolio returns
    ax.plot(portfolio_cum_returns.index, portfolio_cum_returns.values, label="Portfolio")
    
    # Plot benchmark if provided
    if benchmark is not None:
        benchmark_returns = benchmark.get_returns()
        if benchmark_returns is not None:
            # Align dates
            aligned_returns = pd.concat([portfolio_returns, benchmark_returns], axis=1).dropna()
            benchmark_cum_returns = (1 + aligned_returns.iloc[:, 1]).cumprod()
            ax.plot(aligned_returns.index, benchmark_cum_returns.values, label="Benchmark")
    
    # Configure plot
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Create canvas
    canvas = FigureCanvas(fig)
    
    return canvas

def create_efficient_frontier_chart(optimizer, current_portfolio=None, optimal_portfolio=None, points=50, title="Efficient Frontier"):
    """Create an efficient frontier chart."""
    # Generate efficient frontier points
    frontier = optimizer.get_efficient_frontier(points)
    
    if not frontier:
        # Create empty figure with message
        fig = Figure(figsize=(8, 5), dpi=100)
        ax = fig.add_subplot(111)
        ax.text(0.5, 0.5, "Could not calculate efficient frontier", ha='center', va='center', fontsize=12)
        ax.set_xticks([])
        ax.set_yticks([])
        canvas = FigureCanvas(fig)
        return canvas
    
    # Extract risk and return values
    risks = [point['risk'] for point in frontier]
    returns = [point['return'] for point in frontier]
    
    # Create figure
    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)
    
    # Plot efficient frontier
    ax.plot(risks, returns, 'b-', linewidth=2)
    
    # Plot current portfolio if provided
    if current_portfolio is not None:
        stats = current_portfolio.get_portfolio_statistics()
        if stats:
            ax.plot(stats['volatility'], stats['return'], 'ro', markersize=10)
            ax.annotate('Current', 
                        xy=(stats['volatility'], stats['return']),
                        xytext=(10, 10), textcoords='offset points',
                        ha='center')
    
    # Plot optimal portfolio if provided
    if optimal_portfolio is not None:
        ax.plot(optimal_portfolio['risk'], optimal_portfolio['return'], 'go', markersize=10)
        ax.annotate('Optimal', 
                    xy=(optimal_portfolio['risk'], optimal_portfolio['return']),
                    xytext=(10, 10), textcoords='offset points',
                    ha='center')
    
    # Configure plot
    ax.set_title(title)
    ax.set_xlabel("Risk (Volatility)")
    ax.set_ylabel("Expected Return")
    ax.grid(True)
    
    # Create canvas
    canvas = FigureCanvas(fig)
    
    return canvas

def create_allocation_comparison_chart(current_weights, optimized_weights, title="Allocation Comparison"):
    """Create a bar chart comparing current and optimized allocations."""
    # Get common symbols
    common_symbols = sorted(set(current_weights.keys()).union(set(optimized_weights.keys())))
    
    # Create arrays for plotting
    current = [current_weights.get(symbol, 0) for symbol in common_symbols]
    optimized = [optimized_weights.get(symbol, 0) for symbol in common_symbols]
    
    # Create figure
    fig = Figure(figsize=(10, 6), dpi=100)
    ax = fig.add_subplot(111)
    
    # Set up bar chart
    x = np.arange(len(common_symbols))
    width = 0.35
    
    # Create bars
    ax.bar(x - width/2, current, width, label='Current')
    ax.bar(x + width/2, optimized, width, label='Optimized')
    
    # Configure plot
    ax.set_title(title)
    ax.set_ylabel('Weight')
    ax.set_xticks(x)
    ax.set_xticklabels(common_symbols, rotation=45, ha='right')
    ax.legend()
    
    # Adjust layout
    fig.tight_layout()
    
    # Create canvas
    canvas = FigureCanvas(fig)
    
    return canvas

def create_projection_chart(current_portfolio, optimized_portfolio, months=12, title="Projected Performance"):
    """Create a performance projection chart."""
    # Create figure
    fig = Figure(figsize=(8, 5), dpi=100)
    ax = fig.add_subplot(111)
    
    # Get statistics
    current_stats = current_portfolio.get_portfolio_statistics()
    
    # Create time points
    months_array = np.arange(months + 1)
    
    # Simulate current portfolio
    if current_stats:
        current_return = current_stats['return'] / 12  # Monthly return
        current_risk = current_stats['volatility'] / np.sqrt(12)  # Monthly volatility
        
        # Generate random paths
        np.random.seed(42)  # For reproducibility
        current_paths = np.zeros((100, months + 1))
        current_paths[:, 0] = 100  # Start at 100
        
        for i in range(100):
            monthly_returns = np.random.normal(current_return, current_risk, months)
            current_paths[i, 1:] = 100 * np.cumprod(1 + monthly_returns)
        
        # Calculate mean and confidence intervals
        current_mean = np.mean(current_paths, axis=0)
        current_lower = np.percentile(current_paths, 10, axis=0)
        current_upper = np.percentile(current_paths, 90, axis=0)
        
        # Plot current portfolio projection
        ax.plot(months_array, current_mean, 'b-', label='Current Portfolio', linewidth=2)
        ax.fill_between(months_array, current_lower, current_upper, color='b', alpha=0.2)
    
    # Simulate optimized portfolio
    if optimized_portfolio:
        opt_return = optimized_portfolio['return'] / 12  # Monthly return
        opt_risk = optimized_portfolio['risk'] / np.sqrt(12)  # Monthly volatility
        
        # Generate random paths
        np.random.seed(43)  # Different seed
        opt_paths = np.zeros((100, months + 1))
        opt_paths[:, 0] = 100  # Start at 100
        
        for i in range(100):
            monthly_returns = np.random.normal(opt_return, opt_risk, months)
            opt_paths[i, 1:] = 100 * np.cumprod(1 + monthly_returns)
        
        # Calculate mean and confidence intervals
        opt_mean = np.mean(opt_paths, axis=0)
        opt_lower = np.percentile(opt_paths, 10, axis=0)
        opt_upper = np.percentile(opt_paths, 90, axis=0)
        
        # Plot optimized portfolio projection
        ax.plot(months_array, opt_mean, 'g-', label='Optimized Portfolio', linewidth=2)
        ax.fill_between(months_array, opt_lower, opt_upper, color='g', alpha=0.2)
    
    # Configure plot
    ax.set_title(title)
    ax.set_xlabel("Months")
    ax.set_ylabel("Portfolio Value")
    ax.legend()
    ax.grid(True)
    
    # Add vertical line at current time
    ax.axvline(x=0, color='black', linestyle='--')
    ax.text(0.1, 102, 'Current', rotation=90)
    
    # Create canvas
    canvas = FigureCanvas(fig)
    
    return canvas