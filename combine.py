import json

countries1 = []
countries2 = []

with open('resultSample.json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        if location['display'] != "Earth" and (location['property'][0]['valueCode'] == '0000001' or
                location['property'][0]['valueCode'] == '0000002' or location['property'][0]['valueCode'] == '0000003' or
                location['property'][0]['valueCode'] == '0000004' or location['property'][0]['valueCode'] == '0000005' or
                location['property'][0]['valueCode'] == '0000006' or location['property'][0]['valueCode'] == '0000007'): # If this is country level, parent is Earth
            countries1.append(location['display'])
    #         allParents.add(location['property'][0]['valueCode'])
    #     allLocations.append(location['code'])
    #
    # allLocations.sort()  # in ascending order

print(len(countries1))
print(countries1)
# with open('newResultOutput.json') as json_file2:
#     data = json.load(json_file2)
#     for location in data['concept']:
#         if location['display'] != "Earth":
#             allParents.add(location['property'][0]['valueCode'])
#         allLocations.append(location['code'])
#
#     allLocations.sort()  # in ascending order