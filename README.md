# BusTime Client
This is a simple Python3 client for the BusTime API used by the Pittsburgh Port Authority. 
It has no external dependencies.

[Details](http://realtime.portauthority.org/bustime/home.jsp).

It should be usable for *any* BusTime-based transit API. Also depends on Google's 
DistanceMatrix API for doing distance calculations.

Example usage:

    >>> client = BusTime(BASE, API_KEY) #BASE is base URL for access
    >>> client.getroutes() #return a list of routes