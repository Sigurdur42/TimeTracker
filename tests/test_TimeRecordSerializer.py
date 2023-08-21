from typing import List
import unittest
from src.models import TimeRecord
import os
from src.serializers import TimeRecordSerializer
import tempfile
import uuid


class TimeTrackerTests(unittest.TestCase):
    def test_generate_and_read_csv_in_memory(self):
        data2Write = self.__generate_test_data()
        writer = TimeRecordSerializer()
        data = writer.generate_csv(data2Write)
        print(f"Generated CSV: {data}")

        written_data = writer.read_csv(data)
        print(f"Read data: {written_data}")

        self.__compare_collections(data2Write, written_data)

    def test_generate_and_read_csv_from_file(self):
        data2Write = self.__generate_test_data()
        writer = TimeRecordSerializer()
        fileName = tempfile.mktemp()
        print(f"using file: '{fileName}'")
        writer.write_csv_to_file(fileName, data2Write)
        readData = writer.read_from_csv_file(fileName)
        self.__compare_collections(data2Write, readData)
        os.remove(fileName)

    def test_try_reading_nonexistent_file(self):
        reader = TimeRecordSerializer()
        # Ensure that this file does not exist
        file_name = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

        read_data = reader.read_from_csv_file(file_name)
        self.assertEqual(0, len(read_data), f"Expected an empty list -> {read_data}")

    @staticmethod
    def __generate_test_data() -> List[TimeRecord]:
        serializer = TimeRecordSerializer()
        data = [
            "01.01.2020;8:30;12:00",
            "01.01.2020;12:30;16:00;False",

            "02.01.2020;8:00;12:00;True",
            "02.01.2020;12:30;15:00;True",

            "03.01.2020;8:00;12:00",
            "03.01.2020;12:30;15:00",
        ]
        return serializer.read_csv_from_lines(data)

    def __compare_collections(
        self, lhs: List[TimeRecord], rhs: List[TimeRecord]
    ):  # noqa: E501
        self.assertCountEqual(lhs, rhs, "Collections should have same count of items")

        index = 0
        while index < lhs.__len__():
            self.assertEqual(lhs[index], rhs[index], f"Data differs in index {index}")
            index += 1
