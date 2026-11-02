from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QStackedWidget,
    QMainWindow,
    QAbstractItemView,
    QMessageBox,
    QHeaderView,
    QDateEdit,
    QComboBox,
    QLabel,
    QTabWidget,
    QTableWidget,
    QSizePolicy,
    QTableView,
)
from PyQt6.QtCore import QSortFilterProxyModel, Qt 
import sys
from PyQt6.QtGui import QIcon
from models import StudentCreate
from subtabs import *
import os
import data

class CustomProxyModel(QSortFilterProxyModel):
    def headerData(self, section, orientation, role = Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return str(section + 1)
        return super().headerData(section, orientation, role)

class ListTab(QWidget):
    LIST_COLUMNS = [
        "ID",
        "สถานะ",
        "รหัสโครงการ",
        "จังหวัดของโครงการ",
        "English First Name",
        "English Last Name",
        "English Nickname",
        "ชื่อจริง",
        "นามสกุล",
        "ชื่อเล่น",
    ]

    def __init__(self, controller: "MainWindow"):
        super().__init__()
        self.controller = controller
        self._setup_ui()

    def _setup_ui(self):
        # Buttons
        self.add_button = QPushButton("Add")
        self.add_button.clicked.connect(self.controller.open_add_tab)
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete)
        self.edit_codes = QPushButton("Edit Codes")
        self.edit_codes.clicked.connect(self.controller.open_edit_code_tab)

        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search students...")

        # Proxy model for sorting and filtering
        self.proxy_model = CustomProxyModel(self)
        self.proxy_model.setSourceModel(self.controller.all_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.proxy_model.setFilterKeyColumn(-1)  # Search all columns

        # TableView (model-based)
        self.table_view = QTableView()
        self.table_view.setModel(self.proxy_model)
        self.table_view.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table_view.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table_view.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table_view.doubleClicked.connect(self._on_table_view_double_clicked)
        self.table_view.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_view.hideColumn(0)
        self.table_view.setSortingEnabled(True)

        # Connect search bar to proxy model filter
        self.search_bar.textChanged.connect(self._on_search_text_changed)

        # Layouts
        top_layout = QHBoxLayout()
        top_layout.addWidget(self.search_bar)
        top_layout.addWidget(self.add_button)
        top_layout.addWidget(self.delete_button)
        top_layout.addWidget(self.edit_codes)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.table_view)

        self.setLayout(main_layout)

    def _on_search_text_changed(self, text):
        self.proxy_model.setFilterFixedString(text)

    def delete(self):
        selected_indexes = self.table_view.selectedIndexes()
        if not selected_indexes:
            QMessageBox.warning(self, "Warning", "Please select a student to delete.")
            return
        row = selected_indexes[0].row()
        # Map proxy index to source model index
        source_row = self.proxy_model.mapToSource(self.proxy_model.index(row, 0)).row()
        ret = self.controller.all_model.delete_student(
            (int)(
                self.controller.all_model.data(
                    self.controller.all_model.index(source_row, 0)
                )
            )
        )
        if ret == 0:
            QMessageBox.information(self, "Success", "Student deleted successfully!")
        elif ret == 1:
            QMessageBox.warning(self, "Error", "Failed to delete student.")
        elif ret == 2:
            QMessageBox.critical(self, "Error", "Could not connect to API.")
        self.controller.all_model.set_students()

    def _on_table_view_double_clicked(self, index):
        # Map proxy index to source model index
        model_index = self.proxy_model.mapToSource(index)
        row = model_index.row()
        if 0 <= row < self.controller.all_model.rowCount():
            student_id = self.controller.all_model.data(
                self.controller.all_model.index(row, 0)
            )
            student = self.controller.all_model.students.get(int(student_id))
            if student:
                self.controller.open_info_tab(student)
            else:
                QMessageBox.warning(
                    self, "Error", f"Student with id {student_id} not found."
                )


