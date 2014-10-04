# -*- coding: iso-8859-15 -*-
from TwitterAPI import placefinder

__author__ = 'Alvaro Ortigosa <alvaro.ortigosa@uam.es>'

import unittest


class PlaceFinderTests(unittest.TestCase):
    # def test_SimpleGeocode(self):
    #     result = placefinder.geocode("1001 E Playa Del Norte, Tempe AZ 85281")
    #
    #     # fetch the first result
    #     result = result[0]
    #
    #     self.assertEqual(result["latitude"], "33.435493")
    #
    # def test_BogusSimpleGeocodeRaisesNoResults(self):
    #     self.assertRaises(placefinder.NoResultsException, placefinder.geocode, "9u523u4biwhbdfuwfwejb")

    def test_AirPortCode(self):
        result = placefinder.geocode("España")

        #result = result[0]
        print "result=%s" % (result,)
        self.assertEqual(result['name'], "España")

    # def test_FlagsForcesJson(self):
    #     result = placefinder.geocode(name="SFO", flags="XRT")
    #
    #     result = result[0]
    #     self.assertEqual(result["line1"], "San Francisco International Airport")
    #
    # def test_StructuredGeocode(self):
    #     result = placefinder.geocode(house="1001",
    #                                  street="Playa Del Norte Dr",
    #                                  city="Tempe",
    #                                  state="AZ",
    #                                  country="USA")
    #
    #     result = result[0]
    #
    #     self.assertEqual(result["latitude"], "33.435493")

if __name__ == '__main__':
    unittest.main()