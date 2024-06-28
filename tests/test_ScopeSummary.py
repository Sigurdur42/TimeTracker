import unittest
from datetime import datetime

from timetracking.models import ScopeSummary


class ScopeSummaryTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_verify_scope_as_month(self):
        self.assertEqual(
            "01.2023",
            ScopeSummary(datetime(2023, 1, 2), 0, 0).scope_as_month())

        self.assertEqual(
            "12.2023",
            ScopeSummary(datetime(2023, 12, 2), 0, 0).scope_as_month())

    def test_verify_scope_as_year(self):
        self.assertEqual(
            "2023",
            ScopeSummary(datetime(2023, 1, 2), 0, 0).scope_as_year())

        self.assertEqual(
            "2023",
            ScopeSummary(datetime(2023, 12, 2), 0, 0).scope_as_year())

    def test_verify_scope_as_day(self):
        self.assertEqual(
            "02.01.2023",
            ScopeSummary(datetime(2023, 1, 2), 0, 0).scope_as_day())

        self.assertEqual(
            "02.12.2023",
            ScopeSummary(datetime(2023, 12, 2), 0, 0).scope_as_day())

    def test_verify_working_hours(self):
        self.assertAlmostEqual(
            12.5,
            ScopeSummary(datetime(2023, 1, 2), 12.5 * 60 * 60, 0).working_hours())

    def test_verify_overtime(self):
        self.assertAlmostEqual(
            -4.5,
            ScopeSummary(datetime(2023, 1, 2), 0, -4.5 * 60 * 60).overtime_hours())
