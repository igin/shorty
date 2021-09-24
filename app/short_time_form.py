from datetime import date, datetime, timedelta
from typing import Dict, Iterable, List
from parse_report import TimeTrackingReport
import pdfrw

SHORT_TIME_FORM_PATH = './app/swiss_short_time_form.pdf'
NAME_FORM_KEY = 'Name und Vorname'

class ShortTimeForm:
    @staticmethod
    def pdfs_from_report(report: TimeTrackingReport, year: int, month: int) -> List[pdfrw.PdfReader]:
        names = report.get_names()
        names_per_pdf = _split_list_into_slices(list(names), 25)
        pdfs = []
        for names in names_per_pdf:
            form_data = ShortTimeForm.get_form_data_for_names_in_report(
                report, names=names, year=year, month=month
            )
            pdf = ShortTimeForm.pdf_for_form_data(form_data=form_data)
            pdfs.append(pdf)

        return pdfs

    @staticmethod
    def pdf_for_form_data(form_data: Dict[str, str]) -> pdfrw.PdfReader:
        form_pdf = pdfrw.PdfReader(SHORT_TIME_FORM_PATH)
        form_pdf.Root.AcroForm.update(pdfrw.PdfDict(
            NeedAppearances=pdfrw.PdfObject('true')))

        for page in form_pdf.pages:
            for annotation in page['/Annots']:
                key = annotation['/T'][1:-1]
                if annotation['/Subtype'] == '/Widget' and key in form_data.keys():
                    key = annotation['/T'][1:-1]
                    annotation.update(pdfrw.PdfDict(AP='', V=f'{str(form_data[key])}'))
        
        return form_pdf

    @staticmethod
    def get_form_data_for_names_in_report(
        report: TimeTrackingReport, 
        names: List[str],
        year: int,
        month: int
    ) -> Dict[str, str]:
        data_dict = {}
        for person_index, name in enumerate(names):
            data_dict[ShortTimeForm.get_form_key_for_name(person_index)] = name
            
            person_schedule = report.get_schedule_of_person(name)
            for day in _days_of_month(year, month):
                hours_in_day = person_schedule.get(day, 0)
                if hours_in_day > 0:
                    data_dict[ShortTimeForm.get_form_key_for_hours(day, 
                        person_index=person_index)] = hours_in_day
            
        return data_dict

    @staticmethod
    def get_form_key_for_hours(day: date, person_index: int):
        day_in_month = _day_in_month(day)
        postfix = f'_{person_index+1}' if person_index > 0 else ''
        return f"{day_in_month}{postfix}"

    @staticmethod
    def get_form_key_for_name(person_index: int):
        postfix = f'_{person_index+1}' if person_index > 0 else ''
        return f"{NAME_FORM_KEY}{postfix}"


def _split_list_into_slices(input_list: List, slice_size: int) -> List:
    return [input_list[i:i + slice_size] for i in range(0, len(input_list), slice_size)]

def _days_of_month(year: int, month: int) -> Iterable:
    day = date(year, month, 1)
    
    while day.month == month:
        yield day
        day = day + timedelta(days=1)

def _day_in_month(date: date) -> int:
    return date.strftime("%d").lstrip("0")