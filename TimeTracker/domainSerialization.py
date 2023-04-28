import csv
import io

class DomainSerializer :
    def __init__(self):
        pass

    def serialize(self, records):
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerows(records)

        done = output.getvalue()
        print(done)