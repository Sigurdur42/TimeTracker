from typing import List
import csv
import io
from datetime import datetime
from models import TimeRecord


class TimeRecordSerializer:
    def __init__(self):
        pass
    
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
    
    def read_csv(self, fileContent: str) -> List[TimeRecord]:
        result = list[TimeRecord]()
        lines = fileContent.splitlines()
        reader = csv.reader(lines)
        for row in reader:
            parsed = TimeRecord(
                day=datetime.strptime(row[0], "%d.%M.%Y").date(), 
                start=datetime.strptime(row[1], "%H:%M").time(), 
                end=datetime.strptime(row[2], "%H:%M").time(), )
            result.append(parsed)
        
        return result
    