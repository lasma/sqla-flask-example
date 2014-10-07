import datetime

import geoalchemy as ga
from shapely.wkb import loads
from common.utils.time import time_to_string

def flatten_unicode_keys(d):
    """Convert unicode dictionary to regular string dictionary"""
    for k in d:
        if isinstance(k, unicode):
            v = d[k]
            del d[k]
            d[str(k)] = v


def dict_keys_to_unicode(d):
    """Convert string dictionary keys to unicode keys"""
    if d is None:
        return None

    for k in d:
        if isinstance(k, str):
            v = d[k]
            del d[k]
            d[unicode(k)] = v


def dict_to_unicode(d):
    """Convert string dictionary to unicode dictionary"""
    if d is None:
        return None

    for k in d:
        if isinstance(k, str):
            v = d[k]
            del d[k]
            if isinstance(v, str):
                v = unicode(v)
            d[unicode(k)] = v

def get_nested_property(data, map):
    """Access property in dictionary using specified map for property drill-down.

    @param data {dict} dictionary from which to access property using path map
    @param map {list} list of dictionary nodes to drill to

    http://stackoverflow.com/questions/14692690/access-python-nested-dictionary-items-via-a-list-of-keys
    """
    #return reduce(dict.__getitem__, path, d)
    return reduce(lambda d, k: d[k], map, data)


def serializable(dictionary):
    """Convert python dictionary possibly containing complex data types
    (datetimes, binary geometry types) to a dictionary with simplified
    data types (strings, integers) that is JSON serializable.

    The goal is to produce Python dictionary that could be automatically
    jsonified by flask framework on it's automated http method
    (get, post, put, delete) return.

    @param dictionary: objects to be serialized

    @return:  json serializable dictionary

    *TODO*: extend this method to simplify/stringify more object types.
    """

    new_dict = {}

    for key, value in dictionary.iteritems():

        # print "Record type is: ", type(value)

        # Converts unicode string to Python literal structures: strings, numbers, tuples etc.
        if type(value) is unicode:
            new_dict[key] = value

        # Stringify datetime values
        elif type(value) is datetime.datetime:
            new_dict[key] = time_to_string(value)  # value.strftime("%Y-%m-%dT%H:%M:%S.") + value.strftime("%f")[:3] + "Z"

        # Stringify date values
        elif type(value) is datetime.date:
            new_dict[key] = time_to_string(value)  # value.strftime("%Y-%m-%dT%H:%M:%S.") + value.strftime("%f")[:3] + "Z"

        # Handle conversion of generic geometry types to geojson
        elif isinstance(value, ga.SpatialElement) is True:
            wkt = loads(str(value.geom_wkb)).wkt
            geojson = ga.utils.from_wkt(wkt)
            new_dict[key] = geojson

        else:
            # Grab value "as is" and add to the dictionary.
            # If value is a custom type that does not have string representation
            # then an error will be thrown (by flask).
            # You should add the new type here providing conversion to simple
            # (string, numeric) data structure
            new_dict[key] = value

    return new_dict