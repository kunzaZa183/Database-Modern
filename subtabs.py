from PyQt6.QtWidgets import (
    QComboBox,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QHeaderView,
    QLineEdit,
    QTextEdit,
    QDateEdit,
    QSizePolicy,
    QCheckBox,
    QFrame,
    QTableWidgetItem,
    QFileDialog,
)
from PyQt6.QtCore import QDate, QBuffer, QIODevice, Qt
from PyQt6.QtGui import QPixmap
from models import *
import base64
from data import calculate_age

provinces = [
    "",
    "กรุงเทพมหานคร",
    "กระบี่",
    "กาญจนบุรี",
    "กาฬสินธุ์",
    "กำแพงเพชร",
    "ขอนแก่น",
    "จันทบุรี",
    "ฉะเชิงเทรา",
    "ชลบุรี",
    "ชัยนาท",
    "ชัยภูมิ",
    "ชุมพร",
    "เชียงราย",
    "เชียงใหม่",
    "ตรัง",
    "ตราด",
    "ตาก",
    "นครนายก",
    "นครปฐม",
    "นครพนม",
    "นครราชสีมา",
    "นครศรีธรรมราช",
    "นครสวรรค์",
    "นนทบุรี",
    "นราธิวาส",
    "น่าน",
    "บึงกาฬ",
    "บุรีรัมย์",
    "ปทุมธานี",
    "ประจวบคีรีขันธ์",
    "ปราจีนบุรี",
    "ปัตตานี",
    "พระนครศรีอยุธยา",
    "พะเยา",
    "พังงา",
    "พัทลุง",
    "พิจิตร",
    "พิษณุโลก",
    "เพชรบุรี",
    "เพชรบูรณ์",
    "แพร่",
    "ภูเก็ต",
    "มหาสารคาม",
    "มุกดาหาร",
    "แม่ฮ่องสอน",
    "ยโสธร",
    "ยะลา",
    "ร้อยเอ็ด",
    "ระนอง",
    "ระยอง",
    "ราชบุรี",
    "ลพบุรี",
    "ลำปาง",
    "ลำพูน",
    "เลย",
    "ศรีสะเกษ",
    "สกลนคร",
    "สงขลา",
    "สตูล",
    "สมุทรปราการ",
    "สมุทรสงคราม",
    "สมุทรสาคร",
    "สระแก้ว",
    "สระบุรี",
    "สิงห์บุรี",
    "สุโขทัย",
    "สุพรรณบุรี",
    "สุราษฎร์ธานี",
    "สุรินทร์",
    "หนองคาย",
    "หนองบัวลำภู",
    "อ่างทอง",
    "อำนาจเจริญ",
    "อุดรธานี",
    "อุตรดิตถ์",
    "อุทัยธานี",
    "อุบลราชธานี",
]


class GeneralTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        thai_info = QVBoxLayout()

        all_thai_address = QHBoxLayout()
        self.thai_address = QLineEdit()
        all_thai_address.addWidget(QLabel("ที่อยู่/Adress"))
        all_thai_address.addWidget(self.thai_address, 2)
        all_thai_address.addStretch(1)

        self.country = QLineEdit()
        self.country.setText("Thailand")
        all_thai_address.addWidget(QLabel("ประเทศ/Country"))
        all_thai_address.addWidget(self.country, 2)

        all_everything = QHBoxLayout()
        self.thai_fields = []
        for label in [
            "ตำบล/Sub-District",
            "อำเภอ/District",
            "จังหวัด/Province",
            "รหัสไปรษณีย์/Postal Code",
        ]:
            if label == "จังหวัด/Province":
                assert len(provinces) == 78
                widget = QComboBox()
                widget.addItems(provinces)
            else:
                widget = QLineEdit()
            all_everything.addWidget(QLabel(label))
            all_everything.addWidget(widget)
            self.thai_fields.append(widget)

        line_id_layout = QHBoxLayout()
        self.line_id = QLineEdit()
        self.phone_number = QLineEdit()
        line_id_layout.addWidget(QLabel("Line ID"))
        line_id_layout.addWidget(self.line_id)
        line_id_layout.addWidget(QLabel("เบอร์โทรศัพท์/Phone Number"))
        line_id_layout.addWidget(self.phone_number)

        top_info = QVBoxLayout()
        top_info.addLayout(all_thai_address)
        top_info.addLayout(all_everything)
        top_info.addLayout(line_id_layout)

        top_widget = QWidget()
        top_widget.setLayout(top_info)
        top_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.weight = QLineEdit()
        self.tallness = QLineEdit()

        health_layout = QHBoxLayout()
        health_layout.addWidget(QLabel("น้ำหนัก/Weight"))
        health_layout.addWidget(self.weight)
        health_layout.addWidget(QLabel("กก./kg"))
        health_layout.addStretch()
        health_layout.addWidget(QLabel("ส่วนสูง/Height"))
        health_layout.addWidget(self.tallness)
        health_layout.addWidget(QLabel("ซม./cm"))

        illness_layout = QHBoxLayout()
        self.illness = QLineEdit()
        illness_layout.addWidget(QLabel("โรคประจำตัว/Illness"))
        illness_layout.addWidget(self.illness)

        vertical_health_layout = QVBoxLayout()
        vertical_health_layout.addLayout(health_layout)
        vertical_health_layout.addLayout(illness_layout)

        bot_widget = QWidget()
        bot_widget.setLayout(vertical_health_layout)
        bot_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        thai_info.addWidget(top_widget, 2)
        thai_info.addWidget(bot_widget, 1)
        self.additional_info = QTextEdit()
        thai_info.addWidget(QLabel("Additional Information"))
        thai_info.addWidget(self.additional_info, 5)

        layout.addLayout(thai_info)

        picture_layout = QVBoxLayout()
        self.picture_label = QLabel()
        picture_layout.addWidget(self.picture_label)

        picture_buttons = QHBoxLayout()
        file_input_button = QPushButton("Upload Picture")
        file_input_button.clicked.connect(self.select_image)
        download_button = QPushButton("Download Picture")
        download_button.clicked.connect(self.download_image)
        delete_button = QPushButton("Delete Picture")
        delete_button.clicked.connect(self.delete_image)
        picture_buttons.addWidget(file_input_button)
        picture_buttons.addWidget(download_button)
        picture_buttons.addWidget(delete_button)
        picture_layout.addLayout(picture_buttons)

        layout.addLayout(picture_layout, 1)
        self.setLayout(layout)

        # for widget in self.findChildren(QLineEdit):
        #     widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)"
        )
        if file_name:
            self.image = QPixmap(file_name)
            self.picture_label.setPixmap(self.image)

    def download_image(self):
        if not hasattr(self, "image") or self.image.isNull():
            return
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_name:
            self.image.save(file_name)

    def delete_image(self):
        self.image = None
        self.picture_label.clear()

    def extract_data(self, student: StudentCreate):
        student.thai_address = self.thai_address.text()
        student.thai_subdistrict = (
            self.thai_fields[0].text()
            if isinstance(self.thai_fields[0], QLineEdit)
            else None
        )
        student.thai_district = (
            self.thai_fields[1].text()
            if isinstance(self.thai_fields[1], QLineEdit)
            else None
        )
        student.thai_province = (
            self.thai_fields[2].currentText()
            if isinstance(self.thai_fields[2], QComboBox)
            else None
        )
        student.thai_postal_code = (
            self.thai_fields[3].text()
            if isinstance(self.thai_fields[3], QLineEdit)
            else None
        )
        student.additional_info = self.additional_info.toPlainText()
        if getattr(self, "image", None):
            buffer = QBuffer()
            buffer.open(QIODevice.OpenModeFlag.WriteOnly)
            self.image.save(buffer, "PNG")
            student.picture = base64.b64encode(buffer.data()).decode("utf-8")
        student.line_id = self.line_id.text()
        student.phone_number = self.phone_number.text()
        student.country = self.country.text()
        student.weight = self.weight.text()
        student.height = self.tallness.text()
        student.illness = self.illness.text()

    def load_data(self, student: StudentCreate):
        self.thai_address.setText(student.thai_address or "")
        if hasattr(self, "thai_fields") and len(self.thai_fields) == 4:
            self.thai_fields[0].setText(student.thai_subdistrict or "")
            self.thai_fields[1].setText(student.thai_district or "")
            if isinstance(self.thai_fields[2], QComboBox):
                idx = self.thai_fields[2].findText(
                    str(student.thai_province)
                    if student.thai_province is not None
                    else ""
                )
                self.thai_fields[2].setCurrentIndex(idx if idx >= 0 else 0)
            self.thai_fields[3].setText(student.thai_postal_code or "")
        self.additional_info.setPlainText(student.additional_info or "")

        if student.picture:
            image_bytes = base64.b64decode(student.picture) if student.picture else None
            self.image = QPixmap()
            self.image.loadFromData(image_bytes)
            self.picture_label.setPixmap(self.image)
            self.picture_label.show()
        else:
            self.picture_label.clear()

        self.line_id.setText(student.line_id or "")
        self.phone_number.setText(student.phone_number or "")
        self.country.setText(student.country or "")
        self.weight.setText(student.weight or "")
        self.tallness.setText(student.height or "")
        self.illness.setText(student.illness or "")