class GeneralInfo(QWidget):
    STATUSES = [
        "",
        "Sponsored/ปัจจุบัน",
        "Approved/ปรับปรุงประวัติเด็กใหม่",
        "Rejected/ไม่อนุมัติ",
        "Left Program/ยกเลิกทุน",
        "Application/สัมภาษณ์เด็กใหม่",
    ]
    SEXES = ["", "Female/หญิง", "Male/ชาย"]

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        # Style this widget locally; do not depend on a global QApplication
        # variable that is undefined when imported by main.py.
        self.setStyleSheet(
            """
            QTextEdit {
                border: 1px solid #888;
                border-radius: 4px;
            }
            QTableWidget, QTableView {
                border: 1px solid #888;
                border-radius: 4px;
            }
        """
        )
        self._setup_ui()

    def _setup_ui(self):
        eng_labels = ["First Name", "Last Name", "Nickname"]
        thai_labels = ["ชื่อ", "นามสกุล", "ชื่อเล่น"]

        self.eng_lineedits = [QLineEdit() for _ in eng_labels]
        self.thai_lineedits = [QLineEdit() for _ in thai_labels]

        self.eng_first_name, self.eng_last_name, self.eng_nick_name = self.eng_lineedits
        self.thai_first_name, self.thai_last_name, self.thai_nick_name = (
            self.thai_lineedits
        )

        self.birth_date = QDateEdit()
        self.birth_date.setCalendarPopup(True)
        self.birth_date.setSpecialValueText("")

        self.age = QLineEdit()
        self.age.setReadOnly(True)

        self.status = QComboBox()
        self.status.addItems(self.STATUSES)

        self.sex = QComboBox()
        self.sex.addItems(self.SEXES)

        self.id = QLineEdit()
        self.code_project = QComboBox()
        project_codes = self.controller.codes.all_codes[0]
        project_codes.insert(0, "")
        self.code_project.addItems(project_codes)
        self.staff = QComboBox()
        staff_codes = self.controller.codes.all_codes[1]
        staff_codes.insert(0, "")
        self.staff.addItems(staff_codes)

        # Layouts for name inputs using loops
        eng_names_layout = QHBoxLayout()
        for label, lineedit in zip(eng_labels, self.eng_lineedits):
            eng_names_layout.addWidget(QLabel(label))
            eng_names_layout.addWidget(lineedit)
        eng_names_layout.addStretch()

        thai_names_layout = QHBoxLayout()
        for label, lineedit in zip(thai_labels, self.thai_lineedits):
            thai_names_layout.addWidget(QLabel(label))
            thai_names_layout.addWidget(lineedit)
        thai_names_layout.addStretch()

        row1_layout = QHBoxLayout()
        for label, widget in [
            ("Status", self.status),
            ("Code", self.id),
            ("Project", self.code_project),
            ("Staff", self.staff),
        ]:
            row1_layout.addWidget(QLabel(label))
            row1_layout.addWidget(widget)
        row1_layout.addStretch()

        row2_layout = QHBoxLayout()
        for label, widget in [
            ("Birth Date", self.birth_date),
            ("Age", self.age),
            ("Gender", self.sex),
        ]:
            row2_layout.addWidget(QLabel(label))
            row2_layout.addWidget(widget)   
        row2_layout.addStretch()

        # Save and cancel buttons (cancel goes back to list tab)
        self.save_button = QPushButton("Save")
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.controller.open_list_tab)

        buttons_layout = QVBoxLayout()
        for btn in (self.save_button, self.cancel_button):
            buttons_layout.addWidget(btn, 1)

        # Main top layout
        top_layout = QHBoxLayout()
        vertical_layout = QVBoxLayout()
        for layout in (eng_names_layout, thai_names_layout, row1_layout, row2_layout):
            vertical_layout.addLayout(layout)

        top_layout.addLayout(vertical_layout)
        top_layout.addLayout(buttons_layout)

        # Main layout for the widget
        main_layout = QVBoxLayout()
        top_widget = QWidget()
        top_widget.setLayout(top_layout)
        top_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        # top_widget.setStyleSheet("background-color: #7acef0;")
        main_layout.addWidget(top_widget, 1)

        # Tabs container
        self.all_tabs = QTabWidget()
        main_layout.addWidget(self.all_tabs, 4)

        self.set_all_tabs()
        self.setLayout(main_layout)

        # Set expanding size policy for all QLineEdit widgets
        for widget in self.findChildren(QLineEdit):
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def set_all_tabs(self):
        tab_classes = [
            (GeneralTab, "General Information"),
            (PaymentsTab, "Payments"),
            (SchoolTab, "School"),
            (FamilyTab, "Family"),
            (StoryTab, "Story"),
            (DatesTab, "Dates"),
            (ActivitiesInterestsTab, "Activities-Interests"),
            (VisitsTab, "Visits"),
            (ExitTab, "Exit"),
        ]
        self.tabs = []
        for tab_class, tab_name in tab_classes:
            tab = tab_class(self.controller)  
            self.all_tabs.addTab(tab, tab_name)
            self.tabs.append(tab)
        self.all_tabs.setCurrentIndex(0)
    
    def refresh_codes(self):
        project_codes = self.controller.codes.all_codes[0].copy()
        project_codes.insert(0, "")
        self.code_project.clear()
        self.code_project.addItems(project_codes)
        self.code_project.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        staff_codes = self.controller.codes.all_codes[1].copy()
        staff_codes.insert(0, "")
        self.staff.clear()
        self.staff.addItems(staff_codes)
        self.staff.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        
        self.tabs[2].refresh_code()

    def extract_data(self) -> StudentCreate:
        student = StudentCreate()
        student.eng_first_name = self.eng_first_name.text()
        student.eng_last_name = self.eng_last_name.text()
        student.eng_nick_name = self.eng_nick_name.text()
        student.thai_first_name = self.thai_first_name.text()
        student.thai_last_name = self.thai_last_name.text()
        student.thai_nick_name = self.thai_nick_name.text()
        student.status = self.status.currentText()
        student.fake_id = self.id.text() if self.id.text() else None
        student.birthdate = (
            self.birth_date.date().toPyDate()
        )
        student.gender = self.sex.currentText()
        student.project = self.code_project.currentText()
        student.staff = self.staff.currentText()

        for tab in getattr(self, "tabs", []):
            if hasattr(tab, "extract_data"):
                tab.extract_data(student)

        return student


