from os import path
import pdfrw
from short_time_form import ShortTimeForm
from parse_report import TimeTrackingReport
import argparse
import logging


def generate_short_time_pdfs(*, report_file_name: str, output_dir: str, year: int, month: int):
    with open(report_file_name, 'r') as report_csv:
        time_tracking_report = TimeTrackingReport.parse_from_csv(report_csv)
        pdfs = ShortTimeForm.pdfs_from_report(time_tracking_report, year=year, month=month)
        for index, pdf in enumerate(pdfs):
            pdfrw.PdfWriter().write(path.join(output_dir, f'short-time-form-{index}.pdf'), pdf)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fill the swiss short time tracking PDF form from a time tracking report')
    parser.add_argument('--report-file', type=str, required=True, help='absolute path to the time tracking report file')
    parser.add_argument('--output-dir', type=str, required=True, help='absolute path to the output directory')
    parser.add_argument('--year', type=int, required=True, help='year the forms should be generated for')
    parser.add_argument('--month', type=int, required=True, help='month the forms should be generated for')

    args = parser.parse_args()


    if not path.exists(args.report_file):
        logging.critical("Provided report file doesn't exist. Please provide a correct path.")
        exit(1)

    if not path.exists(args.output_dir):
        logging.critical("Provided output directory doesn't exist. Please provide a correct path.")
        exit(1)
    

    generate_short_time_pdfs(
        report_file_name=args.report_file,
        output_dir=args.output_dir,
        year=args.year,
        month=args.month
    )