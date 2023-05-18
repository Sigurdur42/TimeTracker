import csv
import io
from domainModels import TimeRecord
from typing import List

class DomainSerializer :
    def __init__(self):
        pass

    def serialize(self, records: List[TimeRecord]) :
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        
        for rec in records:
            rowData = (rec.start, rec.end)
            writer.writerow(rowData)
        
        done = output.getvalue()
        print(done)