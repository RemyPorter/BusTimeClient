# BusTime Client
This is a simple Python3 client for the BusTime API used by the Pittsburgh Port Authority. 
It has no external dependencies.

[Details](http://realtime.portauthority.org/bustime/home.jsp).

It should be usable for *any* BusTime-based transit API. Also depends on Google's 
DistanceMatrix API for doing distance calculations.

Example usage:

    >>> client = BusTime("http://realtime.portauthority.org/bustime/api/v2/{method}?key={key}&format={format}", API_KEY)
    >>> client.getroutes() #return a list of routes