class PaymentsTab(QWidget):
    options = [
        "",
        "ค่าเทอม",
        "ค่ากิจกรรม",
        "วันเกิด",
        "เยี่ยมเยียน",
        "คริสต์มาส",
        "เงินทุนประจำปี",
        "ค่าอื่นๆ",
    ]

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        self.setLayout(layout)

        self.all_transactions = QTableWidget()
        self.all_transactions.setColumnCount(4)
        self.all_transactions.setHorizontalHeaderLabels(
            ["Date", "Amount", "Purpose", "Note"]
        )

        header = self.all_transactions.horizontalHeader()
        if header is not None:
            header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.add_row_button = QPushButton("Add Row")
        self.delete_row_button = QPushButton("Delete Row")
        self.add_row_button.clicked.connect(self.add_transaction_row)
        self.delete_row_button.clicked.connect(self.delete_transaction_row)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        for btn in (self.add_row_button, self.delete_row_button):
            button_layout.addWidget(btn)

        self.left_side = QVBoxLayout()
        self.left_side.addLayout(button_layout)
        self.left_side.addWidget(self.all_transactions)

        # Add Total expenses label and non-editable textbox
        self.total_expenses_layout = QHBoxLayout()
        self.total_expenses_label = QLabel("Total expenses")
        self.total_expenses_box = QLineEdit()
        self.total_expenses_box.setReadOnly(True)
        self.total_expenses_layout.addStretch()
        for widget in (self.total_expenses_label, self.total_expenses_box):
            self.total_expenses_layout.addWidget(widget)

        self.right_side = QVBoxLayout()
        self.summary_table = QTableWidget()
        self.summary_table.setColumnCount(4)
        self.summary_table.setHorizontalHeaderLabels(["Year", "In", "Out", "Balance"])
        summary_header = self.summary_table.horizontalHeader()
        if summary_header is not None:
            summary_header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.right_side.addWidget(self.summary_table)
        self.right_side.addLayout(self.total_expenses_layout)

        layout.addLayout(self.left_side, 2)
        layout.addLayout(self.right_side, 1)

    def add_transaction_row(self):
        row = self.all_transactions.rowCount()
        self.all_transactions.insertRow(row)

        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        self.all_transactions.setCellWidget(row, 0, date_edit)

        combo = QComboBox()
        combo.addItems(self.options)
        self.all_transactions.setCellWidget(row, 2, combo)

    def delete_transaction_row(self):
        selected = self.all_transactions.currentRow()
        self.all_transactions.removeRow(selected)

    def extract_data(self, student: StudentCreate):
        student.transactions = []
        for row in range(self.all_transactions.rowCount()):
            values = [
                (
                    self.all_transactions.item(row, col).text()
                    if self.all_transactions.item(row, col)
                    else None
                )
                for col in range(self.all_transactions.columnCount())
            ]
            try:
                values[0] = self.all_transactions.cellWidget(row, 0).date().toPyDate()
                values[2] = self.all_transactions.cellWidget(row, 2).currentText()
                transaction = Transaction(
                    transaction_date=values[0] if values[0] else None,
                    amount=float(values[1]) if values[1] else None,
                    purpose=values[2] if values[2] else None,
                    note=values[3] if values[3] else None,
                )
                student.transactions.append(transaction)
            except Exception as e:
                print(e)
                continue

    def load_data(self, student: StudentCreate):
        self.all_transactions.setRowCount(0)
        self.summary_table.setRowCount(0)
        if getattr(student, "transactions", None):

            years = {}

            sum = 0.0

            for t in student.transactions:
                row = self.all_transactions.rowCount()
                self.add_transaction_row()
                for col, val in enumerate(
                    [
                        t.transaction_date,
                        t.amount,
                        t.purpose,
                        t.note,
                    ]
                ):
                    if val is not None:
                        if col == 0:
                            date_edit = QDateEdit()
                            date_edit.setCalendarPopup(True)
                            date_edit.setDate(val)
                            self.all_transactions.setCellWidget(row, col, date_edit)

                            if t.amount != None:
                                sum += t.amount
                                years.setdefault(val.year, [0, 0])
                                if t.amount > 0:
                                    years[val.year][0] += t.amount
                                else:
                                    years[val.year][1] += t.amount

                            if not val.year in years:
                                years[val.year] = [0, 0]

                        elif col == 2:
                            combo = QComboBox()
                            combo.addItems(self.options)
                            idx = combo.findText(val)
                            if idx >= 0:
                                combo.setCurrentIndex(idx)
                            self.all_transactions.setCellWidget(row, col, combo)
                        elif col == 1:
                            item = QTableWidgetItem(f"{val:.2f}")
                            item.setTextAlignment(
                                Qt.AlignmentFlag.AlignRight
                                | Qt.AlignmentFlag.AlignVCenter
                            )
                            self.all_transactions.setItem(row, col, item)
                        else:
                            self.all_transactions.setItem(
                                row, col, QTableWidgetItem(str(val))
                            )

            for year, values in sorted(years.items()):
                row = self.summary_table.rowCount()
                self.summary_table.insertRow(row)
                self.summary_table.setItem(row, 0, QTableWidgetItem(str(year)))
                self.summary_table.setItem(row, 1, QTableWidgetItem(f"{values[0]:.2f}"))
                self.summary_table.setItem(
                    row, 2, QTableWidgetItem(f"{-values[1]:.2f}")
                )
                self.summary_table.setItem(
                    row, 3, QTableWidgetItem(f"{values[0] + values[1]:.2f}")
                )
                for j in range(0, 4):
                    self.summary_table.item(row, j).setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )

            self.total_expenses_box.setText(f"{sum:.2f}")
            self.total_expenses_box.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            )
        else:
            self.total_expenses_box.setText("0.0")


class SchoolTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.controller = controller

        # Names layout
        names = QHBoxLayout()
        self.institution_name_en = QLineEdit()
        self.institution_name_th = QLineEdit()
        names.addWidget(QLabel("Institution Name"))
        names.addWidget(self.institution_name_en)
        names.addWidget(QLabel("ชื่อสถานศึกษา"))
        names.addWidget(self.institution_name_th)

        # All everything layout
        all_everything = QHBoxLayout()
        self.school_fields = []
        for label in ["ตำบล", "อำเภอ", "จังหวัด", "รหัสไปรษณีย์"]:
            if label == "จังหวัด":
                widget = QComboBox()
                widget.addItems(provinces)
            else:
                widget = QLineEdit()
            all_everything.addWidget(QLabel(label))
            all_everything.addWidget(widget)
            self.school_fields.append(widget)

        # Grade level layout
        grade_level = QHBoxLayout()
        self.grade_level_start = QLineEdit()
        self.grade_level_now = QLineEdit()
        self.major = QLineEdit()
        self.gpa = QLineEdit()
        grade_level.addWidget(QLabel("Grade Level (Start)"))
        grade_level.addWidget(self.grade_level_start)
        grade_level.addWidget(QLabel("Grade Level (Now)"))
        grade_level.addWidget(self.grade_level_now)
        grade_level.addWidget(QLabel("Major"))
        grade_level.addWidget(self.major)
        grade_level.addWidget(QLabel("GPA"))
        grade_level.addWidget(self.gpa)

        # Other stuff layout
        other_stuff = QHBoxLayout()

        subjects = self.controller.codes.all_codes[2].copy()
        subjects.insert(0, "")
        self.favorite_subject = QComboBox()
        self.favorite_subject.addItems(subjects)
        self.weakest_subject = QComboBox()
        self.weakest_subject.addItems(subjects)
        self.expected_grad_date = QDateEdit()
        self.expected_grad_date.setCalendarPopup(True)
        other_stuff.addWidget(QLabel("Favorite Subject"))
        other_stuff.addWidget(self.favorite_subject)
        other_stuff.addStretch()
        other_stuff.addWidget(QLabel("Weakest Subject"))
        other_stuff.addWidget(self.weakest_subject)
        other_stuff.addStretch()
        other_stuff.addWidget(QLabel("Expected Graduation Date"))
        other_stuff.addWidget(self.expected_grad_date)
        other_stuff.addStretch()

        self.memo = QTextEdit()

        not_memo = QVBoxLayout()
        not_memo.addLayout(names)
        not_memo.addLayout(all_everything)
        not_memo.addLayout(grade_level)
        not_memo.addLayout(other_stuff)
        not_memo_widget = QWidget()
        not_memo_widget.setLayout(not_memo)
        not_memo_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        layout.addWidget(not_memo_widget, 1)
        layout.addWidget(QLabel("Memo"))
        layout.addWidget(self.memo, 1)
        self.setLayout(layout)

        for widget in self.findChildren(QLineEdit):
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def refresh_code(self):
        self.favorite_subject.clear()
        self.weakest_subject.clear()
        subjects = self.controller.codes.all_codes[2].copy()
        subjects.insert(0, "")
        self.favorite_subject.addItems(subjects)
        self.weakest_subject.addItems(subjects)
        self.favorite_subject.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )
        self.weakest_subject.setSizeAdjustPolicy(
            QComboBox.SizeAdjustPolicy.AdjustToContents
        )

    def extract_data(self, student: StudentCreate):
        student.institution_name = self.institution_name_en.text()
        student.institution_name_th = self.institution_name_th.text()
        student.school_subdistrict = (
            self.school_fields[0].text()
            if isinstance(self.school_fields[0], QLineEdit)
            else None
        )
        student.school_district = (
            self.school_fields[1].text()
            if isinstance(self.school_fields[1], QLineEdit)
            else None
        )
        student.school_province = (
            self.school_fields[2].currentText()
            if isinstance(self.school_fields[2], QComboBox)
            else None
        )
        student.school_postal_code = (
            self.school_fields[3].text()
            if isinstance(self.school_fields[3], QLineEdit)
            else None
        )
        student.grade_level_start = self.grade_level_start.text()
        student.grade_level_now = self.grade_level_now.text()
        student.major = self.major.text()
        student.gpa = self.gpa.text()
        student.favorite_subject = self.favorite_subject.currentText()
        student.weakest_subject = self.weakest_subject.currentText()
        student.expected_graduation_date = self.expected_grad_date.date().toPyDate()
        student.school_memo = self.memo.toPlainText()

    def load_data(self, student: StudentCreate):
        self.institution_name_en.setText(student.institution_name or "")
        self.institution_name_th.setText(student.institution_name_th or "")
        if hasattr(self, "school_fields") and len(self.school_fields) == 4:
            self.school_fields[0].setText(student.school_subdistrict or "")
            self.school_fields[1].setText(student.school_district or "")
            if isinstance(self.school_fields[2], QComboBox):
                idx = self.school_fields[2].findText(
                    str(student.school_province)
                    if student.school_province is not None
                    else ""
                )
                self.school_fields[2].setCurrentIndex(idx if idx >= 0 else 0)
            self.school_fields[3].setText(student.school_postal_code or "")
        self.grade_level_start.setText(
            str(student.grade_level_start)
            if student.grade_level_start is not None
            else ""
        )
        self.grade_level_now.setText(
            str(student.grade_level_now) if student.grade_level_now is not None else ""
        )
        self.major.setText(student.major or "")
        self.gpa.setText(student.gpa or "")
        self.favorite_subject.setCurrentText(student.favorite_subject or "")
        self.weakest_subject.setCurrentText(student.weakest_subject or "")
        if student.expected_graduation_date:
            self.expected_grad_date.setDate(
                QDate.fromString(str(student.expected_graduation_date), "yyyy-MM-dd")
            )
        self.memo.setPlainText(student.school_memo or "")


