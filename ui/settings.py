# ui/settings.py - Settings and configuration widget

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QTabWidget, 
                             QLineEdit, QComboBox, QSpinBox, QGroupBox,
                             QCheckBox, QRadioButton, QFileDialog, QSpacerItem,
                             QSizePolicy, QDoubleSpinBox, QDateEdit)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont

class DataSourceSettings(QWidget):
    def __init__(self, parent=None):
        super(DataSourceSettings, self).__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Data provider settings
        provider_group = QGroupBox("Data Provider")
        provider_layout = QGridLayout(provider_group)
        
        provider_layout.addWidget(QLabel("Primary Data Source:"), 0, 0)
        self.data_source = QComboBox()
        self.data_source.addItems(["Yahoo Finance", "Alpha Vantage", "Local CSV Files"])
        provider_layout.addWidget(self.data_source, 0, 1)
        
        provider_layout.addWidget(QLabel("API Key:"), 1, 0)
        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("Enter API key if required...")
        self.api_key.setEchoMode(QLineEdit.Password)
        provider_layout.addWidget(self.api_key, 1, 1)
        
        provider_layout.addWidget(QLabel("Backup Source:"), 2, 0)
        self.backup_source = QComboBox()
        self.backup_source.addItems(["None", "Yahoo Finance", "Alpha Vantage", "Local CSV Files"])
        provider_layout.addWidget(self.backup_source, 2, 1)
        
        main_layout.addWidget(provider_group)
        
        # Data options
        data_group = QGroupBox("Data Collection Options")
        data_layout = QGridLayout(data_group)
        
        data_layout.addWidget(QLabel("Historical Period:"), 0, 0)
        self.period = QComboBox()
        self.period.addItems(["1 Year", "2 Years", "3 Years", "5 Years", "10 Years", "Max Available"])
        self.period.setCurrentIndex(0)  # 1 Year default
        data_layout.addWidget(self.period, 0, 1)
        
        data_layout.addWidget(QLabel("Data Frequency:"), 1, 0)
        self.frequency = QComboBox()
        self.frequency.addItems(["Daily", "Weekly", "Monthly"])
        self.frequency.setCurrentIndex(0)  # Daily default
        data_layout.addWidget(self.frequency, 1, 1)
        
        data_layout.addWidget(QLabel("Include Dividends:"), 2, 0)
        self.include_dividends = QCheckBox()
        self.include_dividends.setChecked(True)
        data_layout.addWidget(self.include_dividends, 2, 1)
        
        data_layout.addWidget(QLabel("Include Splits:"), 3, 0)
        self.include_splits = QCheckBox()
        self.include_splits.setChecked(True)
        data_layout.addWidget(self.include_splits, 3, 1)
        
        data_layout.addWidget(QLabel("Adjust for Inflation:"), 4, 0)
        self.adjust_inflation = QCheckBox()
        data_layout.addWidget(self.adjust_inflation, 4, 1)
        
        main_layout.addWidget(data_group)
        
        # Cache settings
        cache_group = QGroupBox("Local Cache Settings")
        cache_layout = QGridLayout(cache_group)
        
        cache_layout.addWidget(QLabel("Cache Directory:"), 0, 0)
        cache_path_widget = QWidget()
        cache_path_layout = QHBoxLayout(cache_path_widget)
        cache_path_layout.setContentsMargins(0, 0, 0, 0)
        
        self.cache_path = QLineEdit()
        self.cache_path.setText("C:/PortfolioOptimizer/cache")
        cache_path_layout.addWidget(self.cache_path)
        
        browse_button = QPushButton("Browse...")
        cache_path_layout.addWidget(browse_button)
        
        cache_layout.addWidget(cache_path_widget, 0, 1)
        
        cache_layout.addWidget(QLabel("Maximum Cache Size:"), 1, 0)
        self.max_cache = QSpinBox()
        self.max_cache.setRange(100, 10000)
        self.max_cache.setValue(1000)
        self.max_cache.setSuffix(" MB")
        cache_layout.addWidget(self.max_cache, 1, 1)
        
        cache_layout.addWidget(QLabel("Cache Expiry:"), 2, 0)
        self.cache_expiry = QSpinBox()
        self.cache_expiry.setRange(1, 90)
        self.cache_expiry.setValue(7)
        self.cache_expiry.setSuffix(" days")
        cache_layout.addWidget(self.cache_expiry, 2, 1)
        
        clear_cache_button = QPushButton("Clear Cache")
        cache_layout.addWidget(clear_cache_button, 3, 1)
        
        main_layout.addWidget(cache_group)
        
        # Button section
        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        
        test_connection = QPushButton("Test Connection")
        button_layout.addWidget(test_connection)
        
        button_layout.addStretch()
        
        save_button = QPushButton("Save Settings")
        save_button.setMinimumWidth(120)
        button_layout.addWidget(save_button)
        
        main_layout.addWidget(button_section)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()

