# utils/data_loader.py - Demo data loading utilities

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

from models.stock import Stock
from models.portfolio import Portfolio

class DataLoader:
    """Utility class for loading demo data."""
    
    @staticmethod
    def load_demo_sp500_symbols():
        """Load a list of S&P 500 symbols (top companies only for demo)."""
        symbols = [
            # Technology
            "AAPL", "MSFT", "GOOGL", "GOOG", "META", "NVDA", "AVGO", "CSCO", "ORCL", "ADBE",
            "INTC", "IBM", "AMD", "CRM", "ACN", "TXN", "QCOM", "PYPL", "ADP", "AMAT",
            
            # Financials
            "BRK.B", "JPM", "V", "MA", "BAC", "WFC", "GS", "MS", "SCHW", "BLK",
            "C", "AXP", "SPGI", "CME", "ICE", "CB", "PNC", "TFC", "USB", "MMC",
            
            # Healthcare
            "UNH", "JNJ", "LLY", "PFE", "ABBV", "MRK", "TMO", "ABT", "DHR", "BMY",
            "AMGN", "CVS", "ISRG", "CI", "MDT", "ELV", "VRTX", "GILD", "SYK", "ZTS",
            
            # Consumer Discretionary
            "AMZN", "TSLA", "HD", "MCD", "NKE", "LOW", "SBUX", "TJX", "BKNG", "MAR",
            "GRMN", "CMG", "EBAY", "BBY", "DG", "DLTR", "ROST", "ORLY", "AZO", "YUM",
            
            # Consumer Staples
            "PG", "KO", "PEP", "COST", "WMT", "PM", "MO", "EL", "CL", "GIS",
            "KR", "KMB", "CLX", "SYY", "STZ", "HSY", "K", "CAG", "TAP", "HRL",
            
            # Industrials
            "LMT", "RTX", "HON", "UPS", "BA", "CAT", "DE", "GE", "MMM", "UNP",
            "FDX", "GD", "NOC", "CSX", "ETN", "ITW", "EMR", "WM", "NSC", "ROP",
            
            # Energy
            "XOM", "CVX", "COP", "SLB", "EOG", "PSX", "MPC", "VLO", "OXY", "DVN",
            "KMI", "WMB", "HES", "HAL", "BKR", "OKE", "FANG", "EQT", "CTRA", "MRO",
            
            # Utilities
            "NEE", "DUK", "SO", "D", "AEP", "SRE", "XEL", "ED", "EXC", "PCG",
            "WEC", "ES", "AWK", "AES", "CEG", "ETR", "CMS", "PEG", "DTE", "FE",
            
            # Real Estate
            "AMT", "EQIX", "PSA", "PLD", "CCI", "O", "WY", "SPG", "VICI", "WELL",
            "EXR", "AVB", "DLR", "EQR", "MAA", "SBAC", "UDR", "IRM", "ESS", "KIM",
            
            # Materials
            "LIN", "APD", "SHW", "ECL", "CRH", "FCX", "NEM", "NUE", "ALB", "CTVA",
            "DOW", "DD", "PPG", "VMC", "MLM", "CF", "EMN", "FMC", "IP", "AVY",
            
            # Communication Services
            "CMCSA", "NFLX", "T", "VZ", "CHTR", "ATVI", "EA", "TMUS", "LUMN", "OMC",
            "DISH", "PARA", "WBD", "FOXA", "FOX", "IPG", "LYV", "NWS", "NWSA", "TTWO"
        ]
        
        return symbols
    
    @staticmethod
    def load_demo_sector_map():
        """Load a mapping of symbols to sectors for demo."""
        sectors = {
            # Technology
            "AAPL": "Technology", "MSFT": "Technology", "GOOGL": "Technology", 
            "GOOG": "Technology", "META": "Technology", "NVDA": "Technology", 
            "AVGO": "Technology", "CSCO": "Technology", "ORCL": "Technology", 
            "ADBE": "Technology", "INTC": "Technology", "IBM": "Technology", 
            "AMD": "Technology", "CRM": "Technology", "ACN": "Technology", 
            "TXN": "Technology", "QCOM": "Technology", "PYPL": "Technology", 
            "ADP": "Technology", "AMAT": "Technology",
            
            # Financials
            "BRK.B": "Financials", "JPM": "Financials", "V": "Financials", 
            "MA": "Financials", "BAC": "Financials", "WFC": "Financials", 
            "GS": "Financials", "MS": "Financials", "SCHW": "Financials", 
            "BLK": "Financials", "C": "Financials", "AXP": "Financials", 
            "SPGI": "Financials", "CME": "Financials", "ICE": "Financials", 
            "CB": "Financials", "PNC": "Financials", "TFC": "Financials", 
            "USB": "Financials", "MMC": "Financials",
            
            # Healthcare
            "UNH": "Healthcare", "JNJ": "Healthcare", "LLY": "Healthcare", 
            "PFE": "Healthcare", "ABBV": "Healthcare", "MRK": "Healthcare", 
            "TMO": "Healthcare", "ABT": "Healthcare", "DHR": "Healthcare", 
            "BMY": "Healthcare", "AMGN": "Healthcare", "CVS": "Healthcare", 
            "ISRG": "Healthcare", "CI": "Healthcare", "MDT": "Healthcare", 
            "ELV": "Healthcare", "VRTX": "Healthcare", "GILD": "Healthcare", 
            "SYK": "Healthcare", "ZTS": "Healthcare",
            
            # Consumer Discretionary
            "AMZN": "Consumer Discretionary", "TSLA": "Consumer Discretionary", 
            "HD": "Consumer Discretionary", "MCD": "Consumer Discretionary", 
            "NKE": "Consumer Discretionary", "LOW": "Consumer Discretionary", 
            "SBUX": "Consumer Discretionary", "TJX": "Consumer Discretionary", 
            "BKNG": "Consumer Discretionary", "MAR": "Consumer Discretionary", 
            "GRMN": "Consumer Discretionary", "CMG": "Consumer Discretionary", 
            "EBAY": "Consumer Discretionary", "BBY": "Consumer Discretionary", 
            "DG": "Consumer Discretionary", "DLTR": "Consumer Discretionary", 
            "ROST": "Consumer Discretionary", "ORLY": "Consumer Discretionary", 
            "AZO": "Consumer Discretionary", "YUM": "Consumer Discretionary",
            
            # Consumer Staples
            "PG": "Consumer Staples", "KO": "Consumer Staples", 
            "PEP": "Consumer Staples", "COST": "Consumer Staples", 
            "WMT": "Consumer Staples", "PM": "Consumer Staples", 
            "MO": "Consumer Staples", "EL": "Consumer Staples", 
            "CL": "Consumer Staples", "GIS": "Consumer Staples", 
            "KR": "Consumer Staples", "KMB": "Consumer Staples", 
            "CLX": "Consumer Staples", "SYY": "Consumer Staples", 
            "STZ": "Consumer Staples", "HSY": "Consumer Staples", 
            "K": "Consumer Staples", "CAG": "Consumer Staples", 
            "TAP": "Consumer Staples", "HRL": "Consumer Staples",
            
            # Industrials
            "LMT": "Industrials", "RTX": "Industrials", "HON": "Industrials", 
            "UPS": "Industrials", "BA": "Industrials", "CAT": "Industrials", 
            "DE": "Industrials", "GE": "Industrials", "MMM": "Industrials", 
            "UNP": "Industrials", "FDX": "Industrials", "GD": "Industrials", 
            "NOC": "Industrials", "CSX": "Industrials", "ETN": "Industrials", 
            "ITW": "Industrials", "EMR": "Industrials", "WM": "Industrials", 
            "NSC": "Industrials", "ROP": "Industrials",
            
            # Energy
            "XOM": "Energy", "CVX": "Energy", "COP": "Energy", 
            "SLB": "Energy", "EOG": "Energy", "PSX": "Energy", 
            "MPC": "Energy", "VLO": "Energy", "OXY": "Energy", 
            "DVN": "Energy", "KMI": "Energy", "WMB": "Energy", 
            "HES": "Energy", "HAL": "Energy", "BKR": "Energy", 
            "OKE": "ONEOK Inc.", "FANG": "Diamondback Energy", "EQT": "EQT Corp.",
            "CTRA": "Coterra Energy", "MRO": "Marathon Oil",
            
            # Utilities
            "NEE": "NextEra Energy", "DUK": "Duke Energy", "SO": "Southern Co.",
            "D": "Dominion Energy", "AEP": "American Electric Power", "SRE": "Sempra",
            "XEL": "Xcel Energy", "ED": "Consolidated Edison", "EXC": "Exelon Corp.",
            "PCG": "PG&E Corp.", "WEC": "WEC Energy Group", "ES": "Eversource Energy",
            "AWK": "American Water Works", "AES": "AES Corp.", "CEG": "Constellation Energy",
            "ETR": "Entergy Corp.", "CMS": "CMS Energy", "PEG": "Public Service Enterprise Group",
            "DTE": "DTE Energy", "FE": "FirstEnergy Corp."
        }
        
        return names
    
    @staticmethod
    def generate_sample_price_data(symbol, days=252, start_date=None):
        """Generate sample price data for a stock."""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)
            
        # Parameters for the random walk
        drift = np.random.normal(0.0005, 0.0002)  # Slight upward bias
        volatility = np.random.uniform(0.010, 0.025)  # Different volatility for each stock
        
        # Generate daily returns
        daily_returns = np.random.normal(drift, volatility, days)
        
        # Generate cumulative returns
        cumulative_returns = np.cumprod(1 + daily_returns)
        
        # Set starting price between $10 and $500
        starting_price = np.random.uniform(10, 500)
        
        # Generate price series
        prices = starting_price * cumulative_returns
        
        # Generate dates
        dates = [start_date + timedelta(days=i) for i in range(days)]
        
        # Generate volume
        avg_volume = np.random.uniform(500000, 10000000)
        volume = np.random.normal(avg_volume, avg_volume * 0.2, days)
        volume = np.maximum(volume, 100000)  # Ensure minimum volume
        
        # Create DataFrame
        df = pd.DataFrame({
            'open': prices * np.random.uniform(0.99, 1.01, days),
            'high': prices * np.random.uniform(1.01, 1.03, days),
            'low': prices * np.random.uniform(0.97, 0.99, days),
            'close': prices,
            'volume': volume.astype(int)
        }, index=dates)
        
        return df
    
    @staticmethod
    def generate_sample_fundamentals(symbol, sector):
        """Generate sample fundamental data for a stock."""
        # Market cap ($ billions)
        if sector == "Technology":
            market_cap = np.random.uniform(50, 2500)
        elif sector in ["Financials", "Healthcare"]:
            market_cap = np.random.uniform(20, 700)
        else:
            market_cap = np.random.uniform(10, 300)
            
        # P/E ratio
        if sector == "Technology":
            pe_ratio = np.random.uniform(15, 80)
        elif sector == "Utilities":
            pe_ratio = np.random.uniform(10, 25)
        else:
            pe_ratio = np.random.uniform(12, 40)
            
        # Dividend yield
        if sector in ["Utilities", "Consumer Staples", "Energy"]:
            dividend_yield = np.random.uniform(0.02, 0.05)
        elif sector in ["Technology", "Consumer Discretionary"]:
            dividend_yield = np.random.uniform(0, 0.015)
        else:
            dividend_yield = np.random.uniform(0.005, 0.03)
            
        # Beta
        if sector in ["Utilities", "Consumer Staples"]:
            beta = np.random.uniform(0.3, 0.9)
        elif sector in ["Technology", "Consumer Discretionary"]:
            beta = np.random.uniform(0.9, 1.8)
        else:
            beta = np.random.uniform(0.7, 1.3)
            
        # Average daily volume
        avg_daily_volume = int(np.random.uniform(500000, 20000000))
        
        # Generate other financial metrics
        return {
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "dividend_yield": dividend_yield,
            "beta": beta,
            "avg_daily_volume": avg_daily_volume,
            "price_to_book": np.random.uniform(1, 10),
            "price_to_sales": np.random.uniform(1, 20),
            "debt_to_equity": np.random.uniform(0.1, 2),
            "roe": np.random.uniform(0.05, 0.3),
            "profit_margin": np.random.uniform(0.05, 0.4),
            "revenue_growth": np.random.uniform(-0.1, 0.4)
        }
    
    @staticmethod
    def load_demo_stocks(num_stocks=50):
        """Load demo stock data for a subset of S&P 500 stocks."""
        # Get symbols, sectors, and names
        all_symbols = DataLoader.load_demo_sp500_symbols()
        sectors = DataLoader.load_demo_sector_map()
        names = DataLoader.load_demo_company_names()
        
        # Randomly select a subset of symbols if requested
        if num_stocks < len(all_symbols):
            selected_symbols = random.sample(all_symbols, num_stocks)
        else:
            selected_symbols = all_symbols
            
        # Create stock objects
        stocks = {}
        for symbol in selected_symbols:
            # Create stock
            stock = Stock(symbol, names.get(symbol, symbol))
            
            # Set sector
            sector = sectors.get(symbol, "Other")
            stock.set_sector(sector)
            
            # Generate price data
            price_data = DataLoader.generate_sample_price_data(symbol)
            stock.set_price_data(price_data)
            
            # Generate fundamentals
            fundamentals = DataLoader.generate_sample_fundamentals(symbol, sector)
            stock.set_fundamentals(fundamentals)
            
            # Add to dictionary
            stocks[symbol] = stock
            
        return stocks
    
    @staticmethod
    def load_demo_portfolio():
        """Load a demo portfolio."""
        # Create a portfolio
        portfolio = Portfolio("Demo Portfolio", 1000000)
        
        # Add some holdings
        holdings = {
            "AAPL": 0.08,
            "MSFT": 0.07,
            "AMZN": 0.06,
            "GOOGL": 0.05,
            "META": 0.05,
            "JNJ": 0.04,
            "V": 0.04,
            "PG": 0.04,
            "JPM": 0.04,
            "UNH": 0.04,
            "HD": 0.03,
            "NVDA": 0.03,
            "MA": 0.03,
            "BAC": 0.03,
            "DIS": 0.03,
            "CRM": 0.03,
            "CSCO": 0.03,
            "VZ": 0.03,
            "ADBE": 0.03,
            "PFE": 0.03,
            "KO": 0.03,
            "WMT": 0.03,
            "PEP": 0.03,
            "ABT": 0.03,
            "MRK": 0.03
        }
        
        for symbol, weight in holdings.items():
            portfolio.add_holding(symbol, weight)
            
        return portfolio
    
    @staticmethod
    def generate_covariance_matrix(returns, annualize=True):
        """Generate a covariance matrix from returns."""
        # Calculate the covariance matrix
        cov_matrix = returns.cov()
        
        # Annualize if requested
        if annualize:
            cov_matrix = cov_matrix * 252
            
        return cov_matrix
    
    @staticmethod
    def generate_expected_returns(returns, method="mean", risk_free_rate=0.035):
        """Generate expected returns from historical returns."""
        if method == "mean":
            # Use historical means
            exp_returns = returns.mean() * 252  # Annualize
        elif method == "capm":
            # Use CAPM
            # This is a simplified implementation
            market_return = returns.mean().mean() * 252
            market_premium = market_return - risk_free_rate
            
            betas = {}
            for col in returns.columns:
                # Calculate beta for each asset
                beta = returns[col].cov(returns.mean(axis=1)) / returns.mean(axis=1).var()
                betas[col] = beta
                
            exp_returns = pd.Series({
                symbol: risk_free_rate + beta * market_premium
                for symbol, beta in betas.items()
            })
        else:
            raise ValueError(f"Unknown method: {method}")
            
        return exp_returnsEnergy", "FANG": "Energy", "EQT": "Energy", 
            "CTRA": "Energy", "MRO": "Energy",
            
            # Utilities
            "NEE": "Utilities", "DUK": "Utilities", "SO": "Utilities", 
            "D": "Utilities", "AEP": "Utilities", "SRE": "Utilities", 
            "XEL": "Utilities", "ED": "Utilities", "EXC": "Utilities", 
            "PCG": "Utilities", "WEC": "Utilities", "ES": "Utilities", 
            "AWK": "Utilities", "AES": "Utilities", "CEG": "Utilities", 
            "ETR": "Utilities", "CMS": "Utilities", "PEG": "Utilities", 
            "DTE": "Utilities", "FE": "Utilities",
            
            # Real Estate
            "AMT": "Real Estate", "EQIX": "Real Estate", "PSA": "Real Estate", 
            "PLD": "Real Estate", "CCI": "Real Estate", "O": "Real Estate", 
            "WY": "Real Estate", "SPG": "Real Estate", "VICI": "Real Estate", 
            "WELL": "Real Estate", "EXR": "Real Estate", "AVB": "Real Estate", 
            "DLR": "Real Estate", "EQR": "Real Estate", "MAA": "Real Estate", 
            "SBAC": "Real Estate", "UDR": "Real Estate", "IRM": "Real Estate", 
            "ESS": "Real Estate", "KIM": "Real Estate",
            
            # Materials
            "LIN": "Materials", "APD": "Materials", "SHW": "Materials", 
            "ECL": "Materials", "CRH": "Materials", "FCX": "Materials", 
            "NEM": "Materials", "NUE": "Materials", "ALB": "Materials", 
            "CTVA": "Materials", "DOW": "Materials", "DD": "Materials", 
            "PPG": "Materials", "VMC": "Materials", "MLM": "Materials", 
            "CF": "Materials", "EMN": "Materials", "FMC": "Materials", 
            "IP": "Materials", "AVY": "Materials",
            
            # Communication Services
            "CMCSA": "Communication Services", "NFLX": "Communication Services", 
            "T": "Communication Services", "VZ": "Communication Services", 
            "CHTR": "Communication Services", "ATVI": "Communication Services", 
            "EA": "Communication Services", "TMUS": "Communication Services", 
            "LUMN": "Communication Services", "OMC": "Communication Services", 
            "DISH": "Communication Services", "PARA": "Communication Services", 
            "WBD": "Communication Services", "FOXA": "Communication Services", 
            "FOX": "Communication Services", "IPG": "Communication Services", 
            "LYV": "Communication Services", "NWS": "Communication Services", 
            "NWSA": "Communication Services", "TTWO": "Communication Services"
        }
        
        return sectors
    
    @staticmethod
    def load_demo_company_names():
        """Load a mapping of symbols to company names for demo."""
        names = {
            "AAPL": "Apple Inc.", "MSFT": "Microsoft Corp.", "GOOGL": "Alphabet Inc. Class A",
            "GOOG": "Alphabet Inc. Class C", "META": "Meta Platforms Inc.", "NVDA": "NVIDIA Corp.",
            "AVGO": "Broadcom Inc.", "CSCO": "Cisco Systems Inc.", "ORCL": "Oracle Corp.",
            "ADBE": "Adobe Inc.", "INTC": "Intel Corp.", "IBM": "International Business Machines",
            "AMD": "Advanced Micro Devices", "CRM": "Salesforce Inc.", "ACN": "Accenture PLC",
            "TXN": "Texas Instruments", "QCOM": "Qualcomm Inc.", "PYPL": "PayPal Holdings",
            "ADP": "Automatic Data Processing", "AMAT": "Applied Materials",
            
            "BRK.B": "Berkshire Hathaway", "JPM": "JPMorgan Chase & Co.", "V": "Visa Inc.",
            "MA": "Mastercard Inc.", "BAC": "Bank of America Corp.", "WFC": "Wells Fargo & Co.",
            "GS": "Goldman Sachs Group", "MS": "Morgan Stanley", "SCHW": "Charles Schwab Corp.",
            "BLK": "BlackRock Inc.", "C": "Citigroup Inc.", "AXP": "American Express Co.",
            "SPGI": "S&P Global Inc.", "CME": "CME Group Inc.", "ICE": "Intercontinental Exchange",
            "CB": "Chubb Ltd.", "PNC": "PNC Financial Services", "TFC": "Truist Financial Corp.",
            "USB": "U.S. Bancorp", "MMC": "Marsh & McLennan",
            
            "UNH": "UnitedHealth Group", "JNJ": "Johnson & Johnson", "LLY": "Eli Lilly & Co.",
            "PFE": "Pfizer Inc.", "ABBV": "AbbVie Inc.", "MRK": "Merck & Co.",
            "TMO": "Thermo Fisher Scientific", "ABT": "Abbott Laboratories", "DHR": "Danaher Corp.",
            "BMY": "Bristol-Myers Squibb", "AMGN": "Amgen Inc.", "CVS": "CVS Health Corp.",
            "ISRG": "Intuitive Surgical", "CI": "Cigna Group", "MDT": "Medtronic PLC",
            "ELV": "Elevance Health", "VRTX": "Vertex Pharmaceuticals", "GILD": "Gilead Sciences",
            "SYK": "Stryker Corp.", "ZTS": "Zoetis Inc.",
            
            "AMZN": "Amazon.com Inc.", "TSLA": "Tesla Inc.", "HD": "Home Depot Inc.",
            "MCD": "McDonald's Corp.", "NKE": "Nike Inc.", "LOW": "Lowe's Cos.",
            "SBUX": "Starbucks Corp.", "TJX": "TJX Companies", "BKNG": "Booking Holdings",
            "MAR": "Marriott International", "GRMN": "Garmin Ltd.", "CMG": "Chipotle Mexican Grill",
            "EBAY": "eBay Inc.", "BBY": "Best Buy Co.", "DG": "Dollar General Corp.",
            "DLTR": "Dollar Tree Inc.", "ROST": "Ross Stores", "ORLY": "O'Reilly Automotive",
            "AZO": "AutoZone Inc.", "YUM": "Yum! Brands",
            
            "PG": "Procter & Gamble", "KO": "Coca-Cola Co.", "PEP": "PepsiCo Inc.",
            "COST": "Costco Wholesale", "WMT": "Walmart Inc.", "PM": "Philip Morris International",
            "MO": "Altria Group", "EL": "Estee Lauder", "CL": "Colgate-Palmolive",
            "GIS": "General Mills", "KR": "Kroger Co.", "KMB": "Kimberly-Clark",
            "CLX": "Clorox Co.", "SYY": "Sysco Corp.", "STZ": "Constellation Brands",
            "HSY": "Hershey Co.", "K": "Kellogg Co.", "CAG": "Conagra Brands",
            "TAP": "Molson Coors Beverage", "HRL": "Hormel Foods",
            
            "LMT": "Lockheed Martin", "RTX": "RTX Corp.", "HON": "Honeywell International",
            "UPS": "United Parcel Service", "BA": "Boeing Co.", "CAT": "Caterpillar Inc.",
            "DE": "Deere & Co.", "GE": "General Electric", "MMM": "3M Co.",
            "UNP": "Union Pacific", "FDX": "FedEx Corp.", "GD": "General Dynamics",
            "NOC": "Northrop Grumman", "CSX": "CSX Corp.", "ETN": "Eaton Corp. PLC",
            "ITW": "Illinois Tool Works", "EMR": "Emerson Electric", "WM": "Waste Management",
            "NSC": "Norfolk Southern", "ROP": "Roper Technologies",
            
            "XOM": "Exxon Mobil Corp.", "CVX": "Chevron Corp.", "COP": "ConocoPhillips",
            "SLB": "SLB", "EOG": "EOG Resources", "PSX": "Phillips 66",
            "MPC": "Marathon Petroleum", "VLO": "Valero Energy", "OXY": "Occidental Petroleum",
            "DVN": "Devon Energy", "KMI": "Kinder Morgan", "WMB": "Williams Cos.",
            "HES": "Hess Corp.", "HAL": "Halliburton Co.", "BKR": "Baker Hughes",
            "OKE": "