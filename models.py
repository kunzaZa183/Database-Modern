from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date

class Transaction(BaseModel):
    transaction_date: Optional[date] = None 
    amount: Optional[float] = None
    purpose: Optional[str] = None
    note: Optional[str] = None

class FamilyMember(BaseModel):
    relation: Optional[str] = None
    thai_first_name: Optional[str] = None
    thai_last_name: Optional[str] = None
    eng_first_name: Optional[str] = None
    eng_last_name: Optional[str] = None
    birth_year: Optional[str] = None
    note: Optional[str] = None

class Visit(BaseModel):
    visit_date: Optional[date] = None
    visit_type: Optional[str] = None
    staff: Optional[str] = None
    met: Optional[bool] = None
    interview: Optional[bool] = None
    photo: Optional[bool] = None
    note: Optional[str] = None

class StudentCreate(BaseModel):
    id: Optional[int] = None
    eng_first_name: Optional[str] = None
    eng_last_name: Optional[str] = None
    eng_nick_name: Optional[str] = None
    thai_first_name: Optional[str] = None
    thai_last_name: Optional[str] = None
    thai_nick_name: Optional[str] = None
    status: Optional[str] = None
    fake_id: Optional[str] = None
    project: Optional[str] = None
    staff: Optional[str] = None
    birthdate: Optional[date] = None
    gender: Optional[str] = None
    # 1. Payments/Transactions (PaymentsTab)
    transactions: Optional[list[Transaction]] = None
    # 3. Contact
    thai_address: Optional[str] = None
    thai_subdistrict: Optional[str] = None
    thai_district: Optional[str] = None
    thai_province: Optional[str] = None
    thai_postal_code: Optional[str] = None
    additional_info: Optional[str] = None
    country: Optional[str] = None
    line_id: Optional[str] = None
    phone_number: Optional[str] = None
    picture: Optional[str] = None 
    weight: Optional[str] = None
    height: Optional[str] = None
    illness: Optional[str] = None
    # 4. School
    institution_name: Optional[str] = None
    institution_name_th: Optional[str] = None
    school_subdistrict: Optional[str] = None
    school_district: Optional[str] = None
    school_province: Optional[str] = None
    school_postal_code: Optional[str] = None
    grade_level_start: Optional[str] = None
    grade_level_now: Optional[str] = None
    major: Optional[str] = None
    gpa: Optional[str] = None
    favorite_subject: Optional[str] = None
    weakest_subject: Optional[str] = None
    expected_graduation_date: Optional[date] = None
    school_memo: Optional[str] = None
    # 6. Family
    family_members: Optional[list[FamilyMember]] = None
    # 7. Story
    story_en: Optional[str] = None
    story_th: Optional[str] = None
    # 8. Dates
    application_date: Optional[date] = None
    first_contact_date: Optional[date] = None
    start_support_date: Optional[date] = None
    exit_date: Optional[date] = None
    # 11. Activities/Interests (table, not included as single fields)
    extracurricular_activities: Optional[list[str]] = None
    christian_activities: Optional[list[str]] = None
    # 13. Visits (table, not included as single fields)
    visits: Optional[list[Visit]] = None  
    # 14. Exit
    exit_code: Optional[str] = None
    exit_start_date: Optional[date] = None
    exit_end_date: Optional[date] = None
    exit_institution: Optional[str] = None
    # Employment/Income/Leave (Thai)
    employed_th: Optional[bool] = None
    employer_th: Optional[str] = None
    income_th: Optional[str] = None
    economic_status_th: Optional[str] = None
    employ_ops_th: Optional[str] = None
    leave_reason_th: Optional[str] = None
    # Employment/Income/Leave (English)
    employed_en: Optional[bool] = None
    employer_en: Optional[str] = None
    income_en: Optional[str] = None
    economic_status_en: Optional[str] = None
    employ_ops_en: Optional[str] = None
    leave_reason_en: Optional[str] = None

    model_config = ConfigDict(
        ser_json_bytes="base64"
    )