"""Read-only sponsorship dashboard backed by the loaded student model."""
from collections import Counter
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame, QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QVBoxLayout, QWidget, QProgressBar
)


class DashboardPage(QWidget):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        outer.addWidget(scroll)
        body = QWidget()
        scroll.setWidget(body)
        layout = QVBoxLayout(body)
        layout.setSpacing(20)
        layout.setContentsMargins(4, 4, 4, 4)

        grid = QGridLayout()
        grid.setSpacing(12)
        self.total = self._metric(grid, 0, 0, "Total students")
        self.sponsored = self._metric(grid, 0, 1, "Sponsored")
        self.projects = self._metric(grid, 1, 0, "Projects")
        self.other = self._metric(grid, 1, 1, "Other statuses")
        layout.addLayout(grid)

        heading = QLabel("Sponsorship status breakdown")
        heading.setObjectName("dashboardSectionTitle")
        layout.addWidget(heading)
        self.status_details = QLabel()
        self.status_details.setObjectName("dashboardBreakdown")
        self.status_details.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self.status_details)
        self.status_bars = QVBoxLayout()
        layout.addLayout(self.status_bars)

        project_heading = QLabel("Students by project")
        project_heading.setObjectName("dashboardSectionTitle")
        layout.addWidget(project_heading)
        self.project_details = QLabel()
        self.project_details.setObjectName("dashboardBreakdown")
        self.project_details.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        layout.addWidget(self.project_details)
        self.project_bars = QVBoxLayout()
        layout.addLayout(self.project_bars)
        actions = QHBoxLayout()
        refresh = QPushButton("Refresh overview")
        refresh.clicked.connect(self.refresh)
        records = QPushButton("View student records")
        records.clicked.connect(controller.open_list_tab)
        actions.addWidget(refresh)
        actions.addWidget(records)
        actions.addStretch()
        layout.addLayout(actions)
        layout.addStretch()

    def _metric(self, grid, row, col, label):
        card = QFrame()
        card.setObjectName("dashboardMetricCard")
        content = QVBoxLayout(card)
        title = QLabel(label)
        title.setObjectName("dashboardMetricLabel")
        number = QLabel("0")
        number.setObjectName("dashboardMetricValue")
        content.addWidget(title)
        content.addWidget(number)
        grid.addWidget(card, row, col)
        return number

    def _render_bars(self, target, counts):
        while target.count():
            item = target.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        total = sum(counts.values())
        for name, count in counts.most_common(8):
            label = QLabel(f"{name}: {count}")
            label.setWordWrap(True)
            bar = QProgressBar()
            bar.setRange(0, max(total, 1))
            bar.setValue(count)
            bar.setTextVisible(False)
            bar.setAccessibleName(f"{name}: {count} of {total}")
            target.addWidget(label)
            target.addWidget(bar)

    def refresh(self):
        # Read the already loaded model only. No database writes or new SQL.
        students = list(self.controller.all_model.students.values())
        statuses = Counter((s.status or "Unspecified").strip() or "Unspecified"
                           for s in students)
        projects = Counter((s.project or "Unspecified").strip() or "Unspecified"
                           for s in students)
        self.total.setText(str(len(students)))
        self.sponsored.setText(str(sum(
            count for name, count in statuses.items()
            if name.lower().startswith("sponsored")
        )))
        self.projects.setText(str(len([p for p in projects if p != "Unspecified"])))
        self.other.setText(str(sum(
            count for name, count in statuses.items()
            if not name.lower().startswith("sponsored")
        )))
        self.status_details.setText("\n".join(
            f"{name}: {count}" for name, count in statuses.most_common()
        ) or "No records yet")
        self._render_bars(self.status_bars, statuses)
        self._render_bars(self.project_bars, projects)
        self.project_details.setText("\n".join(
            f"{name}: {count}" for name, count in projects.most_common()
        ) or "No records yet")
