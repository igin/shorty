import sys
import pdfrw
from short_time_form import ShortTimeForm
from parse_report import TimeTrackingReport


def main(report_file_name: str):
    with open(report_file_name, 'r') as report_csv:
        time_tracking_report = TimeTrackingReport.parse_from_csv(report_csv)
        people = time_tracking_report.get_names()
        pdfs = ShortTimeForm.pdfs_from_report(time_tracking_report, year=2021, month=8)
        for index, pdf in enumerate(pdfs):
            pdfrw.PdfWriter().write(f'./output-new{index}.pdf', pdf)

if __name__ == '__main__':
    main(sys.argv[1])