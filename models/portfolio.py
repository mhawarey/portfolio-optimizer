# models/portfolio.py - Portfolio data model

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class Portfolio:
    """Portfolio data model for the optimization engine."""
    
    def __init__(self, name="My Portfolio", initial_investment=100000):
        """Initialize a new portfolio."""
        self.name = name
        self.initial_investment = initial_investment
        self.holdings = {}  # Symbol -> Weight mapping
        self.data = {}  # Symbol -> Price data mapping
        self.benchmark = None  # Benchmark data (e.g., S&P 500)
        self.risk_free_rate = 0.035  # 3.5% annual
        self.last_updated = datetime.now()
        
    def add_holding(self, symbol, weight):
        """Add or update a holding in the portfolio."""
        self.holdings[symbol] = weight
        self.last_updated = datetime.now()
        
    def remove_holding(self, symbol):
        """Remove a holding from the portfolio."""
        if symbol in self.holdings:
            del self.holdings[symbol]
            self.last_updated = datetime.now()
            return True
        return False
    
    def get_holdings(self):
        """Get all portfolio holdings."""
        return self.holdings
    
    def get_weights(self):
        """Get the weights of all holdings as a list."""
        return list(self.holdings.values())
    
    def get_symbols(self):
        """Get the symbols of all holdings as a list."""
        return list(self.holdings.keys())
    
    def set_data(self, symbol, price_data):
        """Set price data for a specific symbol."""
        self.data[symbol] = price_data
        
    def get_data(self, symbol):
        """Get price data for a specific symbol."""
        return self.data.get(symbol)
    
    def set_benchmark(self, benchmark_data):
        """Set benchmark data."""
        self.benchmark = benchmark_data
        
    def get_benchmark(self):
        """Get benchmark data."""
        return self.benchmark
    
    def get_total_value(self):
        """Calculate the current total value of the portfolio."""
        # In a real implementation, this would use actual prices
        # Here we just return the initial investment as a placeholder
        return self.initial_investment
    
    def get_returns(self):
        """Calculate historical returns of the portfolio."""
        # This is a simplified placeholder
        # In a real implementation, this would calculate actual returns
        # based on price data and weights
        if not self.data:
            return None
        
        # Create a sample return series (replace with actual calculation)
        dates = pd.date_range(
            end=datetime.now(), 
            periods=252,  # One year of trading days
            freq='B'  # Business days
        )
        
        # Generate random returns with slight upward bias
        returns = np.random.normal(0.0005, 0.01, len(dates))
        return pd.Series(returns, index=dates)
    
    def get_portfolio_statistics(self):
        """Calculate key portfolio statistics."""
        returns = self.get_returns()
        if returns is None:
            return {}
        
        # Calculate annualized return
        annual_return = returns.mean() * 252
        
        # Calculate annualized volatility
        annual_volatility = returns.std() * np.sqrt(252)
        
        # Calculate Sharpe ratio
        sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility
        
        # Calculate max drawdown
        cum_returns = (1 + returns).cumprod()
        running_max = cum_returns.cummax()
        drawdown = (cum_returns / running_max) - 1
        max_drawdown = drawdown.min()
        
        return {
            "return": annual_return,
            "volatility": annual_volatility,
            "sharpe_ratio": sharpe_ratio,
            "max_drawdown": max_drawdown
        }
    
    def to_dict(self):
        """Convert portfolio to dictionary for serialization."""
        return {
            "name": self.name,
            "initial_investment": self.initial_investment,
            "holdings": self.holdings,
            "last_updated": self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a portfolio from a dictionary."""
        portfolio = cls(
            name=data.get("name", "My Portfolio"),
            initial_investment=data.get("initial_investment", 100000)
        )
        
        portfolio.holdings = data.get("holdings", {})
        portfolio.last_updated = datetime.fromisoformat(
            data.get("last_updated", datetime.now().isoformat())
        )
        
        return portfolio