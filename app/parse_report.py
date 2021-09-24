import csv
import datetime
from dataclasses import dataclass, field
from typing import Dict, Set, TextIO
from operator import itemgetter


@dataclass
class TimeTrackingReport:
    hours_worked_per_person_per_day: Dict[str, Dict[datetime.date, float]] = \
        field(default_factory=dict)

    @staticmethod
    def parse_from_csv(csv_file: TextIO):
        reader = csv.DictReader(csv_file)
        all_schedules = {}
        for row in reader:
            first_name, last_name, date_string, hours_string = itemgetter(
                'First Name', 'Last Name', 'Date', 'Hours')(row)

            name =  f'{first_name} {last_name}'
            parsed_date = datetime.date.fromisoformat(date_string)
            schedule = all_schedules.get(name, {})
            existing_hours = schedule.get(parsed_date, 0.0)
            schedule[parsed_date] = existing_hours + float(hours_string)
            all_schedules[name] = schedule

        return TimeTrackingReport(hours_worked_per_person_per_day=all_schedules)

    def get_names(self) -> Set[str]:
        return set(self.hours_worked_per_person_per_day.keys())

    def get_schedule_of_person(self, name: str) -> Dict[datetime.date, float]:
        return self.hours_worked_per_person_per_day.get(name)

