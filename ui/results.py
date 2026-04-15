# ui/results.py - Results visualization widget

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QTableWidget, 
                             QTableWidgetItem, QHeaderView, QSplitter, 
                             QGroupBox, QTabWidget, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class AllocationComparisonChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(AllocationComparisonChart, self).__init__(self.fig)
        self.setParent(parent)
        self.plot_allocations()
        
    def plot_allocations(self):
        # Sample data
        categories = ['Tech', 'Financials', 'Healthcare', 'Consumer', 'Energy', 'Industrials', 'Utilities', 'Materials']
        current_allocation = [30, 20, 15, 15, 10, 5, 3, 2]
        optimized_allocation = [35, 15, 20, 10, 5, 10, 3, 2]
        
        x = np.arange(len(categories))
        width = 0.35
        
        self.axes.clear()
        self.axes.bar(x - width/2, current_allocation, width, label='Current')
        self.axes.bar(x + width/2, optimized_allocation, width, label='Optimized')
        
        self.axes.set_xticks(x)
        self.axes.set_xticklabels(categories, rotation=45, ha='right')
        self.axes.set_ylabel('Allocation (%)')
        self.axes.set_title('Portfolio Allocation Comparison')
        self.axes.legend()
        
        self.fig.tight_layout()
        self.draw()

class PerformanceProjectionChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(PerformanceProjectionChart, self).__init__(self.fig)
        self.setParent(parent)
        self.plot_projection()
        
    def plot_projection(self):
        # Sample data for performance projection
        months = range(13)  # 0 to 12 months
        
        # Simulated current portfolio performance
        current_mean = np.array([100]) * (1 + np.cumsum(np.random.normal(0.008, 0.02, 13)))
        
        # Simulated optimized portfolio performance
        optimized_mean = np.array([100]) * (1 + np.cumsum(np.random.normal(0.012, 0.025, 13)))
        
        # Confidence intervals (simulated)
        optimized_upper = optimized_mean * 1.15
        optimized_lower = optimized_mean * 0.9
        
        self.axes.clear()
        self.axes.plot(months, current_mean, 'b-', label='Current Portfolio')
        self.axes.plot(months, optimized_mean, 'g-', label='Optimized Portfolio')
        
        self.axes.fill_between(months, optimized_lower, optimized_upper, color='g', alpha=0.2)
        
        self.axes.set_xlabel('Months')
        self.axes.set_ylabel('Portfolio Value')
        self.axes.set_title('Projected Performance (12 Months)')
        self.axes.legend()
        self.axes.grid(True)
        
        # Add vertical line at current time
        self.axes.axvline(x=0, color='black', linestyle='--')
        self.axes.text(0.5, 105, 'Current', rotation=90)
        
        self.fig.tight_layout()
        self.draw()

class OptimizedPortfolioTable(QTableWidget):
    def __init__(self, parent=None):
        super(OptimizedPortfolioTable, self).__init__(parent)
        
        # Setup table
        self.setColumnCount(5)
        self.setRowCount(15)
        self.setHorizontalHeaderLabels(["Symbol", "Company", "Current (%)", "Optimized (%)", "Change (%)"])
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        
        # Sample data
        sample_data = [
            ("AAPL", "Apple Inc.", "7.8", "8.5", "+0.7"),
            ("MSFT", "Microsoft Corp.", "6.3", "7.2", "+0.9"),
            ("AMZN", "Amazon.com Inc.", "5.1", "6.5", "+1.4"),
            ("GOOGL", "Alphabet Inc.", "4.2", "5.3", "+1.1"),
            ("NVDA", "NVIDIA Corp.", "3.8", "4.2", "+0.4"),
            ("BRK.B", "Berkshire Hathaway", "3.2", "2.1", "-1.1"),
            ("META", "Meta Platforms", "2.9", "3.5", "+0.6"),
            ("TSLA", "Tesla Inc.", "2.5", "1.2", "-1.3"),
            ("JPM", "JPMorgan Chase", "2.3", "1.8", "-0.5"),
            ("V", "Visa Inc.", "2.1", "2.8", "+0.7"),
            ("JNJ", "Johnson & Johnson", "1.9", "2.4", "+0.5"),
            ("PG", "Procter & Gamble", "1.7", "1.5", "-0.2"),
            ("UNH", "UnitedHealth Group", "1.6", "2.0", "+0.4"),
            ("HD", "Home Depot Inc.", "1.5", "1.0", "-0.5"),
            ("MA", "Mastercard Inc.", "1.4", "1.8", "+0.4")
        ]
        
        # Populate table
        for i, (symbol, company, current, optimized, change) in enumerate(sample_data):
            self.setItem(i, 0, QTableWidgetItem(symbol))
            self.setItem(i, 1, QTableWidgetItem(company))
            self.setItem(i, 2, QTableWidgetItem(current))
            self.setItem(i, 3, QTableWidgetItem(optimized))
            
            change_item = QTableWidgetItem(change)
            if change.startswith("+"):
                change_item.setForeground(QColor(0, 128, 0))  # Green for positive
            elif change.startswith("-"):
                change_item.setForeground(QColor(255, 0, 0))  # Red for negative
            
            self.setItem(i, 4, change_item)

