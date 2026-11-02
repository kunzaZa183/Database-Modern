"""Non-invasive improvements to the legacy student records page."""
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtWidgets import QComboBox, QLabel, QMessageBox, QHeaderView


class StudentFilterProxy(QSortFilterProxyModel):
    """Combine text search across columns with an optional status filter."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.status_filter = ""
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setFilterKeyColumn(-1)

    def set_status_filter(self, value):
        self.status_filter = value
        self.invalidateFilter()

    def filterAcceptsRow(self, source_row, source_parent):
        if not super().filterAcceptsRow(source_row, source_parent):
            return False
        if not self.status_filter:
            return True
        model = self.sourceModel()
        index = model.index(source_row, 1, source_parent)
        status = str(model.data(index, Qt.ItemDataRole.DisplayRole) or "")
        return status == self.status_filter


def enhance_student_list(tab):
    """Retain the existing model, callbacks and editor workflows."""
    tab.search_bar.setPlaceholderText("Search by name, ID, project, province...")
    tab.search_bar.setClearButtonEnabled(True)
    tab.add_button.setText("+ Add student")
    tab.delete_button.setText("Delete selected")
    tab.table_view.setAlternatingRowColors(True)
    tab.table_view.setShowGrid(False)
    tab.table_view.verticalHeader().setVisible(False)
    tab.table_view.verticalHeader().setDefaultSectionSize(40)
    tab.table_view.horizontalHeader().setSectionResizeMode(
        QHeaderView.ResizeMode.Interactive
    )
    tab.table_view.horizontalHeader().setStretchLastSection(True)

    # Reuse the existing source model, without touching the database schema.
    old_proxy = tab.proxy_model
    proxy = StudentFilterProxy(tab)
    proxy.setSourceModel(tab.controller.all_model)
    tab.proxy_model = proxy
    tab.table_view.setModel(proxy)
    tab.table_view.hideColumn(0)
    old_proxy.deleteLater()

    toolbar = tab.layout().itemAt(0).layout()
    status_box = QComboBox(tab)
    status_box.setMinimumWidth(160)
    status_box.addItem("All statuses", "")
    tab.status_filter_box = status_box
    toolbar.insertWidget(1, status_box)
    count_label = QLabel(tab)
    count_label.setObjectName("recordCountLabel")
    tab.record_count_label = count_label
    tab.layout().insertWidget(1, count_label)

    def refresh_statuses(*_):
        current = status_box.currentData() or ""
        statuses = set()
        model = tab.controller.all_model
        for row in range(model.rowCount()):
            value = model.data(model.index(row, 1), Qt.ItemDataRole.DisplayRole)
            if value:
                statuses.add(str(value))
        status_box.blockSignals(True)
        status_box.clear()
        status_box.addItem("All statuses", "")
        for value in sorted(statuses):
            status_box.addItem(value, value)
        selected = status_box.findData(current)
        status_box.setCurrentIndex(max(selected, 0))
        status_box.blockSignals(False)
        proxy.set_status_filter(status_box.currentData() or "")
        update_count()

    def update_count(*_):
        count_label.setText(f"Showing {proxy.rowCount()} of {tab.controller.all_model.rowCount()} students")

    status_box.currentIndexChanged.connect(
        lambda _: proxy.set_status_filter(status_box.currentData() or "")
    )
    proxy.rowsInserted.connect(update_count)
    proxy.rowsRemoved.connect(update_count)
    proxy.modelReset.connect(update_count)
    proxy.layoutChanged.connect(update_count)
    tab.controller.all_model.modelReset.connect(refresh_statuses)
    tab.controller.all_model.rowsInserted.connect(refresh_statuses)
    tab.controller.all_model.rowsRemoved.connect(refresh_statuses)

    # Add confirmation without altering the existing deletion implementation.
    tab.delete_button.clicked.disconnect()
    def confirm_delete():
        if not tab.table_view.selectionModel().hasSelection():
            QMessageBox.warning(tab, "No selection", "Select a student first.")
            return
        answer = QMessageBox.question(
            tab, "Confirm deletion",
            "Delete the selected student record? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if answer == QMessageBox.StandardButton.Yes:
            tab.delete()
    tab.delete_button.clicked.connect(confirm_delete)
    refresh_statuses()
