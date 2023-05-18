import unittest
import models
from datetime import datetime
from serializers import TimeRecordSerializer

class TimeTrackerTests(unittest.TestCase):
    def test_generate_and_read_csv(self):
        data2Write = [
            models.TimeRecord(
                day=datetime.strptime("01.01.2020", "%d.%M.%Y").date(), 
                start=datetime.strptime("8:30", "%H:%M").time(), 
                end=datetime.strptime("12:00", "%H:%M").time()),
            
            models.TimeRecord(
                day=datetime.strptime("01.01.2020", "%d.%M.%Y").date(), 
                start=datetime.strptime("12:30", "%H:%M").time(), 
                end=datetime.strptime("17:00", "%H:%M").time()),

            models.TimeRecord(
                day=datetime.strptime("02.01.2020", "%d.%M.%Y").date(), 
                start=datetime.strptime("8:45", "%H:%M").time(), 
                end=datetime.strptime("12:00", "%H:%M").time()),            
        ]
                       
        writer = TimeRecordSerializer()
        data = writer.generate_csv(data2Write)
        print(f"Generated CSV: {data}")
        
        writtenData = writer.read_csv(data)
        print(f"Read data: {writtenData}")
        
        self.assertCountEqual(
            data2Write, 
            writtenData, 
            "Collections should have same count of items")
        
        index = 0
        while index < data2Write.__len__():
            self.assertEquals(
                data2Write[index], 
                writtenData[index], 
                f"Data differs in index {index}")
            index += 1