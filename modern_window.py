"""Modern navigation shell around the unchanged legacy record workflows."""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
)
from viewer2 import MainWindow


class ModernMainWindow(MainWindow):
    """Wrap the original QStackedWidget without replacing its pages."""

    PAGE_TITLES = {
        0: ("Welcome", "Create or open a local database to begin."),
        1: ("Student records", "Search and manage sponsorship records."),
        2: ("Add student", "Create a new student record."),
        3: ("Student profile", "Review and edit student details."),
        4: ("Reference codes", "Manage project and activity codes."),
    }

    def __init__(self):
        super().__init__()
        self.setMinimumSize(920, 600)
        self._build_shell()
        self.stack.currentChanged.connect(self._sync_navigation)
        self._sync_navigation(self.stack.currentIndex())

    def init_tabs(self):
        super().init_tabs()
        from records_enhancements import enhance_student_list
        enhance_student_list(self.list_tab)

    def _build_shell(self):
        # Reparent the original stack into a layout, keeping its page instances
        # and all legacy controller methods intact.
        stack = self.stack
        container = QWidget(self)
        container.setObjectName("modernRoot")
        root = QHBoxLayout(container)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        sidebar = QFrame(container)
        sidebar.setObjectName("modernSidebar")
        sidebar.setFixedWidth(224)
        nav = QVBoxLayout(sidebar)
        nav.setContentsMargins(16, 28, 16, 20)
        nav.setSpacing(8)
        brand = QLabel("Project L.I.F.E.")
        brand.setObjectName("modernBrand")
        nav.addWidget(brand)
        subtitle = QLabel("Sponsorship Manager")
        subtitle.setObjectName("modernSubtitle")
        nav.addWidget(subtitle)
        nav.addSpacing(28)

        self.nav_buttons = []
        for label, handler in (
            ("Student records", self.open_list_tab),
            ("Add student", self.open_add_tab),
            ("Reference codes", self.open_edit_code_tab),
        ):
            button = QPushButton(label)
            button.setObjectName("modernNavButton")
            button.setProperty("active", False)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(handler)
            nav.addWidget(button)
            self.nav_buttons.append(button)
        nav.addStretch(1)
        nav.addWidget(QLabel("Local SQLite database"))
        root.addWidget(sidebar)

        content = QWidget(container)
        content.setObjectName("modernContent")
        column = QVBoxLayout(content)
        column.setContentsMargins(28, 24, 28, 24)
        column.setSpacing(16)
        self.page_title = QLabel()
        self.page_title.setObjectName("modernPageTitle")
        self.page_subtitle = QLabel()
        self.page_subtitle.setObjectName("modernPageSubtitle")
        column.addWidget(self.page_title)
        column.addWidget(self.page_subtitle)
        column.addWidget(stack, 1)
        root.addWidget(content, 1)
        self.setCentralWidget(container)

    def _sync_navigation(self, index):
        title, subtitle = self.PAGE_TITLES.get(index, ("Records", ""))
        self.page_title.setText(title)
        self.page_subtitle.setText(subtitle)
        ready = hasattr(self, "list_tab")
        for button in self.nav_buttons:
            button.setEnabled(ready)
        active_index = {1: 0, 2: 1, 4: 2}.get(index, -1)
        for i, button in enumerate(self.nav_buttons):
            button.setProperty("active", i == active_index)
            button.style().unpolish(button)
            button.style().polish(button)
