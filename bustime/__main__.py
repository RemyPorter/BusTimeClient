import unittest
import dateutil
import dateutil.parser
from . import BusTime, BASE
from .requestmock import MockRequest

class URLTest(unittest.TestCase):
    def setUp(self):
        self.bustime = BusTime(BASE, "NOKEY")
    def test_method(self):
        method = self.bustime.buildurl("test_method", **{})
        self.assertEqual(method, 
            "http://realtime.portauthority.org/bustime/api/v2/test_method?key=NOKEY&format=json")

    def test_params(self):
        method = self.bustime.buildurl("test_method", **{"param1":5, "param2":10})
        self.assertTrue(method ==
            "http://realtime.portauthority.org/bustime/api/v2/test_method?key=NOKEY&format=json&param1=5&param2=10" or
            method == "http://realtime.portauthority.org/bustime/api/v2/test_method?key=NOKEY&format=json&param2=10&param1=5")

class MockedTest(unittest.TestCase):
    def setUp(self):
        self.bustime = BusTime(BASE, "NOKEY", factory=MockRequest)

    def test_time(self):
        time = self.bustime.gettime()
        self.assertEqual(time, dateutil.parser.parse("20141012 10:21:04"))

    def test_directions(self):
        dirs = self.bustime.getdirections("71C")
        self.assertEqual(len(dirs), 2)
        self.assertTrue("INBOUND" in dirs and "OUTBOUND" in dirs)

    def test_stops(self):
        stops = self.bustime.getstops("71C", "INBOUND")
        self.assertEqual(stops[0]["stpid"], '2564')

    def test_predictions(self):
        predict = self.bustime.getpredictions("2564", ["71C"])
        self.assertEqual(len(predict), 1)
        self.assertEqual(predict[0]["rt"], "71C")


if __name__ == '__main__':
    unittest.main()