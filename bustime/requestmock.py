from urllib.parse import urlparse, parse_qs
from io import StringIO
import json

class MockRequest:
    def getmethod(self, path):
        apiend = "v2/"
        start = path.find(apiend) + len(apiend)
        return path[start:]

    def urlopen(self, url):
        output = StringIO()
        parsed = urlparse(url)
        params = parse_qs(parsed.query)
        method = self.getmethod(parsed.path)
        print(method)
        s = getattr(self, method)(**params)
        output.write(s)
        output.seek(0)
        return output

    def gettime(self, **kwargs):
        return json.dumps(
            {"bustime-response": {"tm": "20141012 10:21:04"}}
        )