class OptimizationSettings(QWidget):
    def __init__(self, parent=None):
        super(OptimizationSettings, self).__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Optimization engine settings
        engine_group = QGroupBox("Optimization Engine")
        engine_layout = QGridLayout(engine_group)
        
        engine_layout.addWidget(QLabel("Optimization Algorithm:"), 0, 0)
        self.algorithm = QComboBox()
        self.algorithm.addItems([
            "Mean-Variance Optimization",
            "Black-Litterman Model",
            "Risk Parity",
            "Hierarchical Risk Parity",
            "Robust Optimization"
        ])
        engine_layout.addWidget(self.algorithm, 0, 1)
        
        engine_layout.addWidget(QLabel("Risk-Free Rate (%):"), 1, 0)
        self.risk_free_rate = QDoubleSpinBox()
        self.risk_free_rate.setRange(0, 10)
        self.risk_free_rate.setSingleStep(0.1)
        self.risk_free_rate.setValue(3.5)
        engine_layout.addWidget(self.risk_free_rate, 1, 1)
        
        engine_layout.addWidget(QLabel("Maximum Iterations:"), 2, 0)
        self.max_iterations = QSpinBox()
        self.max_iterations.setRange(1000, 100000)
        self.max_iterations.setSingleStep(1000)
        self.max_iterations.setValue(10000)
        engine_layout.addWidget(self.max_iterations, 2, 1)
        
        engine_layout.addWidget(QLabel("Convergence Tolerance:"), 3, 0)
        self.tolerance = QDoubleSpinBox()
        self.tolerance.setRange(0.00001, 0.01)
        self.tolerance.setSingleStep(0.0001)
        self.tolerance.setValue(0.0001)
        self.tolerance.setDecimals(5)
        engine_layout.addWidget(self.tolerance, 3, 1)
        
        main_layout.addWidget(engine_group)
        
        # Covariance estimation
        covariance_group = QGroupBox("Covariance Estimation")
        covariance_layout = QGridLayout(covariance_group)
        
        covariance_layout.addWidget(QLabel("Covariance Method:"), 0, 0)
        self.covariance_method = QComboBox()
        self.covariance_method.addItems([
            "Sample Covariance",
            "Exponentially Weighted",
            "Shrinkage Estimation",
            "Ledoit-Wolf Shrinkage",
            "Factor Model"
        ])
        covariance_layout.addWidget(self.covariance_method, 0, 1)
        
        covariance_layout.addWidget(QLabel("Lookback Period:"), 1, 0)
        self.lookback_period = QSpinBox()
        self.lookback_period.setRange(30, 1000)
        self.lookback_period.setSingleStep(30)
        self.lookback_period.setValue(252)
        self.lookback_period.setSuffix(" days")
        covariance_layout.addWidget(self.lookback_period, 1, 1)
        
        covariance_layout.addWidget(QLabel("Half-Life (EWMA):"), 2, 0)
        self.half_life = QSpinBox()
        self.half_life.setRange(10, 500)
        self.half_life.setValue(90)
        self.half_life.setSuffix(" days")
        covariance_layout.addWidget(self.half_life, 2, 1)
        
        main_layout.addWidget(covariance_group)
        
        # Backtesting settings
        backtest_group = QGroupBox("Backtesting Configuration")
        backtest_layout = QGridLayout(backtest_group)
        
        backtest_layout.addWidget(QLabel("Start Date:"), 0, 0)
        self.backtest_start = QDateEdit()
        self.backtest_start.setDate(QDate(2024, 4, 1))
        self.backtest_start.setCalendarPopup(True)
        backtest_layout.addWidget(self.backtest_start, 0, 1)
        
        backtest_layout.addWidget(QLabel("End Date:"), 1, 0)
        self.backtest_end = QDateEdit()
        self.backtest_end.setDate(QDate(2025, 4, 1))
        self.backtest_end.setCalendarPopup(True)
        backtest_layout.addWidget(self.backtest_end, 1, 1)
        
        backtest_layout.addWidget(QLabel("Rebalancing Frequency:"), 2, 0)
        self.rebalance_freq = QComboBox()
        self.rebalance_freq.addItems([
            "Monthly", "Quarterly", "Semi-Annually", "Annually"
        ])
        self.rebalance_freq.setCurrentIndex(1)  # Quarterly by default
        backtest_layout.addWidget(self.rebalance_freq, 2, 1)
        
        backtest_layout.addWidget(QLabel("Transaction Cost (%):"), 3, 0)
        self.transaction_cost = QDoubleSpinBox()
        self.transaction_cost.setRange(0, 1)
        self.transaction_cost.setSingleStep(0.01)
        self.transaction_cost.setValue(0.1)
        backtest_layout.addWidget(self.transaction_cost, 3, 1)
        
        main_layout.addWidget(backtest_group)
        
        # Button section
        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        
        reset_defaults = QPushButton("Reset to Defaults")
        button_layout.addWidget(reset_defaults)
        
        button_layout.addStretch()
        
        save_button = QPushButton("Save Settings")
        save_button.setMinimumWidth(120)
        button_layout.addWidget(save_button)
        
        main_layout.addWidget(button_section)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()

