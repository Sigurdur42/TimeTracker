import sys
from typing import List
import csv
import io
from datetime import datetime
from .models import TimeRecord
from pathlib import Path
import logging


class TimeRecordSerializer:
    def __init__(self):
        pass

    def write_csv_to_file(self, file_name: str, data: List[TimeRecord]):
        logging.info(f"Writing data to csv file {file_name}")
        content = self.generate_csv(data)
        with open(file_name, "w+") as file:
            file.write(content)

    def generate_csv(self, data: List[TimeRecord]) -> str:
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL, delimiter=";", lineterminator="\n")

        for rec in data:
            row = (
                rec.start.strftime("%d.%m.%Y"),
                rec.start.strftime("%H:%M"),
                rec.end.strftime("%H:%M"),
            )

            writer.writerow(row)

        return output.getvalue()

    def read_from_csv_file(self, file_name: str) -> List[TimeRecord]:
        if file_name is None or file_name == '':
            return list[TimeRecord]()

        path = Path(file_name)
        if not path.exists():
            return list[TimeRecord]()

        logging.info(f"Reading data from csv file {file_name}")
        with open(file_name, "r") as file:
            lines = file.readlines()
            return self.read_csv_from_lines(lines)

    @staticmethod
    def read_csv_from_lines(lines: List[str]) -> List[TimeRecord]:
        result = list[TimeRecord]()
        reader = csv.reader(lines, delimiter=";")
        index = 0
        for row in reader:
            if len(row) == 0:
                continue

            try:
                parsed = TimeRecord(
                    internal_id=index,
                    start=datetime.strptime(f'{row[0]} {row[1]}', "%d.%m.%Y %H:%M"),
                    end=datetime.strptime(f'{row[0]} {row[2]}', "%d.%m.%Y %H:%M"),
                )
                index += 1
                result.append(parsed)
            except ValueError as err:
                logging.error(f"Error parsing line {index} '{row}': {err}")

        return result

    def read_csv(self, file_content: str) -> List[TimeRecord]:
        lines = file_content.splitlines()
        return self.read_csv_from_lines(lines)
