from unittest import TestCase, main
from DataStructure.TimeCode import TimeCodeInMeasures, TimeCodeInSeconds
from DataStructure.util.UtilityClass import meter

meter44 = meter(num_beats=4, beat_unit=4)

timecode1 = TimeCodeInSeconds(5)
timecode2 = TimeCodeInMeasures(num_measure=2, num_beat=3)


class TestTimeCode(TestCase):
    def test_get_time_in_measure(self):
        self.assertEqual(timecode1.get_time_in_measure(num_second=5, bpm=120, mt = meter44), (2, 2))


if __name__ == "__main__":
    #unittest_expect_error()
    main()
