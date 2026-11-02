"""Centralized visual theme for the PyQt6 desktop application."""

APP_STYLESHEET = """
QWidget { font-family: 'Segoe UI', 'Noto Sans', sans-serif; font-size: 13px; color: #17253B; }
QMainWindow, QStackedWidget { background-color: #F6F8FC; }
QLabel { background: transparent; }
QPushButton { background: #E8EEF7; border: 1px solid #CFD9E8; border-radius: 8px; padding: 9px 15px; font-weight: 600; }
QPushButton:hover { background: #DCE7F8; border-color: #91ACD3; }
QPushButton:pressed { background: #CCDDF4; }
QPushButton:disabled { color: #8B97A9; background: #F0F2F6; }
QPushButton:focus, QLineEdit:focus, QComboBox:focus, QDateEdit:focus { border: 2px solid #2563EB; }
QLineEdit, QComboBox, QDateEdit, QTextEdit, QPlainTextEdit, QSpinBox, QDoubleSpinBox { background: #FFFFFF; border: 1px solid #CBD5E1; border-radius: 7px; padding: 7px; selection-background-color: #BFDBFE; }
QTableView, QTableWidget { background: #FFFFFF; alternate-background-color: #F7FAFF; border: 1px solid #DFE5EF; border-radius: 9px; gridline-color: #E8EDF4; selection-background-color: #DBEAFE; selection-color: #17253B; }
QHeaderView::section { background: #EAF0F8; color: #334155; padding: 9px; border: 0; border-right: 1px solid #DCE4F0; border-bottom: 1px solid #DCE4F0; font-weight: 600; }
QTabWidget::pane { background: #FFFFFF; border: 1px solid #DEE6F1; border-radius: 8px; }
QTabBar::tab { background: #E9EFF8; border: 1px solid #D6E0EF; padding: 9px 14px; margin-right: 3px; border-top-left-radius: 7px; border-top-right-radius: 7px; }
QTabBar::tab:selected { background: #FFFFFF; color: #1D4ED8; border-bottom-color: #FFFFFF; }
QScrollBar:vertical { background: #F1F5F9; width: 11px; }
QScrollBar::handle:vertical { background: #AABBD0; border-radius: 5px; min-height: 25px; }
QMessageBox { background: #F6F8FC; }
#dashboardMetricCard { background: #FFFFFF; border: 1px solid #DCE5F0; border-radius: 12px; }
#dashboardMetricLabel { color: #64748B; font-size: 13px; }
#dashboardMetricValue { color: #17375F; font-size: 30px; font-weight: 700; }
#dashboardSectionTitle { color: #17375F; font-size: 17px; font-weight: 700; }
#dashboardBreakdown { background: #FFFFFF; border: 1px solid #DCE5F0; border-radius: 10px; padding: 14px; color: #334155; font-size: 13px; }

#modernProfileHeading { color: #14253C; font-size: 21px; font-weight: 700; }
#modernProfileDescription { color: #64748B; font-size: 12px; }
#modernPrimaryButton { color: #FFFFFF; background: #2563EB; border: 1px solid #1D4ED8; }
#modernPrimaryButton:hover { background: #1D4ED8; }
#modernProfileTabs QTabBar::tab { padding: 10px 14px; }

#modernRoot, #modernContent { background: #F6F8FC; }
#modernSidebar { background: #12243C; border: none; }
#modernSidebar QLabel { color: #B7C8DF; }
#modernBrand { color: #FFFFFF; font-size: 20px; font-weight: 700; }
#modernSubtitle { color: #A9BFD9; font-size: 12px; }
#modernNavButton { color: #DFE9F8; background: transparent; border: 0; text-align: left; padding: 12px 14px; font-size: 14px; }
#modernNavButton:hover { background: #254365; }
#modernNavButton[active="true"] { background: #2C5790; color: white; }
#modernNavButton:disabled { color: #74879E; }
#modernPageTitle { font-size: 26px; font-weight: 700; color: #14253C; }
#modernPageSubtitle { font-size: 13px; color: #63748A; }

"""

def apply_theme(app):
    """Apply consistent widget styling without changing database behavior."""
    app.setStyleSheet(APP_STYLESHEET)