class AddTab(GeneralInfo):
    def __init__(self, controller: "MainWindow"):
        super().__init__(controller)
        self.controller = controller
        self.save_button.clicked.connect(self.add_student)

    def add_student(self):
        student = self.extract_data()
        res = self.controller.all_model.add_student(student)
        if res == 1:
            QMessageBox.warning(self, "Error", "Failed to add student.")
        elif res == 2:
            QMessageBox.critical(self, "Error", "Could not connect to API.")
        else:
            QMessageBox.information(self, "Success", "Student added successfully!")

            self.controller.stack.removeWidget(self.controller.add_tab)
            self.controller.add_tab = AddTab(self.controller)
            self.controller.stack.insertWidget(2, self.controller.add_tab)
            self.controller.open_list_tab()


class InfoTab(GeneralInfo):
    def __init__(self, controller):
        super().__init__(controller)
        self.save_button.clicked.connect(self.edit_student)

    def load_data(self, student: StudentCreate):
        self.eng_first_name.setText(student.eng_first_name or "")
        self.eng_last_name.setText(student.eng_last_name or "")
        self.eng_nick_name.setText(student.eng_nick_name or "")
        self.thai_first_name.setText(student.thai_first_name or "")
        self.thai_last_name.setText(student.thai_last_name or "")
        self.thai_nick_name.setText(student.thai_nick_name or "")
        self.status.setCurrentText(student.status or "")
        self.id.setText(str(student.fake_id or ""))

        birthdate = getattr(student, "birthdate", None)
        self.birth_date.setDate(birthdate)
        self.age.setText(str(calculate_age(birthdate)))

        self.sex.setCurrentText(student.gender or "")
        self.code_project.setCurrentText(student.project or "")
        self.staff.setCurrentText(student.staff or "")

        # Ensure all dict fields exist for subtabs
        if not hasattr(student, "transactions"):
            student.transactions = []
        if not hasattr(student, "family_members"):
            student.family_members = {}
        if not hasattr(student, "extracurricular_activities"):
            student.extracurricular_activities = []
        if not hasattr(student, "christian_activities"):
            student.christian_activities = []
        if not hasattr(student, "visits"):
            student.visits = {}

        # Load all subtabs
        for tab in getattr(self, "tabs", []):
            if hasattr(tab, "load_data"):
                tab.load_data(student)

        # Store the current student id for editing
        self._current_student_id = student.id

    def edit_student(self):
        # Extract updated data from the form
        student = self.extract_data()
        student.id = self._current_student_id
        if student.id is None:
            QMessageBox.warning(self, "Error", "No student loaded for editing.")
            return
        res = self.controller.all_model.edit_student(student)
        if res == 1:
            QMessageBox.warning(self, "Error", "Failed to update student.")
        elif res == 2:
            QMessageBox.critical(self, "Error", "Could not connect to API.")
        else:
            QMessageBox.information(self, "Success", "Student updated successfully!")
            self.controller.all_model.set_students()
            self.load_data(student)

class SelectTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        self.create_button = QPushButton("Create new database file")
        self.load_button = QPushButton("Load existing database file")
        self.create_button.clicked.connect(self.create_db)
        self.load_button.clicked.connect(self.load_db)

        layout = QHBoxLayout()
        layout.addWidget(self.create_button)
        layout.addWidget(self.load_button)
        self.setLayout(layout)

    def create_db(self):
        file_path, _ = QFileDialog.getSaveFileName(
            None,
            "Create New Database",
            "",
            "Database Files (*.db);;All Files (*)"
        )

        if file_path:
            if not file_path.endswith(".db"):
                file_path += ".db"

            if os.path.exists(file_path):
                QMessageBox.warning(None, "File Exists", "This file already exists.")
                return

            QMessageBox.information(None, "Success", f"Database created at:\n{file_path}")

            data.DB_PATH = file_path
            self.controller.init_tabs()


    def load_db(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None,
            "Open Existing Database",
            "",
            "Database Files (*.db);;All Files (*)"
        )

        if file_path and os.path.exists(file_path):
            self.db_path = file_path
            QMessageBox.information(None, "Loaded", f"Database loaded from:\n{file_path}")

            data.DB_PATH = file_path
            self.controller.init_tabs()
        else:
            QMessageBox.warning(None, "Not Found", "File not selected or does not exist.")


