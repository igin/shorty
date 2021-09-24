from datetime import date
from parse_report import TimeTrackingReport

def test_extracts_single_person_from_csv():
    with open('./app/example_time_reports/basic_single_person_export.csv', 'r') as csv_file:
        report = TimeTrackingReport.parse_from_csv(csv_file)
        assert report.get_names() == set(['Max Mustermann'])

def test_extracts_multiple_people_from_csv():
    with open('./app/example_time_reports/basic_multi_person_export.csv', 'r') as csv_file:
        report = TimeTrackingReport.parse_from_csv(csv_file)
        assert set(report.get_names()) == set(['Max Mustermann', 'Albert Einstein', 'Gitte Gunter'])

def test_extracts_all_days_for_single_person():
    with open('./app/example_time_reports/basic_single_person_export.csv', 'r') as csv_file:
        report = TimeTrackingReport.parse_from_csv(csv_file)
        schedule = report.get_schedule_of_person('Max Mustermann')
        assert schedule == {
            date.fromisoformat('2021-08-02'): 3.5,
            date.fromisoformat('2021-08-03'): 1.2,
            date.fromisoformat('2021-08-06'): 6,
            date.fromisoformat('2021-08-09'): 7,
            date.fromisoformat('2021-08-10'): 9,
        }