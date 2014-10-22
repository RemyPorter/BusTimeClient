from urllib.parse import urlparse, parse_qs
from io import BytesIO
import json

class MockRequest:
    def getmethod(self, path):
        apiend = "v2/"
        start = path.find(apiend) + len(apiend)
        return path[start:]

    def urlopen(self, url):
        output = BytesIO()
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        method = self.getmethod(parsed.path)
        assert("key" in params)
        s = getattr(self, method)(**params)
        output.write(s.encode("UTF8"))
        output.seek(0)
        return output

    def gettime(self, **kwargs):
        return json.dumps(
            {"bustime-response": {"tm": "20141012 10:21:04"}}
        )

    def getdirections(self, **kwargs):
        return json.dumps(
            {"bustime-response": 
                {"directions": [{"dir":"INBOUND"}, {"dir":"OUTBOUND"}]}
            }
        )

    def getstops(self, **kwargs):
        return json.dumps(
            {
                "bustime-response": 
                {"stops": [
                {'stpid': '2564', 'stpnm': '5th Ave  at Meyran Ave',
                'lon': -79.959239533731, 'lat': 40.441172012068}]}
            })

    def getpredictions(self, **kwargs):
        return json.dumps({
            "bustime-response":{
                "prd": [{'rt': '71C', 'typ': 'A', 
                'prdctdn': '5', 'prdtm': '20141022 12:37', 
                'rtdir': 'INBOUND', 'zone': '', 
                'des': 'Downtown', 'dly': False, 
                'dstp': 4198, 'stpnm': '5th Ave at Chesterfield Rd', 
                'stpid': '38', 'tatripid': '159261', 
                'tmstmp': '20141022 12:31', 'tablockid': '071C-150', 
                'vid': '5678'}]}
            })

    def getvehicles(self, **kwargs):
        return json.dumps({
            "bustime-response":{
                "vehicle":[{'tablockid': '071C-148', 'pid': 2363, 
                'tatripid': '159264', 'zone': '', 'des': 'Downtown', 
                'dly': False, 'spd': 0, 'pdist': 17607, 'hdg': '299', 
                'tmstmp': '20141022 12:52', 'lat': '40.46042251586914', 
                'rt': '71C', 'vid': '5669', 'lon': '-79.92157814719461'}]
            }
            })



















