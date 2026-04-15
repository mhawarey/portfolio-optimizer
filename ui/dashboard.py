# ui/dashboard.py - Portfolio dashboard widget

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QSplitter,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MatplotlibCanvas, self).__init__(self.fig)
        self.setParent(parent)
        self.fig.tight_layout()

class PieChartWidget(MatplotlibCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(PieChartWidget, self).__init__(parent, width, height, dpi)
        self.plot_sample_data()
    
    def plot_sample_data(self):
        # Sample allocation data
        labels = ['Technology', 'Financials', 'Healthcare', 'Consumer', 'Energy', 'Other']
        sizes = [30, 20, 15, 15, 10, 10]
        colors = ['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0','#ffb3e6']
        
        self.axes.clear()
        self.axes.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        self.axes.axis('equal')
        self.axes.set_title('Portfolio Sector Allocation')
        self.fig.tight_layout()
        self.draw()

class PerformanceChartWidget(MatplotlibCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        super(PerformanceChartWidget, self).__init__(parent, width, height, dpi)
        self.plot_sample_data()
    
    def plot_sample_data(self):
        # Sample performance data
        dates = list(range(30))  # Last 30 days
        portfolio = np.array([100]) * (1 + np.cumsum(np.random.normal(0.001, 0.01, 30)))
        benchmark = np.array([100]) * (1 + np.cumsum(np.random.normal(0.0005, 0.008, 30)))
        
        self.axes.clear()
        self.axes.plot(dates, portfolio, label='Portfolio', color='#3366ff', linewidth=2)
        self.axes.plot(dates, benchmark, label='S&P 500', color='#ff6633', linewidth=2)
        self.axes.set_title('Portfolio Performance')
        self.axes.set_xlabel('Days')
        self.axes.set_ylabel('Value (normalized)')
        self.axes.legend()
        self.axes.grid(True, linestyle='--', alpha=0.7)
        self.fig.tight_layout()
        self.draw()

class MetricsFrame(QFrame):
    def __init__(self, parent=None):
        super(MetricsFrame, self).__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        
        layout = QGridLayout(self)
        
        # Headers
        metric_header = QLabel("Metric")
        metric_header.setFont(QFont("Arial", 10, QFont.Bold))
        value_header = QLabel("Value")
        value_header.setFont(QFont("Arial", 10, QFont.Bold))
        benchmark_header = QLabel("S&P 500")
        benchmark_header.setFont(QFont("Arial", 10, QFont.Bold))
        
        layout.addWidget(metric_header, 0, 0)
        layout.addWidget(value_header, 0, 1)
        layout.addWidget(benchmark_header, 0, 2)
        
        # Sample metrics
        metrics = [
            ("Return (1Y)", "15.7%", "12.3%"),
            ("Volatility", "14.2%", "13.1%"),
            ("Sharpe Ratio", "1.11", "0.94"),
            ("Max Drawdown", "-8.4%", "-9.7%"),
            ("Alpha", "3.4%", "-"),
            ("Beta", "0.92", "1.00")
        ]
        
        for i, (metric, value, benchmark) in enumerate(metrics, 1):
            metric_label = QLabel(metric)
            value_label = QLabel(value)
            benchmark_label = QLabel(benchmark)
            
            layout.addWidget(metric_label, i, 0)
            layout.addWidget(value_label, i, 1)
            layout.addWidget(benchmark_label, i, 2)

class TopHoldingsTable(QTableWidget):
    def __init__(self, parent=None):
        super(TopHoldingsTable, self).__init__(parent)
        
        # Setup table
        self.setColumnCount(4)
        self.setRowCount(10)
        self.setHorizontalHeaderLabels(["Symbol", "Company", "Weight", "Return"])
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        # Sample data
        sample_data = [
            ("AAPL", "Apple Inc.", "7.8%", "+21.2%"),
            ("MSFT", "Microsoft Corp.", "6.3%", "+26.7%"),
            ("AMZN", "Amazon.com Inc.", "5.1%", "+15.4%"),
            ("GOOGL", "Alphabet Inc.", "4.2%", "+19.8%"),
            ("NVDA", "NVIDIA Corp.", "3.8%", "+112.5%"),
            ("BRK.B", "Berkshire Hathaway", "3.2%", "+8.7%"),
            ("META", "Meta Platforms", "2.9%", "+24.3%"),
            ("TSLA", "Tesla Inc.", "2.5%", "-5.8%"),
            ("JPM", "JPMorgan Chase", "2.3%", "+11.4%"),
            ("V", "Visa Inc.", "2.1%", "+9.8%")
        ]
        
        # Populate table
        for i, (symbol, company, weight, ret) in enumerate(sample_data):
            self.setItem(i, 0, QTableWidgetItem(symbol))
            self.setItem(i, 1, QTableWidgetItem(company))
            self.setItem(i, 2, QTableWidgetItem(weight))
            
            return_item = QTableWidgetItem(ret)
            if ret.startswith("+"):
                return_item.setForeground(QColor(0, 128, 0))  # Green for positive
            elif ret.startswith("-"):
                return_item.setForeground(QColor(255, 0, 0))  # Red for negative
            
            self.setItem(i, 3, return_item)

class DashboardWidget(QWidget):
    def __init__(self, parent=None):
        super(DashboardWidget, self).__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Portfolio Dashboard")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)
        
        # Upper section (charts)
        upper_section = QSplitter(Qt.Horizontal)
        
        # Performance chart
        performance_chart = PerformanceChartWidget(width=6, height=4)
        upper_section.addWidget(performance_chart)
        
        # Allocation chart
        allocation_chart = PieChartWidget(width=5, height=4)
        upper_section.addWidget(allocation_chart)
        
        main_layout.addWidget(upper_section)
        
        # Lower section (metrics and holdings)
        lower_section = QSplitter(Qt.Horizontal)
        
        # Key metrics
        metrics_section = QWidget()
        metrics_layout = QVBoxLayout(metrics_section)
        metrics_label = QLabel("Portfolio Metrics")
        metrics_label.setFont(QFont("Arial", 12, QFont.Bold))
        metrics_layout.addWidget(metrics_label)
        metrics_frame = MetricsFrame()
        metrics_layout.addWidget(metrics_frame)
        lower_section.addWidget(metrics_section)
        
        # Top holdings
        holdings_section = QWidget()
        holdings_layout = QVBoxLayout(holdings_section)
        holdings_label = QLabel("Top Holdings")
        holdings_label.setFont(QFont("Arial", 12, QFont.Bold))
        holdings_layout.addWidget(holdings_label)
        holdings_table = TopHoldingsTable()
        holdings_layout.addWidget(holdings_table)
        lower_section.addWidget(holdings_section)
        
        main_layout.addWidget(lower_section)
        
        # Button section
        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        
        optimize_button = QPushButton("Optimize Portfolio")
        optimize_button.setMinimumHeight(40)
        button_layout.addWidget(optimize_button)
        
        refresh_button = QPushButton("Refresh Data")
        refresh_button.setMinimumHeight(40)
        button_layout.addWidget(refresh_button)
        
        button_layout.addStretch()
        
        main_layout.addWidget(button_section)