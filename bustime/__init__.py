"""This is a simple wrapper object around the BusTime API."""

import urllib.request as request
import json
import dateutil
import dateutil.parser
from .distance import Distance
from .stops import Stops

BASE = "http://realtime.portauthority.org/bustime/api/v2/{method}?key={key}&format={format}"

class BustimeError(Exception): pass
class BustimeParameterError(BustimeError): pass

_request_factory = lambda: request


class BusTime:
    """Wrapper around the BusTime API service. Handles all of the communication,
    parsing of JSON, and extracting key data from
    BusTime API responses."""
    def __init__(self, apibase, key, *, factory=_request_factory):
        self.key = key
        self.apibase = apibase
        self.request = factory()

    def buildurl(self, method, **kwargs):
        """Generate the URL for the restful methods."""
        url = self.apibase.format(key=self.key, format="json", method=method)
        for (k, v) in kwargs.items():
            url += "&{0}={1}".format(k, v)
        return url

    def __callrest(self, method, **kwargs):
        """Invoke a RESTful method.
        Params passed as kwargs are converted to URL parameters"""
        url = self.buildurl(method, **kwargs)
        data = self.request.urlopen(url).read()
        jd = json.loads(data.decode("UTF8"))
        resp = jd["bustime-response"]
        if "error" in resp.keys():
            raise BustimeError(resp["error"][0]["msg"])
        return resp

    def gettime(self):
        """Get the bustime server's system time. Returns a datetime object."""
        resp = self.__callrest("gettime")
        dt = resp["tm"]
        return dateutil.parser.parse(dt)

    def getdirections(self, route):
        """List the directions for a route.
        In Pittsburgh, this is always ["OUTBOUND","INBOUND"]"""
        resp = self.__callrest("getdirections", rt=route)
        return [d["dir"] for d in resp["directions"]]

    def getstops(self, route, direction):
        """List the stops for a route, going in a certain direction.
        BusTime returns a JSON object, which converts to
            a dictionary like:
        {'stpid': '2564', 'stpnm': '5th Ave  at Meyran Ave',
        'lon': -79.959239533731, 'lat': 40.441172012068}"""
        resp = self.__callrest("getstops", rt=route, dir=direction)
        return resp["stops"]

    def getpredictions(self, stopid, routes=None, top=10):
        """Return predictions for a stop."""
        if routes:
            rt = ",".join(routes)
            resp = self.__callrest("getpredictions", stpid=stopid,
                    top=top, rt=rt)
        else:
            resp = self.__callrest("getpredictions", stpid=stopid, top=top)
        return resp["prd"]

    def getvehicles(self, vehicles=None, routes=None, resolution="S"):
        """Returns vehicles, either selected by ID or by route numbers.
        Resolution is the time resolution- S for seconds, M for minutes"""
        if vehicles and routes:
            raise BustimeParameterError("Supply vehicles or routes, but not both.")
        if not vehicles and not routes:
            raise BustimeParameterError("Vehicles or routes are required.")
        kwargs = dict()
        if vehicles:
            kwargs["vid"] = ",".join([str(v) for v in vehicles])
        if routes:
            kwargs["rt"] = ",".join(routes)
        kwargs["resolution"] = resolution
        resp = self.__callrest("getvehicles", **kwargs)
        return resp["vehicle"]

    def getroutes(self, feed=None):
        """Lists the routes in the system. The dictionary is like:
        {'rt': '12', 'rtnm': 'MCKNIGHT', 'rtclr': '#cc00cc'}"""
        if feed:
            resp = self.__callrest("getroutes", rtpidatafeed=feed)
        else:
            resp = self.__callrest("getroutes")
        return resp["routes"]

    def getpatterns(self, patterns=None, routes=None):
        if patterns and routes:
            raise BustimeParameterError("Supply pattern ids or route names, but not both.")
        if not patterns and not routes:
            raise BustimeParameterError("Pattern ids or routes are required")
        kwargs = dict()
        if patterns:
            kwargs["pid"] = ",".join([str(p) for p in patterns])
        if routes:
            kwargs["rt"] = ",".join(routes)
        return self.__callrest("getpatterns", **kwargs)["ptr"]

    def getservicebulletins(self, **kwargs):
        params = dict()
        if not "routes" in kwargs and not "stops" in kwargs:
            raise BustimeParameterError("Routes and/or stops are required.")
        if "routes" in kwargs:
            params["rt"] = ",".join(kwargs["routes"])
        if "stops" in kwargs:
            params["stpid"] = ",".join(kwargs["stops"])
        if "direction" in kwargs:
            params["rtdir"] = kwargs["direction"]
        return self.__callrest("getservicebulletins", **params)["sb"]

    def getrtpidatafeeds(self):
        return self.__callrest("getrtpidatafeeds")["rtpidatafeeds"]

class URLTest(unittest.TestCase):
    def setUp(self):
        self.bustime = BusTime(BASE, "NOKEY")
    def test_method(self):
        method = self.bustime.buildurl("test_method", **{})
        self.assertEqual(method, "http://realtime.portauthority.org/bustime/api/v2/test_method?key=NOKEY&format=JSON")

if __name__ == '__main__':
    unittest.main()
