import unittest
import os
import json

class JsonTesting(unittest.TestCase):

    def test_output_file_format(self):
        self.assertTrue(os.path.exists('resultSample.json'), "File not found")
        self.assertTrue(os.stat("resultSample.json").st_size != 0, "File is Empty")

    def test_all_code_exist(self):
        with open('resultSample.json') as json_file:
            data = json.load(json_file)

            currentCounter = "0000000"
            allLocations = []
            allParents = set()
            tmp = []


            for location in data['concept']:
                if location['display'] != "Earth":
                    allParents.add(location['property'][0]['valueCode'])
                allLocations.append(location['code'])
            allLocations.sort()  # in ascending order

            if len(allLocations) != int(data['count']):
                self.fail("Not equal")

            for index in range(0, int(data['count'])):  # TEST THAT ALL CODES EXIST
                if allLocations[0] != currentCounter:
                    self.fail("currently " + allLocations[0] + " expecting " + currentCounter)
                tmp.append(allLocations.pop(0))

                currentCounter = '%07d' % (int(currentCounter) + 1)


            for local in allParents:  # TEST THAT ALL PARENT CODE PROPERTY HAS A LOCATION WITH THAT CODE
                self.assertTrue(tmp.__contains__(local))

if __name__ == '__main__':
    unittest.main()