class FamilyTab(QWidget):

    relationships = [
        "แม่ / Mother",
        "พ่อ / Father",
        "พี่สาว / Sister",
        "พี่ชาย / Brother",
        "น้องสาว / Younger Sister",
        "น้องชาย / Younger Brother",
        "น้าหรืออาผู้หญิง / Aunt",
        "น้าหรืออาผู้ชาย / Uncle",
        "ย่าหรือยาย / Grandmother",
        "ปู่หรือตา / Grandfather",
        "ลูกพี่ลูกน้อง / Cousin",
        "หลานชาย / Nephew",
        "หลานสาว / Niece",
        "อื่นๆ / Other",
    ]

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.family_table = QTableWidget()
        self.family_table.setColumnCount(9)
        self.family_table.setHorizontalHeaderLabels(
            [
                "ความสัมพันธ์",
                "ชื่อจริง",
                "นามสกุล",
                "First name",
                "Last name",
                "Get Age",
                "Age",
                "Birth year",
                "Note",
            ]
        )
        self.family_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.family_table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )

        label_and_button_layout = QHBoxLayout()

        add_button = QPushButton("Add Row")
        add_button.clicked.connect(self.add_transaction_row)
        delete_button = QPushButton("Delete Row")
        delete_button.clicked.connect(
            lambda: self.family_table.removeRow(self.family_table.currentRow())
        )
        label_and_button_layout.addWidget(QLabel("Family Members"))
        label_and_button_layout.addStretch()
        label_and_button_layout.addWidget(add_button)
        label_and_button_layout.addWidget(delete_button)

        layout.addLayout(label_and_button_layout)
        layout.addWidget(self.family_table)

        self.setLayout(layout)

        for widget in self.findChildren(QLineEdit):
            widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

    def add_transaction_row(self):
        row = self.family_table.rowCount()
        self.family_table.insertRow(row)

        relation_combo = QComboBox()
        relation_combo.addItems(self.relationships)
        self.family_table.setCellWidget(row, 0, relation_combo)

        age_label = QTableWidgetItem()
        age_label.setFlags(age_label.flags() ^ Qt.ItemFlag.ItemIsEditable)
        self.family_table.setItem(row, 6, age_label)

    def extract_data(self, student: StudentCreate):
        family_members = []
        for row in range(self.family_table.rowCount()):
            values = [
                (
                    self.family_table.item(row, col).text()
                    if self.family_table.item(row, col)
                    else None
                )
                for col in range(self.family_table.columnCount())
            ]
            values[0] = self.family_table.cellWidget(row, 0).currentText()
            try:
                values[5] = int(values[5])
                values[7] = str(date.today().year - int(values[5]))
            except Exception:
                pass

            member = FamilyMember(
                relation=values[0] if values[0] else None,
                thai_first_name=values[1] if values[1] else None,
                thai_last_name=values[2] if values[2] else None,
                eng_first_name=values[3] if values[3] else None,
                eng_last_name=values[4] if values[4] else None,
                birth_year=values[7] if values[7] else None,
                note=values[8],
            )
            family_members.append(member)

        student.family_members = family_members

    def load_data(self, student: StudentCreate):
        self.family_table.setRowCount(0)
        if getattr(student, "family_members", None):
            for f in student.family_members:
                row = self.family_table.rowCount()
                self.add_transaction_row()
                for col, val in enumerate(
                    [
                        f.relation,
                        f.thai_first_name,
                        f.thai_last_name,
                        f.eng_first_name,
                        f.eng_last_name,
                        "",
                        "",
                        f.birth_year,
                        f.note,
                    ]
                ):
                    if val is not None:
                        if col == 0:
                            relation_combo = QComboBox()
                            relation_combo.addItems(self.relationships)
                            idx = relation_combo.findText(val)
                            if idx >= 0:
                                relation_combo.setCurrentIndex(idx)
                            self.family_table.setCellWidget(row, col, relation_combo)
                        elif col == 7:
                            val = calculate_age(date(int(f.birth_year), 1, 1))
                            age_label = QTableWidgetItem(str(val))
                            age_label.setFlags(
                                age_label.flags() ^ Qt.ItemFlag.ItemIsEditable
                            )
                            self.family_table.setItem(row, 6, age_label)
                            self.family_table.setItem(row, col, QTableWidgetItem(str(f.birth_year)))
                        else:
                            self.family_table.setItem(
                                row, col, QTableWidgetItem(str(val))
                            )


class StoryTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()

        self.story_edits = {}
        for lang, label in [("English", "English"), ("Thai", "ภาษาไทย")]:
            vbox = QVBoxLayout()
            vbox.addWidget(QLabel(label))
            edit = QTextEdit()
            vbox.addWidget(edit)
            layout.addLayout(vbox, 1)
            self.story_edits[lang] = edit

        self.setLayout(layout)

    def extract_data(self, student: StudentCreate):
        student.story_en = self.story_edits["English"].toPlainText()
        student.story_th = self.story_edits["Thai"].toPlainText()

    def load_data(self, student: StudentCreate):
        self.story_edits["English"].setPlainText(student.story_en or "")
        self.story_edits["Thai"].setPlainText(student.story_th or "")


class DatesTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout()

        self.date_fields = []
        date_fields = [
            ("Application Date", QDateEdit()),
            ("Presented on (date)", QDateEdit()),
            ("Start Support Date", QDateEdit()),
            ("Exit Date", QDateEdit()),
        ]
        for label, widget in date_fields:
            widget.setCalendarPopup(True)
            hbox = QHBoxLayout()
            hbox.addWidget(QLabel(label))
            hbox.addWidget(widget)
            hbox.addStretch()
            layout.addLayout(hbox)
            self.date_fields.append((label, widget))

        self.setLayout(layout)

    def extract_data(self, student: StudentCreate):
        label_to_field = {
            "Application Date": "application_date",
            "Presented on (date)": "first_contact_date",
            "Start Support Date": "start_support_date",
            "Exit Date": "exit_date",
        }
        for label, widget in self.date_fields:
            value = widget.date().toPyDate()
            setattr(student, label_to_field[label], value)

    def load_data(self, student: StudentCreate):
        label_to_field = {
            "Application Date": "application_date",
            "Presented on (date)": "first_contact_date",
            "Start Support Date": "start_support_date",
            "Exit Date": "exit_date",
        }
        for label, widget in self.date_fields:
            value = getattr(student, label_to_field[label], None)
            if value:
                widget.setDate(QDate(value.year, value.month, value.day))


