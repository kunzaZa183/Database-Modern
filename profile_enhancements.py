"""Presentation-only enhancements for student create/edit forms.

No database schema, field mapping, or save handlers are changed.
"""
from PyQt6.QtWidgets import QFrame, QLabel, QTabBar, QVBoxLayout


def enhance_profile(form):
    """Improve existing GeneralInfo-based forms without replacing widgets."""
    if getattr(form, "_modern_profile_enhanced", False):
        return
    form._modern_profile_enhanced = True
    form.setObjectName("modernProfileForm")
    form.setMinimumWidth(550)

    tabs = form.all_tabs
    tabs.setObjectName("modernProfileTabs")
    tabs.setDocumentMode(True)
    tabs.setMovable(False)
    tabs.setUsesScrollButtons(True)
    tabs.tabBar().setExpanding(False)
    tabs.tabBar().setElideMode(__import__("PyQt6.QtCore", fromlist=["Qt"]).Qt.TextElideMode.ElideRight)
    tabs.setToolTip("Choose a section to view or edit student information")

    # Keep the existing top form, tab instances, and save/cancel connections.
    layout = form.layout()
    layout.setContentsMargins(18, 16, 18, 18)
    layout.setSpacing(14)
    heading = QLabel("Student details")
    heading.setObjectName("modernProfileHeading")
    description = QLabel("Update the fields below, then save your changes.")
    description.setObjectName("modernProfileDescription")
    layout.insertWidget(0, description)
    layout.insertWidget(0, heading)

    form.save_button.setObjectName("modernPrimaryButton")
    form.save_button.setText("Save student")
    form.cancel_button.setText("Back to records")
    form.save_button.setMinimumHeight(38)
    form.cancel_button.setMinimumHeight(38)
    form.age.setReadOnly(True)
    form.age.setToolTip("Calculated from the student's birth date")
