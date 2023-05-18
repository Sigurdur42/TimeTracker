from typing import List
import unittest
import models
import os
from datetime import datetime
from serializers import TimeRecordSerializer
import tempfile

class TimeTrackerTests(unittest.TestCase):
    def test_generate_and_read_csv_in_memory(self):
        data2Write = self.__generate_test_data()                       
        writer = TimeRecordSerializer()
        data = writer.generate_csv(data2Write)
        print(f"Generated CSV: {data}")
        
        writtenData = writer.read_csv(data)
        print(f"Read data: {writtenData}")
        
        self.__compare_collections(data2Write, writtenData)
        
    def test_generate_and_read_csv_from_file(self):
        data2Write = self.__generate_test_data()                       
        writer = TimeRecordSerializer()
        fileName = tempfile.mktemp()
        print(f"using file: '{fileName}'")
        writer.write_csv_to_file(fileName, data2Write)
        readData = writer.read_from_csv(fileName)
        self.__compare_collections(data2Write, readData)
        os.remove(fileName)
            
    def __generate_test_data(self) -> List[models.TimeRecord]:
        return [
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
        
    def __compare_collections(self, lhs : List[models.TimeRecord], rhs : List[models.TimeRecord]):  # noqa: E501
        self.assertCountEqual(
            lhs, 
            rhs, 
            "Collections should have same count of items")
        
        index = 0
        while index < lhs.__len__():
            self.assertEquals(
                lhs[index], 
                rhs[index], 
                f"Data differs in index {index}")
            index += 1