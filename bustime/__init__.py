import urllib.request as request
import json
import dateutil.parser

base = "http://realtime.portauthority.org/bustime/api/v2/{method}?key={key}&format={format}"
max_ids = 10
class Stops:
    """Manage stop data. Depends on a BusTime API object and a Distance API client.
    """
    def __init__(self, busapi, distanceapi):
        self.api = busapi
        self.dist = distanceapi

    def stops_in_range(self, route, direction, location, distance=400, duration=None):
        """Find all the stops for a given route and direction in range of a lat/long coordinate.
        Location must be a dict in the form {lat:40.1234, lon:80.1234}.

        Distance is measured in meters, duration is measured in seconds. If duration is supplied,
        it will use the duration returned by the distance API, otherwise it will use the distance.
        """
        stops = self.api.getstops(route, direction)
        distances = self.dist.distance_points(location, *stops)
        if duration:
            distance_item = lambda x: x[1]["value"] <= duration
        else:
            distance_item = lambda x: x[0]["value"] <= distance
        return [s[2] for s in distances if distance_item(s)]




class BusTime:
    """Wrapper around the BusTime API service. Handles all of the communication, parsing of JSON, and extracting key data from
    BusTime API responses."""
    def __init__(self, apibase, key):
        self.key = key
        self.apibase = apibase
    
    def __callrest(self, method, **kwargs):
        """Invoke a RESTful method. Params passed as kwargs are converted to URL parameters"""
        url = self.apibase.format(key=self.key, format="json", method=method)
        for (k,v) in kwargs.items():
            url += "&{0}={1}".format(k,v)
        data = request.urlopen(url).read()
        return json.loads(data.decode("UTF8"))

    def gettime(self):
        """Get the bustime server's system time. Returns a datetime object."""
        resp = self.__callrest("gettime")
        dt = resp["bustime-response"]["tm"]
        return dateutil.parser.parse(dt)

    def getdirections(self, route):
        """List the directions for a route. In Pittsburgh, this is always ["OUTBOUND","INBOUND"]"""
        resp = self.__callrest("getdirections", rt=route)
        return [d["dir"] for d in resp["bustime-response"]["directions"]]

    def getstops(self, route, direction):
        """List the stops for a route, going in a certain direction. BusTime returns a JSON object, which converts to
        a dictionary like:
        {'stpid': '2564', 'stpnm': '5th Ave  at Meyran Ave', 'lon': -79.959239533731, 'lat': 40.441172012068}"""
        resp= self.__callrest("getstops", rt=route, dir=direction)
        return resp["bustime-response"]["stops"]

    def getpredictions(self, stopid, routes=None, top=10):
        if routes:
            rt = ",".join(routes)
            resp = self.__callrest("getpredictions", stpid=stopid, top=top, rt=rt)    
        else:
            resp = self.__callrest("getpredictions", stpid=stopid, top=top)
        return resp["bustime-response"]["prd"]

class Distance:
    def __init__(self, google_key, window_size = 45):
        self.key = google_key
        self.window_size = window_size

    def format_point(self, point):
        pointfmt = "{lat},{lon}"
        return pointfmt.format(**point)

    def join_points(self, *points):
        return "|".join([self.format_point(p) for p in points])

    def distance_points(self, origin, *destinations):
        """Given an origin and a list of destinations (in lat/lon form), returns a list of 3-tuples in the form "[(distance, duration, stop)]".
        Distance and duration are dicts in the form {"value":n, "text":s}. Distance is in meters, duration in seconds.
        The stop is a dictionary like: {'stpid': '2564', 'stpnm': '5th Ave  at Meyran Ave', 'lon': -79.959239533731, 'lat': 40.441172012068}"""
        l = len(destinations) #we window the call so that we're not trying to pass 1,000 points on the URL and getting 400 errors. 45 appears to be a good default size.
        if l < self.window_size:
            return self.__distance_points(origin, *destinations)
        else:
            return list(self.__distance_points(origin, *destinations[:self.window_size])) + list(self.distance_points(origin, *destinations[self.window_size:]))

    def __distance_points(self, origin, *destinations):
        o = self.format_point(origin)
        dests = self.join_points(*destinations)
        base = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={0}&destinations={1}&mode=walking&key={2}" #I should externalize this.
        url = base.format(o, dests, self.key)
        raw = request.urlopen(url).read()
        data = json.loads(raw.decode("UTF8"))
        data = data["rows"][0]["elements"]
        return zip([e["distance"] for e in data], [e["duration"] for e in data], destinations)

