# BusTime Client
This is a simple Python3 client library for the BusTime API used by the Pittsburgh Port Authority. 

It depends on python-dateutil for date parsing.

    $ pip3 install python-dateutil

[Details](http://realtime.portauthority.org/bustime/home.jsp).

It should be usable for *any* BusTime-based transit API. Also depends on Google's 
DistanceMatrix API for doing distance calculations.

Example usage:

    >>> client = BusTime(BASE, API_KEY) #BASE is base URL for access
    >>> client.getroutes() #return a list of routes

Currently, core BusTime object is a mostly complete implementation of the BusTime API. It doesn't support locales, and it doesn't support getting predictions on a per-vehicle basis (getpredictions works with stops and routes).

The Stops object is a first attempt at building some more useful operations atop the simple BusTime library. It depends on an instance of the Distance object, which is a simple wrapper around Google's DistanceMatrix API.

My plans for this library are to focus more on interesting query operations, like the Stops object telling me the next busses to arrive in a given range, and *not* so much on being a 100% feature-complete wrapper around the BusTime REST API. 

Run the unit tests with:

    $ python3 -m bustime