class ActivitiesInterestsTab(QWidget):

    extracurriculars = [
        "เล่นกีฬา/Sports",
        "ดนตรี/Music",
        "ศิลปะ/Art",
        "การแสดง/Performance",
    ]
    christian_activities = [
        "ศึกษาพระคัมภีร์/Bible Study",
        "ค่ายคริสเตียน/Camps & Retreats",
        "การช่วยเหลือชุมชน/Community Service",
    ]

    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        extracurriculars_layout = QVBoxLayout()
        extracurriculars_label_and_buttons = QHBoxLayout()
        extracurriculars_label_and_buttons.addWidget(
            QLabel("Extracurricular Activities")
        )
        extracurriculars_label_and_buttons.addStretch()
        self.add_extracurricular_button = QPushButton("Add Row")
        self.add_extracurricular_button.clicked.connect(self.add_extracurricular_row)
        self.delete_extracurricular_button = QPushButton("Delete Row")
        self.delete_extracurricular_button.clicked.connect(
            lambda: self.extracurriculars.removeRow(self.extracurriculars.currentRow())
        )
        extracurriculars_label_and_buttons.addWidget(self.add_extracurricular_button)
        extracurriculars_label_and_buttons.addWidget(self.delete_extracurricular_button)
        extracurriculars_layout.addLayout(extracurriculars_label_and_buttons)

        self.extracurriculars = QTableWidget()
        self.extracurriculars.setColumnCount(1)
        self.extracurriculars.setHorizontalHeaderLabels(["กิจกรรม"])
        self.extracurriculars.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        extracurriculars_layout.addWidget(self.extracurriculars)

        christ_activities_layout = QVBoxLayout()
        christ_activities_label_and_buttons = QHBoxLayout()
        christ_activities_label_and_buttons.addWidget(QLabel("Christian Activities"))
        christ_activities_label_and_buttons.addStretch()
        self.add_christ_activities_button = QPushButton("Add Row")
        self.add_christ_activities_button.clicked.connect(
            self.add_christ_activities_row
        )
        self.delete_christ_activities_button = QPushButton("Delete Row")
        self.delete_christ_activities_button.clicked.connect(
            lambda: self.christ_activities.removeRow(
                self.christ_activities.currentRow()
            )
        )
        christ_activities_label_and_buttons.addWidget(self.add_christ_activities_button)
        christ_activities_label_and_buttons.addWidget(
            self.delete_christ_activities_button
        )
        christ_activities_layout.addLayout(christ_activities_label_and_buttons)

        self.christ_activities = QTableWidget()
        self.christ_activities.setColumnCount(1)
        self.christ_activities.setHorizontalHeaderLabels(["กิจกรรม"])
        self.christ_activities.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        christ_activities_layout.addWidget(self.christ_activities)

        layout = QHBoxLayout()
        layout.addLayout(extracurriculars_layout)
        layout.addLayout(christ_activities_layout)
        self.setLayout(layout)

    def add_extracurricular_row(self):
        row = self.extracurriculars.rowCount()
        self.extracurriculars.insertRow(row)

        combo = QComboBox()
        extracurriculars = self.controller.codes.all_codes[3].copy()
        extracurriculars.insert(0, "")
        combo.addItems(extracurriculars)
        self.extracurriculars.setCellWidget(row, 0, combo)

    def add_christ_activities_row(self):
        row = self.christ_activities.rowCount()
        self.christ_activities.insertRow(row)

        combo = QComboBox()
        christian_activities = self.controller.codes.all_codes[4].copy()
        christian_activities.insert(0, "")
        combo.addItems(christian_activities)
        self.christ_activities.setCellWidget(row, 0, combo)

    def extract_data(self, student: StudentCreate):
        extracurriculars = []
        for row in range(self.extracurriculars.rowCount()):
            extracurriculars.append(
                self.extracurriculars.cellWidget(row, 0).currentText()
            )
        student.extracurricular_activities = extracurriculars

        christian_activities = []
        for row in range(self.christ_activities.rowCount()):
            christian_activities.append(
                self.christ_activities.cellWidget(row, 0).currentText()
            )
        student.christian_activities = christian_activities

    def load_data(self, student: StudentCreate):
        self.extracurriculars.setRowCount(0)
        if getattr(student, "extracurricular_activities", None):
            for a in student.extracurricular_activities:
                self.add_extracurricular_row()

                row = self.extracurriculars.rowCount()
                self.extracurriculars.cellWidget(row - 1, 0).setCurrentText(a)

        self.christ_activities.setRowCount(0)
        if getattr(student, "christian_activities", None):
            for a in student.christian_activities:
                self.add_christ_activities_row()

                row = self.christ_activities.rowCount()
                self.christ_activities.cellWidget(row - 1, 0).setCurrentText(a)


class VisitsTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller

        self.add_button = QPushButton("Add Row")
        self.add_button.clicked.connect(self.add_visit_row)
        self.delete_button = QPushButton("Delete Row")
        self.delete_button.clicked.connect(
            lambda: self.visit_table.removeRow(self.visit_table.currentRow())
        )

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Visits Tab"))
        top_layout.addStretch()
        top_layout.addWidget(self.add_button)
        top_layout.addWidget(self.delete_button)

        self.visit_table = QTableWidget()
        self.visit_table.setColumnCount(7)
        self.visit_table.setHorizontalHeaderLabels(
            ["Date", "Type", "Staff", "พบ", "สัมภาษณ์", "ถ่ายรูป", "Note"]
        )
        self.visit_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addWidget(self.visit_table)
        self.setLayout(layout)

    def add_visit_row(self):
        row = self.visit_table.rowCount()
        self.visit_table.insertRow(row)

        date_edit = QDateEdit()
        date_edit.setCalendarPopup(True)
        date_edit.setDate(QDate.currentDate())
        self.visit_table.setCellWidget(row, 0, date_edit)

        combo_box = QComboBox()
        combo_box.addItems(["", "ตัวต่อตัว", "กลุ่ม", "จดหมาย", "จัดกิจกรรม", "โทรศัพท์"])
        self.visit_table.setCellWidget(row, 1, combo_box)

        staff_combo_box = QComboBox()
        staff_codes = self.controller.codes.all_codes[1].copy()
        staff_codes.insert(0, "")
        staff_combo_box.addItems(staff_codes)
        self.visit_table.setCellWidget(row, 2, staff_combo_box)

        for i in range(3, 6):
            check_box = QTableWidgetItem()
            check_box.setFlags(
                Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled
            )
            check_box.setCheckState(Qt.CheckState.Unchecked)
            self.visit_table.setItem(row, i, check_box)

    def extract_data(self, student: StudentCreate):
        visits = []
        for row in range(self.visit_table.rowCount()):
            try:
                visit = Visit(
                    visit_date=self.visit_table.cellWidget(row, 0).date().toPyDate(),
                    visit_type=(
                        self.visit_table.item(row, 1).text()
                        if self.visit_table.item(row, 1)
                        else None
                    ),
                    staff=(
                        self.visit_table.cellWidget(row, 2).currentText()
                        if self.visit_table.item(row, 2)
                        else None
                    ),
                    met=self.visit_table.item(row, 3).checkState()
                    == Qt.CheckState.Checked,
                    interview=self.visit_table.item(row, 4).checkState()
                    == Qt.CheckState.Checked,
                    photo=self.visit_table.item(row, 5).checkState()
                    == Qt.CheckState.Checked,
                    note=(
                        self.visit_table.item(row, 6).text()
                        if self.visit_table.item(row, 6)
                        else None
                    ),
                )
                visits.append(visit)
            except Exception as e:
                print(e)
                continue
        student.visits = visits

    def load_data(self, student: StudentCreate):
        self.visit_table.setRowCount(0)
        if getattr(student, "visits", None):
            for visit in student.visits:
                row = self.visit_table.rowCount()
                self.add_visit_row()

                self.visit_table.setItem(
                    row, 0, QTableWidgetItem(str(visit.visit_date))
                )
                self.visit_table.setItem(
                    row, 1, QTableWidgetItem(str(visit.visit_type))
                )
                self.visit_table.cellWidget(row, 2).setCurrentText(str(visit.staff))
                self.visit_table.item(row, 3).setCheckState(
                    Qt.CheckState.Checked if visit.met else Qt.CheckState.Unchecked
                )
                self.visit_table.item(row, 4).setCheckState(
                    Qt.CheckState.Checked
                    if visit.interview
                    else Qt.CheckState.Unchecked
                )
                self.visit_table.item(row, 5).setCheckState(
                    Qt.CheckState.Checked if visit.photo else Qt.CheckState.Unchecked
                )
                self.visit_table.setItem(
                    row,
                    6,
                    (
                        QTableWidgetItem(str(visit.note))
                        if visit.note
                        else QTableWidgetItem("")
                    ),
                )


