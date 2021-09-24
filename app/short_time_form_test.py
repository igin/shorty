from typing import Dict
from short_time_form import ShortTimeForm
from datetime import date, datetime
from parse_report import TimeTrackingReport
import faker

fake = faker.Faker()

def generate_schedule(length: int, year: int, month: int) -> Dict[date, float]:
    schedule = {}
    for _ in range(length):
        fake_date = fake.date_between_dates(
            date(year, month, 1),
            date(year, month, 28)
            )
        hours = fake.pyfloat()
        schedule[fake_date] = hours
    return schedule

def generate_report(number_of_people: int, year: int = 2020, month: int = 8) -> Dict[str, Dict[date, float]]:
    report = {}
    for _ in range(number_of_people):
        name = fake.name()
        report[name] = generate_schedule(10, year=year, month=month)
    
    return report

def test_returns_single_pdf_for_single_person_report():
    report = TimeTrackingReport(hours_worked_per_person_per_day=generate_report(1))
    pdfs = ShortTimeForm.pdfs_from_report(report, year=2020, month=8)
    assert len(pdfs) == 1

def test_returns_two_pdfs_for_27_person_report():
    report = TimeTrackingReport(hours_worked_per_person_per_day=generate_report(27))
    pdfs = ShortTimeForm.pdfs_from_report(report, year=2020, month=8)
    assert len(pdfs) == 2

def test_data_dict_has_schedule_filled_for_person():
    report = TimeTrackingReport(hours_worked_per_person_per_day=generate_report(1, 2020, 8))
    data = ShortTimeForm.get_form_data_for_names_in_report(report, report.get_names(), 2020, 8)
    assert data["Name und Vorname"] == list(report.get_names())[0]

