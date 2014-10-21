"""Convenience methods for working with stop data.
Uses BusTime API and Distance API through dependency injection."""
class Stops:
    """Manage stop data.
    Depends on a BusTime API object and a Distance API client.
    """
    def __init__(self, busapi, distanceapi):
        self.api = busapi
        self.dist = distanceapi

    def stops_in_range(self, route, direction, location,
        distance=400, duration=None):
        """Find all the stops for a given route and direction
        in range of a lat/long coordinate.
        Location must be a dict in the form {lat:40.1234, lon:80.1234}.

        Distance is measured in meters, duration is measured in seconds.
        If duration is supplied, it will use the duration returned
        by the distance API, otherwise it will use the distance.
        """
        stops = self.api.getstops(route, direction)
        distances = self.dist.distance_points(location, *stops)
        if duration:
            distance_item = lambda x: x[1]["value"] <= duration
        else:
            distance_item = lambda x: x[0]["value"] <= distance
        return [s[2] for s in distances if distance_item(s)]

    def next_busses(self, route, direction, location, 
        distance=400, duration=None):
        """Check predictions for nearby stops, sorted by arrivals."""
        stops = self.stops_in_range(route, direction, 
            location, distance, duration)
        ids = [s["stpid"] for s in stops]
        predictions = self.__getpredics(ids, [route], direction)
        return predictions

    def __getpredics(self, ids, route, direction):
        if len(ids) <= 10:
            return self.api.getpredictions(",".join(ids),
                route)
        else:
            return self.api.getpredictions(",".join(ids[:10]),
                route) + self.__getpredics(ids[10:], route, direction)

