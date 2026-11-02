from PyQt6.QtCore import (
    Qt,
    QAbstractTableModel,
    QModelIndex,
)
from models import StudentCreate
from subtabs import *
from data import *
import sqlite3


def calculate_age(birthdate: date) -> int:
    today = date.today()
    age = today.year - birthdate.year
    if (today.month, today.day) < (birthdate.month, birthdate.day):
        age -= 1
    return age


DB_PATH = ""


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


class StudentTableModel(QAbstractTableModel):
    def __init__(self, columns, parent=None):
        super().__init__(parent)
        self.columns = columns
        self.students = {}  # Now a dict of {id (int): StudentCreate}
        self.create_table()

    def create_table(self):
        conn = get_db_connection()

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                eng_first_name TEXT,
                eng_last_name TEXT,
                eng_nick_name TEXT,
                thai_first_name TEXT,
                thai_last_name TEXT,
                thai_nick_name TEXT,
                status TEXT,
                fake_id TEXT,
                gender TEXT,
                birthdate TEXT,
                project TEXT,
                staff TEXT
            )
        """
        )
        # 2. Payments/Transactions
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                student_id INTEGER,
                transaction_date TEXT,
                amount REAL,
                purpose TEXT,
                note TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 4. Contact
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS contact_info (
                contact_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                thai_address TEXT,
                thai_subdistrict TEXT,
                thai_district TEXT,
                thai_province TEXT,
                thai_postal_code TEXT,
                additional_info TEXT,
                picture TEXT,
                line_id TEXT,
                phone_number TEXT,
                country TEXT,
                weight TEXT,
                height TEXT,
                illness TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 5. School
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS school_info (
                school_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                institution_name TEXT,
                institution_name_th TEXT,
                school_subdistrict TEXT,
                school_district TEXT,
                school_province TEXT,
                school_postal_code TEXT,
                grade_level_start INTEGER,
                grade_level_now INTEGER,
                major TEXT,
                gpa TEXT,
                favorite_subject TEXT,
                weakest_subject TEXT,
                expected_graduation_date TEXT,
                school_memo TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 7. Family
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS family_members (
                family_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                relation TEXT,
                thai_first_name TEXT,
                thai_last_name TEXT,
                eng_first_name TEXT,
                eng_last_name TEXT,
                birth_year TEXT,
                note TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 8. Story
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS story (
                story_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                story_en TEXT,
                story_th TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 9. Dates
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS student_dates (
                dates_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                application_date TEXT,
                first_contact_date TEXT,
                start_support_date TEXT,
                end_support_date TEXT,
                annual_report_date TEXT,
                exit_date TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 11. Activities-Interests
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS extracurricular_activities (
                student_id INTEGER,
                code TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS christian_activities (
                student_id INTEGER,
                code TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 13. Visits
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS visits (
                visit_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                visit_date TEXT,
                visit_type TEXT,
                staff TEXT,
                met BOOL,
                interview BOOL,
                photo BOOL,
                note TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        # 15. Exit
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exit_info (
                exit_id INTEGER PRIMARY KEY,
                student_id INTEGER,
                exit_code TEXT,
                exit_start_date TEXT,
                exit_end_date TEXT,
                exit_institution TEXT,
                employed_th BOOLEAN,
                employer_th TEXT,
                income_th TEXT,
                economic_status_th TEXT,
                employ_ops_th TEXT,
                leave_reason_th TEXT,
                employed_en BOOLEAN,
                employer_en TEXT,
                income_en TEXT,
                economic_status_en TEXT,
                employ_ops_en TEXT,
                leave_reason_en TEXT,
                FOREIGN KEY(student_id) REFERENCES students(id)
            )
        """
        )
        conn.commit()
        conn.close()

    def fetch_students(self):
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM students ORDER BY id DESC").fetchall()
        students_dict = {}
        for row in rows:
            student_id = row["id"]
            student_data = dict(row)
            # Transactions
            transactions = conn.execute(
                "SELECT * FROM transactions WHERE student_id = ?", (student_id,)
            ).fetchall()
            student_data["transactions"] = [
                Transaction(**dict(t)) for t in transactions
            ]
            # Contact
            contact = conn.execute(
                "SELECT * FROM contact_info WHERE student_id = ?", (student_id,)
            ).fetchone()
            if contact:
                student_data.update(dict(contact))
            # School
            school = conn.execute(
                "SELECT * FROM school_info WHERE student_id = ?", (student_id,)
            ).fetchone()
            if school:
                student_data.update(dict(school))
            # Family
            family_members = conn.execute(
                "SELECT * FROM family_members WHERE student_id = ?", (student_id,)
            ).fetchall()
            student_data["family_members"] = [
                FamilyMember(**dict(f)) for f in family_members
            ]
            # Story
            story = conn.execute(
                "SELECT * FROM story WHERE student_id = ?", (student_id,)
            ).fetchone()
            if story:
                student_data.update(dict(story))
            # Dates
            dates = conn.execute(
                "SELECT * FROM student_dates WHERE student_id = ?", (student_id,)
            ).fetchone()
            if dates:
                student_data.update(dict(dates))
            # Activities-Interests
            activities = conn.execute(
                "SELECT * FROM extracurricular_activities WHERE student_id = ?",
                (student_id,),
            ).fetchall()
            student_data["extracurricular_activities"] = [row[1] for row in activities]
            christ_activities = conn.execute(
                "SELECT * FROM christian_activities WHERE student_id = ?",
                (student_id,),
            ).fetchall()
            student_data["christian_activities"] = [row[1] for row in christ_activities]
            # Visits
            visits = conn.execute(
                "SELECT * FROM visits WHERE student_id = ?", (student_id,)
            ).fetchall()
            student_data["visits"] = [Visit(**dict(v)) for v in visits]
            # Exit
            exit_info = conn.execute(
                "SELECT * FROM exit_info WHERE student_id = ?", (student_id,)
            ).fetchone()
            if exit_info:
                student_data.update(dict(exit_info))
            # Build StudentCreate
            student = StudentCreate(**student_data)
            student.id = student_id
            students_dict[student.id] = student
        conn.close()
        self.students = students_dict
        self.set_students()
        return 0

    def rowCount(self, parent=QModelIndex()):
        return len(self.students)

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.columns[section]
            else:
                return str(section + 1)
        return None

    def set_students(self):
        self.beginResetModel()

        self._data = [
            [
                student.id,
                student.status or "",
                student.fake_id or "",
                student.project or "",
                student.eng_first_name or "",
                student.eng_last_name or "",
                student.eng_nick_name or "",
                student.thai_first_name or "",
                student.thai_last_name or "",
                student.thai_nick_name or "",
            ]
            for student in self.students.values()
        ]
        self.endResetModel()

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self._data)):
            return None
        if role == Qt.ItemDataRole.DisplayRole:
            return str(self._data[index.row()][index.column()])
        return None

    def get_student_dict(self, row):
        if 0 <= row < len(self._data):
            # This assumes you have the original students_data list in ListTab
            return self._data[row]
        return None

    def add_student(self, student: StudentCreate):
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                """
                INSERT INTO students (
                    eng_first_name, eng_last_name, eng_nick_name,
                    thai_first_name, thai_last_name, thai_nick_name,
                    status, fake_id, gender, birthdate, project, staff
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    student.eng_first_name,
                    student.eng_last_name,
                    student.eng_nick_name,
                    student.thai_first_name,
                    student.thai_last_name,
                    student.thai_nick_name,
                    student.status,
                    student.fake_id,
                    student.gender,
                    student.birthdate.isoformat() if student.birthdate else None,
                    student.project,
                    student.staff,
                ),
            )
            student.id = cursor.lastrowid

            # 1. Transactions
            if student.transactions:
                for t in student.transactions:
                    conn.execute(
                        """
                        INSERT INTO transactions (
                            student_id, transaction_date, amount, purpose, note 
                        ) VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            student.id,
                            (
                                t.transaction_date.isoformat()
                                if t.transaction_date
                                else None
                            ),
                            t.amount,
                            t.purpose,
                            t.note,
                        ),
                    )
            # 3. Contact
            conn.execute(
                """
                INSERT INTO contact_info (
                    student_id, thai_address, thai_subdistrict, thai_district, thai_province, thai_postal_code, additional_info, picture, line_id, phone_number, country, weight, height, illness
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?,?)
            """,
                (
                    student.id,
                    student.thai_address,
                    student.thai_subdistrict,
                    student.thai_district,
                    student.thai_province,
                    student.thai_postal_code,
                    student.additional_info,
                    student.picture if student.picture else None,
                    student.line_id,
                    student.phone_number,
                    student.country,
                    student.weight,
                    student.height,
                    student.illness,
                ),
            )
            # 4. School
            conn.execute(
                """
                INSERT INTO school_info (
                    student_id, institution_name, institution_name_th, school_subdistrict, school_district, school_province, school_postal_code, grade_level_start, grade_level_now, major, gpa, favorite_subject, weakest_subject, expected_graduation_date, school_memo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    student.id,
                    student.institution_name,
                    student.institution_name_th,
                    student.school_subdistrict,
                    student.school_district,
                    student.school_province,
                    student.school_postal_code,
                    student.grade_level_start,
                    student.grade_level_now,
                    student.major,
                    student.gpa,
                    student.favorite_subject,
                    student.weakest_subject,
                    (
                        student.expected_graduation_date.isoformat()
                        if student.expected_graduation_date
                        else None
                    ),
                    student.school_memo,
                ),
            )
            # 6. Family
            if student.family_members:
                for f in student.family_members:
                    conn.execute(
                        """
                        INSERT INTO family_members (
                            student_id, relation, thai_first_name, thai_last_name, eng_first_name, eng_last_name, birth_year, note
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            student.id,
                            f.relation,
                            f.thai_first_name,
                            f.thai_last_name,
                            f.eng_first_name,
                            f.eng_last_name,
                            f.birth_year,
                            f.note,
                        ),
                    )
            # 7. Story
            conn.execute(
                """
                INSERT INTO story (
                    student_id, story_en, story_th
                ) VALUES (?, ?, ?)
            """,
                (student.id, student.story_en, student.story_th),
            )
            # 8. Dates
            conn.execute(
                """
                INSERT INTO student_dates (
                    student_id, application_date, first_contact_date, start_support_date,  exit_date
                ) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    student.id,
                    (
                        student.application_date.isoformat()
                        if student.application_date
                        else None
                    ),
                    (
                        student.first_contact_date.isoformat()
                        if student.first_contact_date
                        else None
                    ),
                    (
                        student.start_support_date.isoformat()
                        if student.start_support_date
                        else None
                    ),
                    student.exit_date.isoformat() if student.exit_date else None,
                ),
            )
            # 9. Activities-Interests
            if student.extracurricular_activities:
                for a in student.extracurricular_activities:
                    conn.execute(
                        """
                        INSERT INTO extracurricular_activities (
                            student_id, code
                        ) VALUES (?, ?)
                    """,
                        (student.id, a),
                    )
            if student.christian_activities:
                for a in student.christian_activities:
                    conn.execute(
                        """
                        INSERT INTO christian_activities (
                            student_id, code
                        ) VALUES (?, ?)
                    """,
                        (student.id, a),
                    )
            # 10. Visits
            if student.visits:
                for v in student.visits:
                    conn.execute(
                        """
                        INSERT INTO visits (
                            student_id, visit_date, visit_type, staff, met, interview, photo, note
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            student.id,
                            v.visit_date.isoformat() if v.visit_date else None,
                            v.visit_type,
                            v.staff,
                            v.met,
                            v.interview,
                            v.photo,
                            v.note,
                        ),
                    )
            # 11. Exit
            conn.execute(
                """
                INSERT INTO exit_info (
                    student_id, exit_code, exit_start_date, exit_end_date, exit_institution,
                    employed_th, employer_th, income_th, economic_status_th, employ_ops_th, leave_reason_th,
                    employed_en, employer_en, income_en, economic_status_en, employ_ops_en, leave_reason_en
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    student.id,
                    student.exit_code,
                    (
                        student.exit_start_date.isoformat()
                        if student.exit_start_date
                        else None
                    ),
                    (
                        student.exit_end_date.isoformat()
                        if student.exit_end_date
                        else None
                    ),
                    student.exit_institution,
                    student.employed_th,
                    student.employer_th,
                    student.income_th,
                    student.economic_status_th,
                    student.employ_ops_th,
                    student.leave_reason_th,
                    student.employed_en,
                    student.employer_en,
                    student.income_en,
                    student.economic_status_en,
                    student.employ_ops_en,
                    student.leave_reason_en,
                ),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()
            return -1
        finally:
            conn.close()
        self.students[student.id] = student
        return 0

    def delete_student(self, student_id):
        del self.students[student_id]

        conn = get_db_connection()
        try:
            conn.execute("DELETE FROM transactions WHERE student_id = ?", (student_id,))
            conn.execute("DELETE FROM contact_info WHERE student_id = ?", (student_id,))
            conn.execute("DELETE FROM school_info WHERE student_id = ?", (student_id,))
            conn.execute(
                "DELETE FROM family_members WHERE student_id = ?", (student_id,)
            )
            conn.execute("DELETE FROM story WHERE student_id = ?", (student_id,))
            conn.execute(
                "DELETE FROM student_dates WHERE student_id = ?", (student_id,)
            )
            conn.execute(
                "DELETE FROM extracurricular_activities WHERE student_id = ?",
                (student_id,),
            )
            conn.execute("DELETE FROM visits WHERE student_id = ?", (student_id,))
            conn.execute("DELETE FROM exit_info WHERE student_id = ?", (student_id,))

            conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
        finally:
            conn.close()
        return 0

    def edit_student(self, student: StudentCreate):
        student_id = student.id
        conn = get_db_connection()
        try:
            # Update core student fields
            conn.execute(
                """
                UPDATE students SET
                    eng_first_name = ?, eng_last_name = ?, eng_nick_name = ?,
                    thai_first_name = ?, thai_last_name = ?, thai_nick_name = ?,
                    status = ?, fake_id = ?, birthdate = ?, gender = ?, project = ?, staff = ?
                WHERE id = ?
            """,
                (
                    student.eng_first_name,
                    student.eng_last_name,
                    student.eng_nick_name,
                    student.thai_first_name,
                    student.thai_last_name,
                    student.thai_nick_name,
                    student.status,
                    student.fake_id,
                    student.birthdate.isoformat() if student.birthdate else None,
                    student.gender,
                    student.project,
                    student.staff,
                    student_id,
                ),
            )

            # Delete and re-insert related tables for simplicity
            conn.execute("DELETE FROM transactions WHERE student_id = ?", (student_id,))
            if student.transactions:
                for t in student.transactions:
                    conn.execute(
                        """
                        INSERT INTO transactions (
                            student_id, transaction_date,  amount, purpose, note 
                        ) VALUES (?, ?, ?, ?, ?)
                    """,
                        (
                            student_id,
                            (
                                t.transaction_date.isoformat()
                                if t.transaction_date
                                else None
                            ),
                            t.amount,
                            t.purpose,
                            t.note,
                        ),
                    )

            conn.execute("DELETE FROM contact_info WHERE student_id = ?", (student_id,))
            conn.execute(
                """
                INSERT INTO contact_info (
                    student_id, thai_address, thai_subdistrict, thai_district, thai_province, thai_postal_code, additional_info, picture, line_id, phone_number, country, weight, height, illness
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?,?)
            """,
                (
                    student_id,
                    student.thai_address,
                    student.thai_subdistrict,
                    student.thai_district,
                    student.thai_province,
                    student.thai_postal_code,
                    student.additional_info,
                    student.picture if student.picture else None,
                    student.line_id,
                    student.phone_number,
                    student.country,
                    student.weight,
                    student.height,
                    student.illness,
                ),
            )

            conn.execute("DELETE FROM school_info WHERE student_id = ?", (student_id,))
            conn.execute(
                """
                INSERT INTO school_info (
                    student_id, institution_name, institution_name_th, school_subdistrict, school_district, school_province, school_postal_code, grade_level_start, grade_level_now, major, gpa, favorite_subject, weakest_subject, expected_graduation_date, school_memo
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    student_id,
                    student.institution_name,
                    student.institution_name_th,
                    student.school_subdistrict,
                    student.school_district,
                    student.school_province,
                    student.school_postal_code,
                    student.grade_level_start,
                    student.grade_level_now,
                    student.major,
                    student.gpa,
                    student.favorite_subject,
                    student.weakest_subject,
                    (
                        student.expected_graduation_date.isoformat()
                        if student.expected_graduation_date
                        else None
                    ),
                    student.school_memo,
                ),
            )

            conn.execute(
                "DELETE FROM family_members WHERE student_id = ?", (student_id,)
            )
            if student.family_members:
                for f in student.family_members:
                    conn.execute(
                        """
                        INSERT INTO family_members (
                            student_id, relation, thai_first_name, thai_last_name, eng_first_name, eng_last_name, birth_year, note
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            student_id,
                            f.relation,
                            f.thai_first_name,
                            f.thai_last_name,
                            f.eng_first_name,
                            f.eng_last_name,
                            f.birth_year,
                            f.note,
                        ),
                    )

            conn.execute("DELETE FROM story WHERE student_id = ?", (student_id,))
            conn.execute(
                """
                INSERT INTO story (
                    student_id, story_en, story_th
                ) VALUES (?, ?, ?)
            """,
                (student_id, student.story_en, student.story_th),
            )

            conn.execute(
                "DELETE FROM student_dates WHERE student_id = ?", (student_id,)
            )
            conn.execute(
                """
                INSERT INTO student_dates (
                    student_id, application_date, first_contact_date, start_support_date, exit_date
                ) VALUES (?, ?, ?, ?, ?)
            """,
                (
                    student_id,
                    (
                        student.application_date.isoformat()
                        if student.application_date
                        else None
                    ),
                    (
                        student.first_contact_date.isoformat()
                        if student.first_contact_date
                        else None
                    ),
                    (
                        student.start_support_date.isoformat()
                        if student.start_support_date
                        else None
                    ),
                    student.exit_date.isoformat() if student.exit_date else None,
                ),
            )

            conn.execute(
                "DELETE FROM extracurricular_activities WHERE student_id = ?",
                (student_id,),
            )
            conn.execute(
                "DELETE FROM christian_activities WHERE student_id = ?",
                (student_id,),
            )
            if student.extracurricular_activities:
                for a in student.extracurricular_activities:
                    conn.execute(
                        """
                        INSERT INTO extracurricular_activities (
                            student_id, code
                        ) VALUES (?, ?)
                    """,
                        (student_id, a),
                    )
            if student.christian_activities:
                for a in student.christian_activities:
                    conn.execute(
                        """
                        INSERT INTO christian_activities (
                            student_id, code
                        ) VALUES (?, ?)
                    """,
                        (student_id, a),
                    )

            conn.execute("DELETE FROM visits WHERE student_id = ?", (student_id,))
            if student.visits:
                for v in student.visits:
                    conn.execute(
                        """
                        INSERT INTO visits (
                            student_id, visit_date, visit_type, staff, met, interview, photo, note
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                        (
                            student_id,
                            v.visit_date.isoformat() if v.visit_date else None,
                            v.visit_type,
                            v.staff,
                            v.met,
                            v.interview,
                            v.photo,
                            v.note,
                        ),
                    )

            conn.execute("DELETE FROM exit_info WHERE student_id = ?", (student_id,))
            conn.execute(
                """
                INSERT INTO exit_info (
                    student_id, exit_code, exit_start_date, exit_end_date, exit_institution,
                    employed_th, employer_th, income_th, economic_status_th, employ_ops_th, leave_reason_th,
                    employed_en, employer_en, income_en, economic_status_en, employ_ops_en, leave_reason_en
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    student_id,
                    student.exit_code,
                    (
                        student.exit_start_date.isoformat()
                        if student.exit_start_date
                        else None
                    ),
                    (
                        student.exit_end_date.isoformat()
                        if student.exit_end_date
                        else None
                    ),
                    student.exit_institution,
                    student.employed_th,
                    student.employer_th,
                    student.income_th,
                    student.economic_status_th,
                    student.employ_ops_th,
                    student.leave_reason_th,
                    student.employed_en,
                    student.employer_en,
                    student.income_en,
                    student.economic_status_en,
                    student.employ_ops_en,
                    student.leave_reason_en,
                ),
            )

            conn.commit()
        finally:
            conn.close()
        self.students[student.id] = student
        return 0


class Codes:

    def __init__(self):
        conn = get_db_connection()
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS project_codes (
                id INTEGER PRIMARY KEY,
                code TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS staff_codes (
                id INTEGER PRIMARY KEY,
                code TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS subject_codes (
                id INTEGER PRIMARY KEY,
                code TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS extracurricular_activity_codes (
                id INTEGER PRIMARY KEY,
                code TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS christian_activity_codes (
                id INTEGER PRIMARY KEY,
                code TEXT
            )
            """
        )
        self.all_codes = [[], [], [], [], []]
        conn.commit()
        conn.close()

    def save_all_code_tables(self, all_data: list[list[str]]):
        # Save all_data to DB
        conn = get_db_connection()
        cursor = conn.cursor()

        table_names = [
            "project_codes",
            "staff_codes",
            "subject_codes",
            "extracurricular_activity_codes",
            "christian_activity_codes",
        ]

        for i, table_name in enumerate(table_names):
            # Clear old data
            cursor.execute(f"DELETE FROM {table_name}")
            # Insert new codes
            for code in all_data[i]:
                cursor.execute(f"INSERT INTO {table_name} (code) VALUES (?)", (code,))
        conn.commit()
        conn.close()
        self.all_codes = all_data

    def get_all_code_tables(self):
        conn = get_db_connection()
        result = []

        queries = [
            "SELECT code FROM project_codes",
            "SELECT code FROM staff_codes",
            "SELECT code FROM subject_codes",
            "SELECT code FROM extracurricular_activity_codes",
            "SELECT code FROM christian_activity_codes",
        ]

        for query in queries:
            rows = conn.execute(query).fetchall()
            codes = [row[0] for row in rows]
            result.append(codes)

        self.all_codes = result

        conn.close()
        return result