class MetricsComparisonWidget(QWidget):
    def __init__(self, parent=None):
        super(MetricsComparisonWidget, self).__init__(parent)
        
        layout = QGridLayout(self)
        
        # Headers
        metric_header = QLabel("Metric")
        metric_header.setFont(QFont("Arial", 10, QFont.Bold))
        current_header = QLabel("Current")
        current_header.setFont(QFont("Arial", 10, QFont.Bold))
        optimized_header = QLabel("Optimized")
        optimized_header.setFont(QFont("Arial", 10, QFont.Bold))
        difference_header = QLabel("Difference")
        difference_header.setFont(QFont("Arial", 10, QFont.Bold))
        
        layout.addWidget(metric_header, 0, 0)
        layout.addWidget(current_header, 0, 1)
        layout.addWidget(optimized_header, 0, 2)
        layout.addWidget(difference_header, 0, 3)
        
        # Sample comparison metrics
        metrics = [
            ("Expected Return", "12.3%", "15.7%", "+3.4%"),
            ("Volatility", "14.2%", "15.1%", "+0.9%"),
            ("Sharpe Ratio", "0.87", "1.04", "+0.17"),
            ("Max Drawdown", "-12.4%", "-13.1%", "-0.7%"),
            ("VaR (95%)", "-2.1%", "-2.3%", "-0.2%"),
            ("Beta to S&P 500", "1.05", "1.12", "+0.07")
        ]
        
        for i, (metric, current, optimized, diff) in enumerate(metrics, 1):
            metric_label = QLabel(metric)
            current_label = QLabel(current)
            optimized_label = QLabel(optimized)
            diff_label = QLabel(diff)
            
            # Color the difference based on whether higher is better
            if metric in ["Expected Return", "Sharpe Ratio"]:
                if diff.startswith("+"):
                    diff_label.setStyleSheet("color: green;")
                else:
                    diff_label.setStyleSheet("color: red;")
            elif metric in ["Volatility", "Max Drawdown", "VaR (95%)"]:
                if diff.startswith("-") and metric != "Max Drawdown":
                    diff_label.setStyleSheet("color: green;")
                elif diff.startswith("+"):
                    diff_label.setStyleSheet("color: red;")
                
            layout.addWidget(metric_label, i, 0)
            layout.addWidget(current_label, i, 1)
            layout.addWidget(optimized_label, i, 2)
            layout.addWidget(diff_label, i, 3)

class ResultsWidget(QWidget):
    def __init__(self, parent=None):
        super(ResultsWidget, self).__init__(parent)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Optimization Results")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        main_layout.addWidget(title)
        
        # Status bar
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_layout = QHBoxLayout(status_frame)
        
        status_layout.addWidget(QLabel("Optimization Status:"))
        status_value = QLabel("Completed")
        status_value.setFont(QFont("Arial", 10, QFont.Bold))
        status_value.setStyleSheet("color: green;")
        status_layout.addWidget(status_value)
        
        status_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        status_layout.addWidget(QLabel("Last run:"))
        last_run = QLabel("April 14, 2025, 10:23 AM")
        status_layout.addWidget(last_run)
        
        main_layout.addWidget(status_frame)
        
        # Tabs for different result views
        tabs = QTabWidget()
        
        # Allocation tab
        allocation_tab = QWidget()
        allocation_layout = QVBoxLayout(allocation_tab)
        
        allocation_chart = AllocationComparisonChart(width=8, height=5)
        allocation_layout.addWidget(allocation_chart)
        
        allocation_table = OptimizedPortfolioTable()
        allocation_layout.addWidget(allocation_table)
        
        tabs.addTab(allocation_tab, "Portfolio Allocation")
        
        # Performance tab
        performance_tab = QWidget()
        performance_layout = QVBoxLayout(performance_tab)
        
        performance_chart = PerformanceProjectionChart(width=8, height=5)
        performance_layout.addWidget(performance_chart)
        
        metrics_group = QGroupBox("Performance Metrics")
        metrics_layout = QVBoxLayout(metrics_group)
        metrics_layout.addWidget(MetricsComparisonWidget())
        performance_layout.addWidget(metrics_group)
        
        tabs.addTab(performance_tab, "Projected Performance")
        
        main_layout.addWidget(tabs)
        
        # Button section
        button_section = QWidget()
        button_layout = QHBoxLayout(button_section)
        
        apply_button = QPushButton("Apply Optimization")
        apply_button.setMinimumHeight(40)
        button_layout.addWidget(apply_button)
        
        export_button = QPushButton("Export Results")
        export_button.setMinimumHeight(40)
        button_layout.addWidget(export_button)
        
        rerun_button = QPushButton("Re-run Optimization")
        rerun_button.setMinimumHeight(40)
        button_layout.addWidget(rerun_button)
        
        button_layout.addStretch()
        
        main_layout.addWidget(button_section)