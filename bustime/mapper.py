"""Tools to convert dictionaries (returned by JSON), to actual objects."""

class JSONObject:
    """
    Lift a dictionary to an actual object type.
    >>> test = JSONObject({"key":"value","sub":{"subkey":"subvalue"}})
    >>> test.key
    'value'
    >>> test = JSONObject({"key":"value","sub":{"subkey":"subvalue"}})
    >>> test.sub.subkey
    'subvalue'
    """
    def __init__(self, jsondict, namemap=None, typemap=None):
        dct = dict()
        for k,v in jsondict.items():
            new_key = namemap(k) if namemap else k
            if type(v) == dict:
                dct[k] = JSONObject(v)
            else:
                dct[k] = typemap(newkey, v) if typemap else v
        self.__dict__ = dct

class Namemap:
    """
    Map old key names to new key names. Used to make the published JSON interface easier to use.
    >>> m = Namemap(**{"key":"new_key"})
    >>> m("key")
    'new_key'
    """
    def __init__(self, **kwargs):
        self.__map = kwargs

    def __call__(self, key):
        return self.__map.get(key, key)

class Typemap:
    """
    Conversion functions to apply to individual fields in a dictionary.
    >>> t = Typemap(**{"key":int})
    >>> t("key", "5")
    5
    """
    def __init__(self, **kwargs):
        self.__map = kwargs

    def __call__(self, key, value):
        nop = lambda x: x
        conv = self.__map.get(key, nop)
        return conv(value)

if __name__ == "__main__":
    import doctest
    doctest.testmod()