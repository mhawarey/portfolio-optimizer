# ui/universe.py - Stock universe management widget

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QLineEdit,
                             QComboBox, QCheckBox, QGroupBox, QScrollArea,
                             QSplitter)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QColor, QIcon

class StockFilterWidget(QWidget):
    def __init__(self, parent=None):
        super(StockFilterWidget, self).__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Search section
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter symbol or company name...")
        search_layout.addWidget(self.search_input)
        main_layout.addLayout(search_layout)
        
        # Sector filter
        sector_layout = QHBoxLayout()
        sector_layout.addWidget(QLabel("Sector:"))
        self.sector_combo = QComboBox()
        self.sector_combo.addItem("All Sectors")
        self.sector_combo.addItems([
            "Technology", "Financials", "Healthcare", "Consumer Discretionary",
            "Consumer Staples", "Industrials", "Energy", "Utilities",
            "Materials", "Real Estate", "Communication Services"
        ])
        sector_layout.addWidget(self.sector_combo)
        main_layout.addLayout(sector_layout)
        
        # Filters group
        filters_group = QGroupBox("Fundamental Filters")
        filters_layout = QGridLayout(filters_group)
        
        # Market cap filter
        filters_layout.addWidget(QLabel("Market Cap:"), 0, 0)
        self.market_cap_combo = QComboBox()
        self.market_cap_combo.addItems([
            "Any", "Mega (>$200B)", "Large (>$10B)", "Mid (>$2B)",
            "Small (>$300M)", "Micro (<$300M)"
        ])
        filters_layout.addWidget(self.market_cap_combo, 0, 1)
        
        # P/E filter
        filters_layout.addWidget(QLabel("P/E Ratio:"), 1, 0)
        self.pe_combo = QComboBox()
        self.pe_combo.addItems([
            "Any", "Low (<10)", "Medium (10-20)", "High (20-50)", "Very High (>50)", "Negative"
        ])
        filters_layout.addWidget(self.pe_combo, 1, 1)
        
        # Dividend filter
        filters_layout.addWidget(QLabel("Dividend Yield:"), 2, 0)
        self.dividend_combo = QComboBox()
        self.dividend_combo.addItems([
            "Any", "None (0%)", "Low (0-1%)", "Medium (1-3%)", "High (3-5%)", "Very High (>5%)"
        ])
        filters_layout.addWidget(self.dividend_combo, 2, 1)
        
        # Beta filter
        filters_layout.addWidget(QLabel("Beta:"), 3, 0)
        self.beta_combo = QComboBox()
        self.beta_combo.addItems([
            "Any", "Defensive (<0.5)", "Low (0.5-1.0)", "Market (1.0)", 
            "High (1.0-1.5)", "Aggressive (>1.5)"
        ])
        filters_layout.addWidget(self.beta_combo, 3, 1)
        
        main_layout.addWidget(filters_group)
        
        # Liquidity filter
        liquidity_group = QGroupBox("Liquidity Filter")
        liquidity_layout = QGridLayout(liquidity_group)
        
        liquidity_layout.addWidget(QLabel("Min. Daily Volume ($):"), 0, 0)
        self.min_volume_combo = QComboBox()
        self.min_volume_combo.addItems([
            "Any", "> $1M", "> $5M", "> $10M", "> $50M", "> $100M"
        ])
        liquidity_layout.addWidget(self.min_volume_combo, 0, 1)
        
        liquidity_layout.addWidget(QLabel("Min. Shares Float:"), 1, 0)
        self.min_float_combo = QComboBox()
        self.min_float_combo.addItems([
            "Any", "> 10M", "> 50M", "> 100M", "> 500M", "> 1B"
        ])
        liquidity_layout.addWidget(self.min_float_combo, 1, 1)
        
        main_layout.addWidget(liquidity_group)
        
        # Custom filters section
        custom_group = QGroupBox("Custom Filters")
        custom_layout = QVBoxLayout(custom_group)
        
        self.include_sp500 = QCheckBox("S&P 500 Components Only")
        self.include_sp500.setChecked(True)
        custom_layout.addWidget(self.include_sp500)
        
        self.exclude_financials = QCheckBox("Exclude Financial Statements with Warnings")
        custom_layout.addWidget(self.exclude_financials)
        
        self.exclude_low_liquidity = QCheckBox("Exclude Low Liquidity Stocks")
        self.exclude_low_liquidity.setChecked(True)
        custom_layout.addWidget(self.exclude_low_liquidity)
        
        main_layout.addWidget(custom_group)
        
        # Button
        apply_button = QPushButton("Apply Filters")
        apply_button.setMinimumHeight(40)
        main_layout.addWidget(apply_button)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()

