# ui/optimization.py - Portfolio optimization controls

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QFrame, QPushButton, QSlider, QCheckBox,
                             QComboBox, QSpinBox, QDoubleSpinBox, QGroupBox,
                             QRadioButton, QSpacerItem, QSizePolicy)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class EfficientFrontierChart(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(EfficientFrontierChart, self).__init__(self.fig)
        self.setParent(parent)
        self.plot_efficient_frontier()
        
    def plot_efficient_frontier(self):
        # Generate sample efficient frontier
        returns = np.linspace(0.02, 0.20, 100)
        # Simulate the risk-return relationship (quadratic)
        risk = 0.05 + 0.5 * (returns - 0.02) + 0.5 * (returns - 0.02)**2
        
        self.axes.clear()
        self.axes.plot(risk, returns, 'b-', linewidth=2)
        
        # Plot a marker for current portfolio
        self.axes.plot(0.14, 0.12, 'ro', markersize=10)
        
        # Plot a marker for optimal portfolio
        self.axes.plot(0.16, 0.15, 'go', markersize=10)
        
        self.axes.set_xlabel('Risk (Volatility)')
        self.axes.set_ylabel('Expected Return')
        self.axes.set_title('Efficient Frontier')
        self.axes.grid(True)
        self.axes.legend(['Efficient Frontier', 'Current Portfolio', 'Optimized Portfolio'])
        
        self.fig.tight_layout()
        self.draw()

class OptimizationWidget(QWidget):
    def __init__(self, parent=None):
        super(OptimizationWidget, self).__init__(parent)
        
        # Main layout
        main_layout = QHBoxLayout(self)
        
        # Controls section
        controls_section = QWidget()
        controls_section.setMaximumWidth(400)
        controls_layout = QVBoxLayout(controls_section)
        
        # Optimization targets
        targets_group = QGroupBox("Optimization Target")
        targets_layout = QVBoxLayout(targets_group)
        
        self.max_return_radio = QRadioButton("Maximize Return")
        self.max_return_radio.setChecked(True)
        targets_layout.addWidget(self.max_return_radio)
        
        self.min_risk_radio = QRadioButton("Minimize Risk")
        targets_layout.addWidget(self.min_risk_radio)
        
        self.max_sharpe_radio = QRadioButton("Maximize Sharpe Ratio")
        targets_layout.addWidget(self.max_sharpe_radio)
        
        controls_layout.addWidget(targets_group)
        
        # Risk tolerance
        risk_group = QGroupBox("Risk Parameters")
        risk_layout = QGridLayout(risk_group)
        
        risk_layout.addWidget(QLabel("Maximum Volatility:"), 0, 0)
        self.max_volatility = QDoubleSpinBox()
        self.max_volatility.setRange(0.05, 0.50)
        self.max_volatility.setSingleStep(0.01)
        self.max_volatility.setValue(0.20)
        self.max_volatility.setSuffix(" (20%)")
        risk_layout.addWidget(self.max_volatility, 0, 1)
        
        risk_layout.addWidget(QLabel("Target Return:"), 1, 0)
        self.target_return = QDoubleSpinBox()
        self.target_return.setRange(0.01, 0.30)
        self.target_return.setSingleStep(0.01)
        self.target_return.setValue(0.15)
        self.target_return.setSuffix(" (15%)")
        risk_layout.addWidget(self.target_return, 1, 1)
        
        controls_layout.addWidget(risk_group)
        
        # Constraints
        constraints_group = QGroupBox("Constraints")
        constraints_layout = QGridLayout(constraints_group)
        
        # Liquidity constraint
        constraints_layout.addWidget(QLabel("Minimum Liquidity:"), 0, 0)
        self.min_liquidity = QComboBox()
        self.min_liquidity.addItems(["No constraint", "Low", "Medium", "High", "Very High"])
        self.min_liquidity.setCurrentIndex(2)  # Medium by default
        constraints_layout.addWidget(self.min_liquidity, 0, 1)
        
        # Min/Max position sizes
        constraints_layout.addWidget(QLabel("Maximum Position:"), 1, 0)
        self.max_position = QDoubleSpinBox()
        self.max_position.setRange(0.01, 0.20)
        self.max_position.setSingleStep(0.01)
        self.max_position.setValue(0.08)
        self.max_position.setSuffix(" (8%)")
        constraints_layout.addWidget(self.max_position, 1, 1)
        
        constraints_layout.addWidget(QLabel("Minimum Position:"), 2, 0)
        self.min_position = QDoubleSpinBox()
        self.min_position.setRange(0.0, 0.05)
        self.min_position.setSingleStep(0.005)
        self.min_position.setValue(0.01)
        self.min_position.setSuffix(" (1%)")
        constraints_layout.addWidget(self.min_position, 2, 1)
        
        # Sector constraints
        constraints_layout.addWidget(QLabel("Max Sector Allocation:"), 3, 0)
        self.max_sector = QDoubleSpinBox()
        self.max_sector.setRange(0.1, 0.5)
        self.max_sector.setSingleStep(0.05)
        self.max_sector.setValue(0.25)
        self.max_sector.setSuffix(" (25%)")
        constraints_layout.addWidget(self.max_sector, 3, 1)
        
        # Additional constraints
        self.enable_fundamental = QCheckBox("Enable Fundamental Filters")
        self.enable_fundamental.setChecked(True)
        constraints_layout.addWidget(self.enable_fundamental, 4, 0, 1, 2)
        
        controls_layout.addWidget(constraints_group)
        
        # Optimization button
        run_button = QPushButton("Run Optimization")
        run_button.setMinimumHeight(50)
        run_button.setFont(QFont("Arial", 12, QFont.Bold))
        controls_layout.addWidget(run_button)
        
        # Add a spacer to push everything up
        controls_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        
        main_layout.addWidget(controls_section)
        
        # Visualization section
        viz_section = QWidget()
        viz_layout = QVBoxLayout(viz_section)
        
        # Title
        title = QLabel("Portfolio Optimization")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        viz_layout.addWidget(title)
        
        # Efficient frontier plot
        self.efficient_frontier = EfficientFrontierChart(width=8, height=6)
        viz_layout.addWidget(self.efficient_frontier)
        
        # Description
        description = QLabel(
            "The efficient frontier represents the set of optimal portfolios that "
            "offer the highest expected return for a defined level of risk. "
            "The red dot represents your current portfolio, and the green dot "
            "shows the optimized portfolio based on your parameters."
        )
        description.setWordWrap(True)
        viz_layout.addWidget(description)
        
        # Status
        status_frame = QFrame()
        status_frame.setFrameShape(QFrame.StyledPanel)
        status_layout = QHBoxLayout(status_frame)
        
        status_layout.addWidget(QLabel("Status:"))
        status_value = QLabel("Ready to optimize")
        status_value.setFont(QFont("Arial", 10, QFont.Bold))
        status_layout.addWidget(status_value)
        
        status_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        
        status_layout.addWidget(QLabel("Last run:"))
        last_run = QLabel("Never")
        status_layout.addWidget(last_run)
        
        viz_layout.addWidget(status_frame)
        
        main_layout.addWidget(viz_section)