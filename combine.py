import json

countries1 = []
countries2 = []

with open('resultSample.json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        if location['display'] != "Earth" and location['property'][0]['valueCode'] == '0000000': # If this is country level, parent is Earth
            countries1.append(location['display'])
    #         allParents.add(location['property'][0]['valueCode'])
    #     allLocations.append(location['code'])
    #
    # allLocations.sort()  # in ascending order

# with open('newResultOutput.json') as json_file2:
#     data = json.load(json_file2)
#     for location in data['concept']:
#         if location['display'] != "Earth":
#             allParents.add(location['property'][0]['valueCode'])
#         allLocations.append(location['code'])
#
#     allLocations.sort()  # in ascending order