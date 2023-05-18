from typing import List
import csv
import io
from datetime import datetime
from models import TimeRecord


class TimeRecordSerializer:
    def __init__(self):
        pass
    
    def write_csv_to_file(self, fileName: str, data : List[TimeRecord]):
        content = self.generate_csv(data)
        with open(fileName, "x") as file:
            file.write(content)
            
    
    def generate_csv(self, data : List[TimeRecord]) -> str:
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        
        for rec in data :
            row = (
                rec.day.strftime("%d.%M.%Y"), 
                rec.start.strftime("%H:%M"), 
                rec.end.strftime("%H:%M"))
            
            writer.writerow(row)
            
        return output.getvalue()
    
    def read_from_csv(self, fileName: str) -> List[TimeRecord]:
        with open(fileName, "r") as file:
            lines = file.readlines()
            return self.read_csv_from_lines(lines)
        
    def read_csv_from_lines(self, lines: List[str]) -> List[TimeRecord]:
        result = list[TimeRecord]()
        reader = csv.reader(lines)
        for row in reader:
            parsed = TimeRecord(
                day=datetime.strptime(row[0], "%d.%M.%Y").date(), 
                start=datetime.strptime(row[1], "%H:%M").time(), 
                end=datetime.strptime(row[2], "%H:%M").time(), )
            result.append(parsed)
        return result
        
    def read_csv(self, fileContent: str) -> List[TimeRecord]:
        lines = fileContent.splitlines()        
        return self.read_csv_from_lines(lines)
    