# models/stock.py - Stock data model

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

class Stock:
    """Stock data model."""
    
    def __init__(self, symbol, name=None):
        """Initialize a new stock."""
        self.symbol = symbol
        self.name = name if name else symbol
        self.price_data = None
        self.fundamentals = {}
        self.sector = None
        self.industry = None
        self.last_updated = None
        
    def set_price_data(self, price_data):
        """Set the historical price data for the stock."""
        self.price_data = price_data
        self.last_updated = datetime.now()
        
    def get_price_data(self):
        """Get the historical price data for the stock."""
        return self.price_data
    
    def get_returns(self, period='daily'):
        """Calculate returns over the specified period."""
        if self.price_data is None:
            return None
            
        if 'close' not in self.price_data.columns:
            return None
            
        # Calculate returns based on close prices
        if period == 'daily':
            return self.price_data['close'].pct_change().dropna()
        elif period == 'weekly':
            return self.price_data['close'].resample('W').last().pct_change().dropna()
        elif period == 'monthly':
            return self.price_data['close'].resample('M').last().pct_change().dropna()
        else:
            raise ValueError(f"Invalid period: {period}")
    
    def set_fundamentals(self, fundamentals):
        """Set fundamental data for the stock."""
        self.fundamentals = fundamentals
        
    def get_fundamentals(self):
        """Get fundamental data for the stock."""
        return self.fundamentals
    
    def set_sector(self, sector):
        """Set the sector for the stock."""
        self.sector = sector
        
    def get_sector(self):
        """Get the sector for the stock."""
        return self.sector
    
    def set_industry(self, industry):
        """Set the industry for the stock."""
        self.industry = industry
        
    def get_industry(self):
        """Get the industry for the stock."""
        return self.industry
    
    def get_current_price(self):
        """Get the most recent price for the stock."""
        if self.price_data is None or len(self.price_data) == 0:
            return None
            
        if 'close' not in self.price_data.columns:
            return None
            
        return self.price_data['close'].iloc[-1]
    
    def get_liquidity_metrics(self):
        """Calculate liquidity metrics for the stock."""
        if self.price_data is None or len(self.price_data) == 0:
            return {}
            
        if 'volume' not in self.price_data.columns or 'close' not in self.price_data.columns:
            return {}
            
        # Calculate average daily volume (last 30 days)
        avg_volume = self.price_data['volume'].tail(30).mean()
        
        # Calculate dollar volume
        last_price = self.price_data['close'].iloc[-1]
        avg_dollar_volume = avg_volume * last_price
        
        # Calculate volume volatility
        volume_volatility = self.price_data['volume'].tail(30).std() / avg_volume
        
        return {
            'avg_volume': avg_volume,
            'avg_dollar_volume': avg_dollar_volume,
            'volume_volatility': volume_volatility
        }
    
    def get_volatility(self, days=252):
        """Calculate annualized volatility."""
        returns = self.get_returns()
        if returns is None or len(returns) == 0:
            return None
            
        # Calculate annualized volatility using daily returns
        return returns.tail(days).std() * np.sqrt(252)
    
    def get_beta(self, market_returns, days=252):
        """Calculate beta relative to the provided market returns."""
        stock_returns = self.get_returns()
        if stock_returns is None or len(stock_returns) == 0:
            return None
            
        # Align stock returns with market returns
        aligned_returns = pd.concat([stock_returns, market_returns], axis=1).dropna()
        
        if len(aligned_returns) < 30:  # Require at least 30 data points
            return None
            
        # Use the most recent data points
        aligned_returns = aligned_returns.tail(days)
        
        # Calculate covariance and variance
        covariance = aligned_returns.iloc[:, 0].cov(aligned_returns.iloc[:, 1])
        market_variance = aligned_returns.iloc[:, 1].var()
        
        # Calculate beta
        if market_variance == 0:
            return None
            
        return covariance / market_variance
    
    def to_dict(self):
        """Convert stock to dictionary for serialization."""
        return {
            "symbol": self.symbol,
            "name": self.name,
            "sector": self.sector,
            "industry": self.industry,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None,
            "current_price": self.get_current_price(),
            "volatility": self.get_volatility()
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a stock from a dictionary."""
        stock = cls(
            symbol=data.get("symbol"),
            name=data.get("name")
        )
        
        stock.sector = data.get("sector")
        stock.industry = data.get("industry")
        
        if data.get("last_updated"):
            stock.last_updated = datetime.fromisoformat(data.get("last_updated"))
        
        return stock