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