class ExitTab(QWidget):
    def __init__(self, controller, parent=None):
        super().__init__(parent)

        self.exit_code = QComboBox()
        exit_reasons = [
            "Support not required/ขอระงับทุน",
            "Better economy/ฐานะดีขึ้น",
            "Employed/ได้งานทำ",
            "Married/แต่งงาน",
            "Did not complete education/ไม่จบ",
            "Can not Contact/ไม่สามารถติดต่อได้",
            "Don't follow rule/ไม่ปฏิบัติตามกฎ",
            "Don't Know/ไม่ทราบ",
            "Move Province/ย้ายถิ่นที่อยู่",
            "Still sponsored with other organization/ได้รับทุนกับหน่วยงานอื่น",
            "Graduated/เรียนจบ",
            "GPA Lower than educational standard/ผลการเรียนต่ำกว่าเกณฑ์",
            "Died/เสียชีวิต"
        ]
        self.exit_code.addItems(exit_reasons)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.institution = QLineEdit()

        top_layout = QHBoxLayout()
        top_layout.addWidget(QLabel("Exit Code"))
        top_layout.addWidget(self.exit_code)
        top_layout.addWidget(QLabel("Start Date"))
        top_layout.addWidget(self.start_date)
        top_layout.addWidget(QLabel("End Date"))
        top_layout.addWidget(self.end_date)
        top_layout.addWidget(QLabel("Institution Name"))
        top_layout.addWidget(self.institution)

        bottom_layout = QHBoxLayout()

        frame_th = QFrame()
        frame_th.setFrameShape(QFrame.Shape.Box)
        frame_th.setLineWidth(2)
        frame_th.setObjectName("outerFrame")
        frame_th.setStyleSheet(
            "#outerFrame { border: 2px solid #888; border-radius: 4px; }"
        )
        group_th_layout = QVBoxLayout()

        self.employed_th = QCheckBox()
        self.employer_th = QLineEdit()
        employed_th_layout = QHBoxLayout()
        employed_th_layout.addWidget(QLabel("มีงานทำ"))
        employed_th_layout.addWidget(self.employed_th)
        employed_th_layout.addWidget(QLabel("ผู้จ้างงาน"))
        employed_th_layout.addWidget(self.employer_th)

        self.income_th = QLineEdit()
        self.economic_status_th = QLineEdit()
        self.employ_ops_th = QLineEdit()
        income_th_layout = QHBoxLayout()
        income_th_layout.addWidget(QLabel("แหล่งรายได้"))
        income_th_layout.addWidget(self.income_th)
        income_th_layout.addWidget(QLabel("ฐานะทางเศรษฐกิจ"))
        income_th_layout.addWidget(self.economic_status_th)
        income_th_layout.addWidget(QLabel("โอกาสได้งาน"))
        income_th_layout.addWidget(self.employ_ops_th)

        self.leave_th = QTextEdit()
        leave_th_layout = QHBoxLayout()
        leave_th_layout.addWidget(QLabel("สาเหตุของการยกเลิกทุน"))
        leave_th_layout.addWidget(self.leave_th)

        group_th_layout.addLayout(employed_th_layout)
        group_th_layout.addLayout(income_th_layout)
        group_th_layout.addLayout(leave_th_layout)
        frame_th.setLayout(group_th_layout)

        frame_en = QFrame()
        frame_en.setFrameShape(QFrame.Shape.Box)
        frame_en.setLineWidth(2)
        frame_en.setObjectName("outerFrame")
        frame_en.setStyleSheet(
            "#outerFrame { border: 2px solid #888; border-radius: 4px; }"
        )

        group_en_layout = QVBoxLayout()

        self.employed_en = QCheckBox()
        self.employer_en = QLineEdit()
        employed_en_layout = QHBoxLayout()
        employed_en_layout.addWidget(QLabel("Employed"))
        employed_en_layout.addWidget(self.employed_en)
        employed_en_layout.addWidget(QLabel("Employer"))
        employed_en_layout.addWidget(self.employer_en)

        self.income_en = QLineEdit()
        self.economic_status_en = QLineEdit()
        self.employ_ops_en = QLineEdit()
        income_en_layout = QHBoxLayout()
        income_en_layout.addWidget(QLabel("Source of Income"))
        income_en_layout.addWidget(self.income_en)
        income_en_layout.addWidget(QLabel("Economic Status"))
        income_en_layout.addWidget(self.economic_status_en)
        income_en_layout.addWidget(QLabel("Chances of Employment"))
        income_en_layout.addWidget(self.employ_ops_en)

        self.leave_en = QTextEdit()
        leave_en_layout = QHBoxLayout()
        leave_en_layout.addWidget(QLabel("Reason for Termination"))
        leave_en_layout.addWidget(self.leave_en)

        group_en_layout.addLayout(employed_en_layout)
        group_en_layout.addLayout(income_en_layout)
        group_en_layout.addLayout(leave_en_layout)
        frame_en.setLayout(group_en_layout)

        bottom_layout.addWidget(frame_th)
        bottom_layout.addWidget(frame_en)

        layout = QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def extract_data(self, student: StudentCreate):
        student.exit_code = self.exit_code.currentText()
        student.exit_start_date = self.start_date.date().toPyDate()
        student.exit_end_date = self.end_date.date().toPyDate()
        student.exit_institution = self.institution.text()
        student.employed_th = self.employed_th.isChecked()
        student.employer_th = self.employer_th.text()
        student.income_th = self.income_th.text()
        student.economic_status_th = self.economic_status_th.text()
        student.employ_ops_th = self.employ_ops_th.text()
        student.leave_reason_th = self.leave_th.toPlainText()
        student.employed_en = self.employed_en.isChecked()
        student.employer_en = self.employer_en.text()
        student.income_en = self.income_en.text()
        student.economic_status_en = self.economic_status_en.text()
        student.employ_ops_en = self.employ_ops_en.text()
        student.leave_reason_en = self.leave_en.toPlainText()

    def load_data(self, student: StudentCreate):
        if student.exit_code is not None:
            idx = self.exit_code.findText(student.exit_code)
            self.exit_code.setCurrentIndex(idx if idx >= 0 else 0)
        if student.exit_start_date:
            self.start_date.setDate(
                QDate(
                    student.exit_start_date.year,
                    student.exit_start_date.month,
                    student.exit_start_date.day,
                )
            )
        if student.exit_end_date:
            self.end_date.setDate(
                QDate(
                    student.exit_end_date.year,
                    student.exit_end_date.month,
                    student.exit_end_date.day,
                )
            )
        self.institution.setText(student.exit_institution or "")
        self.employed_th.setChecked(bool(student.employed_th))
        self.employer_th.setText(student.employer_th or "")
        self.income_th.setText(student.income_th or "")
        self.economic_status_th.setText(student.economic_status_th or "")
        self.employ_ops_th.setText(student.employ_ops_th or "")
        self.leave_th.setPlainText(student.leave_reason_th or "")
        self.employed_en.setChecked(bool(student.employed_en))
        self.employer_en.setText(student.employer_en or "")
        self.income_en.setText(student.income_en or "")
        self.economic_status_en.setText(student.economic_status_en or "")
        self.employ_ops_en.setText(student.employ_ops_en or "")
        self.leave_en.setPlainText(student.leave_reason_en or "")