class EditCodeTab(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.tables = []
        self.code_types = [
            "Project Codes",
            "Staff Codes",
            "Subject Codes",
            "Extracurricular Activity Codes",
            "Christian Activity Codes"
        ]

        mainer_layout = QVBoxLayout()

        main_layout = QHBoxLayout()

        # Create UI for each code type
        for name in self.code_types:
            section_layout = QVBoxLayout()
            top_layout = QHBoxLayout()
            top_layout.addWidget(QLabel(name))
            top_layout.addStretch()

            add_button = QPushButton("Add")
            delete_button = QPushButton("Delete")
            top_layout.addWidget(add_button)
            top_layout.addWidget(delete_button)

            table = QTableWidget()
            table.setColumnCount(1)
            table.setHorizontalHeaderLabels(["Code"])
            table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch )
            table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
            table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

            add_button.clicked.connect(lambda _, t=table: self.add_row(t))
            delete_button.clicked.connect(lambda _, t=table, n=name: self.delete_row(t, n))

            self.tables.append(table)
            section_layout.addLayout(top_layout)
            section_layout.addWidget(table)
            main_layout.addLayout(section_layout)

        mainer_layout.addLayout(main_layout)

        save_button = QPushButton("Save All")
        save_button.clicked.connect(self.save_all)
        mainer_layout.addWidget(save_button)

        self.setLayout(mainer_layout)
        self.load_data()

    def load_data(self):
        all_data = self.controller.codes.get_all_code_tables()  # List[List[str]]
        for table, data in zip(self.tables, all_data):
            table.setRowCount(0)
            for i, val in enumerate(data):
                table.insertRow(i)
                table.setItem(i, 0, QTableWidgetItem(val))

    def add_row(self, table: QTableWidget):
        row = table.rowCount()
        table.insertRow(row)
        table.setItem(row, 0, QTableWidgetItem(""))

    def delete_row(self, table: QTableWidget, table_name: str):
        selected = table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "No Selection", f"Select a row to delete from {table_name}.")
            return
        table.removeRow(selected)

    def save_all(self):
        """Collect data from all tables and send to controller."""
        all_data = []
        for table in self.tables:
            current = []
            for row in range(table.rowCount()):
                item = table.item(row, 0)
                if item:
                    text = item.text().strip()
                    if text:
                        current.append(text)
            all_data.append(current)
        self.controller.codes.save_all_code_tables(all_data)
        QMessageBox.information(self, "Saved", "All data saved successfully.")
        self.controller.open_list_tab() 



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("icon.ico"))
        self.setStyleSheet("font-size: 12pt;")
        self.setWindowTitle("Database")
        self._setup_ui()

    def _setup_ui(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.select_tab = SelectTab(self)
        self.stack.addWidget(self.select_tab)
        self.stack.setCurrentIndex(0)

    def init_tabs(self):
        self.all_model = data.StudentTableModel(ListTab.LIST_COLUMNS)
        res = self.all_model.fetch_students()

        self.codes = data.Codes()
        self.codes.get_all_code_tables()

        self.list_tab = ListTab(self)
        self.add_tab = AddTab(self)
        self.info_tab = InfoTab(self)
        self.edit_code_tab = EditCodeTab(self)
        self.stack.addWidget(self.list_tab)
        self.stack.addWidget(self.add_tab)
        self.stack.addWidget(self.info_tab)
        self.stack.addWidget(self.edit_code_tab)

        if res < 0:
            QMessageBox.critical(self, "Error", "Failed to fetch students. Please check if the server is running.")

        self.open_list_tab()


    def open_list_tab(self):
        self.all_model.set_students()
        self.stack.setCurrentIndex(1)

    def open_add_tab(self):
        self.add_tab.refresh_codes()
        self.stack.setCurrentIndex(2)

    def open_info_tab(self, student_dict):
        self.info_tab.refresh_codes()
        self.stack.setCurrentIndex(3)
        self.info_tab.load_data(student_dict)
    
    def open_edit_code_tab(self):
        self.stack.setCurrentIndex(4)
        self.edit_code_tab.load_data()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
