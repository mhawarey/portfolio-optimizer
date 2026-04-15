#!/usr/bin/env python3
# main.py - Application entry point for Portfolio Optimizer

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from ui.main_window import MainWindow

def main():
    # Enable high-DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create the application
    app = QApplication(sys.argv)
    app.setApplicationName("Portfolio Optimizer")
    app.setStyle("Fusion")  # Use Fusion style for a modern look
    
    # Create and show the main window
    main_window = MainWindow()
    main_window.show()
    
    # Enter the application main loop
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()