class StockUniverseTable(QTableWidget):
    def __init__(self, parent=None):
        super(StockUniverseTable, self).__init__(parent)
        
        # Setup table
        self.setColumnCount(8)
        self.setRowCount(50)  # Show top 50 stocks
        self.setHorizontalHeaderLabels([
            "Symbol", "Company", "Sector", "Market Cap", 
            "P/E", "Dividend", "Beta", "Include"
        ])
        
        # Set column stretch behavior
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        # Sample data for S&P 500 stocks (just a subset for demonstration)
        sample_data = [
            ("AAPL", "Apple Inc.", "Technology", "$2.84T", "30.1", "0.5%", "1.2", True),
            ("MSFT", "Microsoft Corp.", "Technology", "$2.76T", "35.6", "0.7%", "0.9", True),
            ("AMZN", "Amazon.com Inc.", "Consumer Discretionary", "$1.86T", "69.5", "0%", "1.3", True),
            ("GOOGL", "Alphabet Inc.", "Communication Services", "$1.75T", "25.7", "0%", "1.1", True),
            ("META", "Meta Platforms Inc.", "Communication Services", "$1.10T", "28.4", "0%", "1.4", True),
            ("NVDA", "NVIDIA Corp.", "Technology", "$2.30T", "73.2", "0.03%", "1.7", True),
            ("BRK.B", "Berkshire Hathaway", "Financials", "$860B", "17.2", "0%", "0.8", True),
            ("TSLA", "Tesla Inc.", "Consumer Discretionary", "$720B", "72.3", "0%", "2.0", True),
            ("JPM", "JPMorgan Chase", "Financials", "$540B", "12.1", "2.3%", "1.1", True),
            ("V", "Visa Inc.", "Financials", "$510B", "30.5", "0.7%", "0.9", True),
            ("PG", "Procter & Gamble", "Consumer Staples", "$370B", "26.8", "2.4%", "0.4", True),
            ("UNH", "UnitedHealth Group", "Healthcare", "$455B", "21.7", "1.3%", "0.7", True),
            ("XOM", "Exxon Mobil Corp.", "Energy", "$480B", "12.9", "3.2%", "1.1", True),
            ("JNJ", "Johnson & Johnson", "Healthcare", "$410B", "17.8", "3.0%", "0.6", True),
            ("MA", "Mastercard Inc.", "Financials", "$420B", "34.5", "0.6%", "1.0", True),
            ("HD", "Home Depot Inc.", "Consumer Discretionary", "$350B", "23.1", "2.3%", "1.0", True),
            ("AVGO", "Broadcom Inc.", "Technology", "$410B", "27.5", "1.9%", "1.2", True),
            ("PFE", "Pfizer Inc.", "Healthcare", "$170B", "14.2", "5.2%", "0.7", True),
            ("CSCO", "Cisco Systems", "Technology", "$210B", "15.8", "2.9%", "0.9", True),
            ("ORCL", "Oracle Corp.", "Technology", "$320B", "40.2", "1.4%", "1.2", True)
        ]
        
        # Populate table
        for i, (symbol, company, sector, market_cap, pe, dividend, beta, include) in enumerate(sample_data):
            self.setItem(i, 0, QTableWidgetItem(symbol))
            self.setItem(i, 1, QTableWidgetItem(company))
            self.setItem(i, 2, QTableWidgetItem(sector))
            self.setItem(i, 3, QTableWidgetItem(market_cap))
            
            pe_item = QTableWidgetItem(pe)
            if float(pe.replace(',', '')) > 30:
                pe_item.setForeground(QColor(255, 120, 0))  # Orange for high P/E
            self.setItem(i, 4, pe_item)
            
            self.setItem(i, 5, QTableWidgetItem(dividend))
            self.setItem(i, 6, QTableWidgetItem(beta))
            
            # Checkbox for including in optimization
            include_checkbox = QTableWidgetItem()
            include_checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
            include_checkbox.setCheckState(Qt.Checked if include else Qt.Unchecked)
            self.setItem(i, 7, include_checkbox)

class UniverseWidget(QWidget):
    def __init__(self, parent=None):
        super(UniverseWidget, self).__init__(parent)
        
        # Main layout
        main_layout = QHBoxLayout(self)
        
        # Create a splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)
        
        # Left side - Filters
        filter_widget = QWidget()
        filter_layout = QVBoxLayout(filter_widget)
        
        filter_title = QLabel("Stock Filters")
        filter_title.setFont(QFont("Arial", 14, QFont.Bold))
        filter_layout.addWidget(filter_title)
        
        filter_scroll = QScrollArea()
        filter_scroll.setWidgetResizable(True)
        filter_scroll.setWidget(StockFilterWidget())
        filter_layout.addWidget(filter_scroll)
        
        splitter.addWidget(filter_widget)
        
        # Right side - Stock Table
        table_widget = QWidget()
        table_layout = QVBoxLayout(table_widget)
        
        table_header = QWidget()
        table_header_layout = QHBoxLayout(table_header)
        
        universe_title = QLabel("Investment Universe")
        universe_title.setFont(QFont("Arial", 14, QFont.Bold))
        table_header_layout.addWidget(universe_title)
        
        stock_count = QLabel("Showing 20 of 505 stocks")
        table_header_layout.addWidget(stock_count)
        
        table_header_layout.addStretch()
        
        select_all = QPushButton("Select All")
        table_header_layout.addWidget(select_all)
        
        clear_all = QPushButton("Clear All")
        table_header_layout.addWidget(clear_all)
        
        table_layout.addWidget(table_header)
        
        # Stock table
        stock_table = StockUniverseTable()
        table_layout.addWidget(stock_table)
        
        # Controls below table
        table_controls = QWidget()
        table_controls_layout = QHBoxLayout(table_controls)
        
        table_controls_layout.addWidget(QLabel("Selected: 20 stocks"))
        
        table_controls_layout.addStretch()
        
        add_custom = QPushButton("Add Custom Stock")
        table_controls_layout.addWidget(add_custom)
        
        apply_button = QPushButton("Apply to Optimization")
        apply_button.setMinimumHeight(40)
        table_controls_layout.addWidget(apply_button)
        
        table_layout.addWidget(table_controls)
        
        splitter.addWidget(table_widget)
        
        # Set initial sizes
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)