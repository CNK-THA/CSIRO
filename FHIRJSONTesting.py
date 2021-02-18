"""
2020-2021 Vacation Project
@author: Chanon Kachornvuthidej, kac016@csiro.au, chanon.kachorn@gmail.com
@Supervisors: Dr Alejandro Metke Jimenez, Alejandro.Metke@csiro.au and Dr Hoa Ngo Hoa.Ngo@csiro.au

Test whether the produced JSON is correctly produced (FHIR format and is OnToServer ready)
"""

import unittest
import os
import json


currentCounter = "0000000"
allLocations = []
allParents = set()
tmp = []
data = None

class JsonTesting(unittest.TestCase):
    def test_output_file_format(self):
        self.assertTrue(os.path.exists('newResultOutput.json'), "File not found")
        self.assertTrue(os.stat("newResultOutput.json").st_size != 0, "File is Empty")

    @classmethod
    def setUpClass(cls):
        global currentCounter, allLocations, allParents, tmp, data

        with open('newResultOutput.json') as json_file:
            data = json.load(json_file)
            for location in data['concept']:
                if location['display'] != "Earth":
                    allParents.add(location['property'][0]['valueCode'])
                allLocations.append(location['code'])

            allLocations.sort()  # in ascending order

    def test_all_location_code_exist(self): # test that all location code exist from 000000 - XXXXXXX <-- as shown in the CodeSystemConcept count
        global currentCounter, allLocations, allParents, tmp, data

        if len(allLocations) != int(data['count']):
            print("got", len(allLocations), "expecting", int(data['count']))
            self.fail("Not equal")

        for index in range(0, int(data['count'])):  # TEST THAT ALL CODES EXIST
            if allLocations[0] != currentCounter:
                self.fail("currently " + allLocations[0] + " expecting " + currentCounter)
            tmp.append(allLocations.pop(0))

            currentCounter = '%07d' % (int(currentCounter) + 1)

    def test_all_parent_code_exist(self):
        global currentCounter, allLocations, allParents, tmp, data

        for local in allParents:  # TEST THAT ALL PARENT CODE PROPERTY HAS A LOCATION WITH THAT CODE
            self.assertTrue(tmp.__contains__(local))

if __name__ == '__main__':
    unittest.main()