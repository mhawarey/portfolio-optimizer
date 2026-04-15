# ui/main_window.py - Main application window

from PyQt5.QtWidgets import (QMainWindow, QTabWidget, QVBoxLayout, 
                             QHBoxLayout, QWidget, QAction, QMenuBar,
                             QStatusBar, QLabel, QSplitter)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from ui.dashboard import DashboardWidget
from ui.optimization import OptimizationWidget
from ui.results import ResultsWidget
from ui.universe import UniverseWidget
from ui.settings import SettingsWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Window setup
        self.setWindowTitle("Portfolio Optimizer - S&P 500 - By Dr. Mosab Hawarey")
        self.setMinimumSize(1200, 800)
        
        # Create the central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Create main layout
        self.main_layout = QVBoxLayout(self.central_widget)
        
        # Create tab widget for main interface
        self.tab_widget = QTabWidget()
        
        # Create widgets for each tab
        self.dashboard = DashboardWidget()
        self.optimization = OptimizationWidget()
        self.results = ResultsWidget()
        self.universe = UniverseWidget()
        self.settings = SettingsWidget()
        
        # Add tabs
        self.tab_widget.addTab(self.dashboard, "Dashboard")
        self.tab_widget.addTab(self.optimization, "Optimization")
        self.tab_widget.addTab(self.results, "Results")
        self.tab_widget.addTab(self.universe, "Stock Universe")
        self.tab_widget.addTab(self.settings, "Settings")
        
        # Add tab widget to main layout
        self.main_layout.addWidget(self.tab_widget)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Create data status indicator
        self.data_status = QLabel("Data: Demo Mode")
        self.status_bar.addPermanentWidget(self.data_status)
        
        # Setup menu bar
        self.create_menu_bar()
        
    def create_menu_bar(self):
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        
        new_action = QAction("&New Portfolio", self)
        new_action.setShortcut("Ctrl+N")
        file_menu.addAction(new_action)
        
        open_action = QAction("&Open Portfolio", self)
        open_action.setShortcut("Ctrl+O")
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save Portfolio", self)
        save_action.setShortcut("Ctrl+S")
        file_menu.addAction(save_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("E&xit", self)
        exit_action.setShortcut("Alt+F4")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Optimization menu
        optim_menu = self.menuBar().addMenu("&Optimization")
        
        run_action = QAction("&Run Optimization", self)
        run_action.setShortcut("F5")
        optim_menu.addAction(run_action)
        
        backtest_action = QAction("&Backtest", self)
        optim_menu.addAction(backtest_action)
        
        # Data menu
        data_menu = self.menuBar().addMenu("&Data")
        
        refresh_action = QAction("&Refresh Data", self)
        refresh_action.setShortcut("F4")
        data_menu.addAction(refresh_action)
        
        import_action = QAction("&Import Data...", self)
        data_menu.addAction(import_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        
        about_action = QAction("&About", self)
        help_menu.addAction(about_action)