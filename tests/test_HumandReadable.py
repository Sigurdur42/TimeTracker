from unittest import TestCase

from timetracking.models import HumanReadable


class HumanReadableTests(TestCase):
    def setUp(self):
        pass

    def test_seconds_to_human_readable(self):
        self.assertEqual("-02:00", HumanReadable.seconds_to_human_readable(-2 * 60 * 60))
        self.assertEqual("-00:10", HumanReadable.seconds_to_human_readable(-10 * 60))
        self.assertEqual("00:30", HumanReadable.seconds_to_human_readable(0.5 * 60 * 60))
        self.assertEqual("01:30", HumanReadable.seconds_to_human_readable(1.5 * 60 * 60))
        self.assertEqual("00:00", HumanReadable.seconds_to_human_readable(0 * 60 * 60))
        self.assertEqual("02:00", HumanReadable.seconds_to_human_readable(2 * 60 * 60))

    def test_seconds_to_decimal_display(self):
        self.assertEqual("0.50", HumanReadable.seconds_to_decimal_display(0.5 * 60 * 60))
        self.assertEqual("8.75", HumanReadable.seconds_to_decimal_display(8.75 * 60 * 60))
