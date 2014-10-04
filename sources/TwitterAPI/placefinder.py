# -*- coding: iso-8859-15 -*-
__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'
import json

import httplib2

from TwitterAPI.getAuthorizations import GetAuthorizations


http = httplib2.Http()

_base_uri = "http://where.yahooapis.com/v1/"
_decode = json.loads

locale = "es-ES"

class NoResultsException(Exception):
    pass

cache = {'Spain':23424950, 'World':1, 'US':23424977}

#def geocode(q=None, flags="JRT", gflags="AC", **kwargs):
def geocode(name):
    """
    Si no encuentra name retorna los trends mundiales
    """
    if name in cache:
        return cache[name]
    authorizator = GetAuthorizations()
    uri = _base_uri + "places.q(%s)?format=json&appid=%s" % (name, authorizator.get_yahoo_geo_api_auth())
    print "uri %s", uri
    response, content = http.request(uri)
    #print "content: %s" % (content)
    content = _decode(content)
    return content['places']['place'][0]
    # if content["ResultSet"]["Found"] == 0:
    #     raise NoResultsException("Found 0 Results")
    # else:
    #     return content["ResultSet"]["Results"]