class GeneralSettings(QWidget):
    def __init__(self, parent=None):
        super(GeneralSettings, self).__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Application settings
        app_group = QGroupBox("Application Settings")
        app_layout = QGridLayout(app_group)
        
        app_layout.addWidget(QLabel("Theme:"), 0, 0)
        self.theme = QComboBox()
        self.theme.addItems(["Light", "Dark", "System Default"])
        app_layout.addWidget(self.theme, 0, 1)
        
        app_layout.addWidget(QLabel("Chart Style:"), 1, 0)
        self.chart_style = QComboBox()
        self.chart_style.addItems(["Classic", "Modern", "Financial", "Minimal"])
        app_layout.addWidget(self.chart_style, 1, 1)
        
        app_layout.addWidget(QLabel("Date Format:"), 2, 0)
        self.date_format = QComboBox()
        self.date_format.addItems(["MM/DD/YYYY", "DD/MM/YYYY", "YYYY-MM-DD"])
        app_layout.addWidget(self.date_format, 2, 1)
        
        app_layout.addWidget(QLabel("Number Format:"), 3, 0)
        self.number_format = QComboBox()
        self.number_format.addItems(["1,234.56", "1 234,56", "1234.56"])
        app_layout.addWidget(self.number_format, 3, 1)
        
        self.auto_save = QCheckBox("Auto-save portfolios")
        self.auto_save.setChecked(True)
        app_layout.addWidget(self.auto_save, 4, 0, 1, 2)
        
        self.auto_update = QCheckBox("Check for updates on startup")
        self.auto_update.setChecked(True)
        app_layout.addWidget(self.auto_update, 5, 0, 1, 2)
        
        main_layout.addWidget(app_group)
        
        # Portfolio settings
        portfolio_group = QGroupBox("Default Portfolio Settings")
        portfolio_layout = QGridLayout(portfolio_group)
        
        portfolio_layout.addWidget(QLabel("Default Portfolio Name:"), 0, 0)
        self.default_name = QLineEdit("My Portfolio")
        portfolio_layout.addWidget(self.default_name, 0, 1)
        
        portfolio_layout.addWidget(QLabel("Portfolio Currency:"), 1, 0)
        self.currency = QComboBox()
        self.currency.addItems(["USD", "EUR", "GBP", "JPY", "CAD", "AUD"])
        portfolio_layout.addWidget(self.currency, 1, 1)
        
        portfolio_layout.addWidget(QLabel("Initial Investment:"), 2, 0)
        self.initial_investment = QSpinBox()
        self.initial_investment.setRange(1000, 10000000)
        self.initial_investment.setSingleStep(10000)
        self.initial_investment.setValue(100000)
        self.initial_investment.setPrefix("$ ")
        portfolio_layout.addWidget(self.initial_investment, 2, 1)
        
        portfolio_layout.addWidget(QLabel("Benchmark Index:"), 3, 0)
        self.benchmark = QComboBox()
        self.benchmark.addItems(["S&P 500", "Dow Jones", "NASDAQ", "Russell 2000", "Custom..."])
        portfolio_layout.addWidget(self.benchmark, 3, 1)
        
        main_layout.addWidget(portfolio_group)
        
        # File locations
        files_group = QGroupBox("File Locations")
        files_layout = QGridLayout(files_group)
        
        files_layout.addWidget(QLabel("Default Save Location:"), 0, 0)
        save_path_widget = QWidget()
        save_path_layout = QHBoxLayout(save_path_widget)
        save_path_layout.setContentsMargins(0, 0, 0, 0)
        
        self.save_path = QLineEdit()
        self.save_path.setText("C:/PortfolioOptimizer/portfolios")
        save_path_layout.addWidget(self.save_path)
        
        browse_button = QPushButton("Browse...")
        save_path_layout.addWidget(browse_button)
        
        files_layout.addWidget(save_path_widget, 0, 1)
        
        files_layout.addWidget(QLabel("Export Format:"), 1, 0)
        self.export_format = QComboBox()
        self.export_format.addItems(["CSV", "Excel", "JSON", "PDF"])
        files_layout.addWidget(self.export_format, 1, 1)
        
        main_layout.addWidget(files_group)
        
        # Button section
        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        
        reset_defaults = QPushButton("Reset to Defaults")
        button_layout.addWidget(reset_defaults)
        
        button_layout.addStretch()
        
        save_button = QPushButton("Save Settings")
        save_button.setMinimumWidth(120)
        button_layout.addWidget(save_button)
        
        main_layout.addWidget(button_section)
        
        # Add stretch to push everything to the top
        main_layout.addStretch()

class SettingsWidget(QWidget):
    def __init__(self, parent=None):
        super(SettingsWidget, self).__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Settings")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)
        
        # Create tabs
        tabs = QTabWidget()
        
        # General settings tab
        general_tab = GeneralSettings()
        tabs.addTab(general_tab, "General")
        
        # Data source settings tab
        data_tab = DataSourceSettings()
        tabs.addTab(data_tab, "Data Sources")
        
        # Optimization settings tab
        optimization_tab = OptimizationSettings()
        tabs.addTab(optimization_tab, "Optimization")
        
        main_layout.addWidget(tabs)
        
        # Bottom buttons
        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        
        button_layout.addStretch()
        
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(cancel_button)
        
        apply_button = QPushButton("Apply")
        button_layout.addWidget(apply_button)
        
        ok_button = QPushButton("OK")
        ok_button.setDefault(True)
        button_layout.addWidget(ok_button)
        
        main_layout.addWidget(button_section)