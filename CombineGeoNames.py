"""
2020-2021 Vacation Project
@author: Chanon Kachornvuthidej, kac016@csiro.au, chanon.kachorn@gmail.com
@Supervisors: Dr Alejandro Metke Jimenez, Alejandro.Metke@csiro.au and Dr Hoa Ngo Hoa.Ngo@csiro.au

Attempt to combine all json files produced by different GeoNames script into 1 FHIR format json.

NOTE: THE 7 DIGIT NUMBERS USED BELOW REPRESENT THE CONTINENTS LEVEL/COUNTRY LEVEL THAT WE WANT TO IGNORE, FUTURE
DEVELOPMENT WILL NEED TO UPDATE THESE VALUES!!!
"""

import json
from GeoNames1 import *
from GeoNames2 import *

countries1 = {}
countries2 = {}

# GET COUNTRIES LEVEL for the first file
with open('GlobalData(GeoNames1).json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        if location['display'] != "Earth" and (location['property'][0]['valueCode'] == '0000001' or
                location['property'][0]['valueCode'] == '0000002' or location['property'][0]['valueCode'] == '0000003' or
                location['property'][0]['valueCode'] == '0000004' or location['property'][0]['valueCode'] == '0000005' or
                location['property'][0]['valueCode'] == '0000006' or location['property'][0]['valueCode'] == '0000007'): # If this is country level, parent is Earth
            countries1[location['code']] = location['display']

# GET countries level for the second file
with open('newResultOutput.json') as json_file2:
    data = json.load(json_file2)
    for location in data['concept']:
        if location['display'] != "Earth" and (location['property'][0]['valueCode'] == '0151619' or
                location['property'][0]['valueCode'] == '0151620' or location['property'][0]['valueCode'] == '0151621' or
                location['property'][0]['valueCode'] == '0151622' or location['property'][0]['valueCode'] == '0151623' or
                location['property'][0]['valueCode'] == '0151624' or location['property'][0]['valueCode'] == '0151625'): # CHECK THESE NUMBERS, GOTTA BE BETWEEN 20 TO 26!!!
            countries2[location['code']] = location['display']

countries1_set = set(countries1.values()) # Use the set datastructure to remove duplicates
countries2_set = set(countries2.values())

in_second_but_not_first = countries2_set - countries1_set # find which locations appear in one file but not the other, then try to add it together
combined = list(countries1.values()) + list(in_second_but_not_first) # use 1 cause that's the one that is less



code_system = create_code_system_instance("complete", "draft", "CodeSystem for different administrative divisions around the world", True, FHIRDate(str(date.today())), "Ontology-CSIRO",
                                "http://csiro.au/geographic-locations", "0.4", "Location Ontology", "Chanon K.", True, "is-a", "http://csiro.au/geographic-locations?vs") # FHIRDate(str(date.today()))
root = Region2("Earth", None)
code_concept = create_code_system_concept_instance(code_system, root)
populate_code_system_concept_property_field(code_concept, "root", True)
populate_code_system_concept_property_field(code_concept, "deprecated", False)

continents_to_FHIR = create_continents_region2(code_system, root.FHIRCode)


states1 = {}
states2 = {}
# GET STATES
with open('GlobalData(GeoNames1).json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        for codes in countries1.keys():
            if location['display'] != "Earth" and location['property'][0]['valueCode'] == codes: # if parent is the country
                if states1.get(countries1.get(codes)) is None:
                    state = []
                else:
                    state = states1.get(countries1.get(codes))
                state.append((location['code'], location['display']))
                states1[countries1.get(codes)] = state # parent code (country) mapped to list containing tuples of current code and name (states)

with open('newResultOutput.json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        for codes in countries2.keys():
            if location['display'] != "Earth" and location['property'][0]['valueCode'] == codes: # if parent is the country
                if states2.get(countries2.get(codes)) is None:
                    state = []
                else:
                    state = states2.get(countries2.get(codes))
                state.append((location['code'], location['display']))
                states2[countries2.get(codes)] = state # parent code (country) mapped to list containing tuples of current code and name (states)

# For debugging
# print("------------------------------------------------------------------------------------------------------------")

combined_states = {}

# Attempt to combine the countries together
for country in combined:
    s12 = set()
    s1 = states1.get(country)
    s2 = states1.get(country)
    if s1 is not None:
        for element in s1:
            s12.add(element[1])
    if s2 is not None:
        for element in s2:
            s12.add(element[1])
    combined_states[country] = s12


# GET DISTRICTS Level from the files
district1 = {}
district2 = {}

with open('GlobalData(GeoNames1).json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        for country in states1.keys():
            for states in states1.get(country):
                if location['display'] != "Earth" and location['property'][0]['valueCode'] == states[0]: # if parent is the country
                    if district1.get(country+","+states[1]) is None:
                        district = []
                    else:
                        district = district1.get(country+","+states[1])
                    district.append((location['code'], location['display']))
                    district1[country+","+states[1]] = district # parent code (country) mapped to list containing tuples of current code and name (states)

with open('newResultOutput.json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        for country in states2.keys():
            for states in states2.get(country):
                if location['display'] != "Earth" and location['property'][0]['valueCode'] == states[0]:  # if parent is the country
                    if district2.get(country + "," + states[1]) is None:
                        district = []
                    else:
                        district = district2.get(country + "," + states[1])
                    district.append((location['code'], location['display']))
                    district2[country + "," + states[1]] = district  # parent code (country) mapped to list containing tuples of current code and name (states)





# SECOND VERSION, STILL IN DEVELOPMENT


import json

countries = {}
locations = []
country = None

# Get names of all countries
with open('newResultOutput.json') as json_file2:
    data = json.load(json_file2)
    for location in data['concept']:
        if location['display'] != "Earth" and (location['property'][0]['valueCode'] == '0151619' or
                                               location['property'][0]['valueCode'] == '0151620' or
                                               location['property'][0]['valueCode'] == '0151621' or
                                               location['property'][0]['valueCode'] == '0151622' or
                                               location['property'][0]['valueCode'] == '0151623' or
                                               location['property'][0]['valueCode'] == '0151624' or
                                               location['property'][0]['valueCode'] == '0151625' or
                                               location['property'][0]['valueCode'] == '0151626') and (
                location['code'] != '0151626' and
                location['code'] != '0151620' and
                location['code'] != '0151621' and
                location['code'] != '0151622' and
                location['code'] != '0151623' and
                location['code'] != '0151624' and
                location['code'] != '0151625'):  # CHECK THESE NUMBERS, GOTTA BE BETWEEN 20 TO 26!!!
            countries[location['code']] = location['display']

# print(countries)

# Get names of all states
states = {}
mark = False
with open('newResultOutput.json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        if location['code'] == "0003728": # end of the states section
            break
        elif location['code'] != "0000256" and not mark:
            continue
        mark = True
        for codes in countries.keys():
            if location['display'] != "Earth" and location['property'][0]['valueCode'] == codes: # if parent is the country
                if states.get(countries.get(codes)) is None:
                    state = []
                else:
                    state = states.get(countries.get(codes))
                state.append((location['code'], location['display']))
                states[countries.get(codes)] = state # parent code (country) mapped to list containing tuples of current code and name (states)
                break

# print(states)

# Get names of all districts
districts = {}
mark = False
with open('newResultOutput.json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        if location['code'] == "0045430":
            break
        elif location['code'] != "0003728" and not mark:
            continue
        mark = True

        for country in states.keys():
            found = False
            for state in states.get(country):
                if location['display'] != "Earth" and location['property'][0]['valueCode'] == state[0]:  # if parent is the country
                    if districts.get(country + "," + state[1]) is None:
                        district = []
                    else:
                        district = districts.get(country + "," + state[1])
                    district.append((location['code'], location['display']))
                    districts[country + "," + state[1]] = district  # parent code (country) mapped to list containing tuples of current code and name (states)
                    found = True
                    break
            if found:
                break
print(districts.keys())


# Get names of all suburbs
suburbs = {}
mark = False
with open('newResultOutput.json') as json_file1:
    data = json.load(json_file1)
    for location in data['concept']:
        print(location['code'])
        if location['code'] != '0045430' and not mark:
            continue
        mark = True

        for key in districts.keys():
            # print(key, '************************')
            # print(districts.get(key))
            found = False
            if districts.get(key) is not None:  # for some reason it's none, probably blank?
                for district in districts.get(key):
                    if location['display'] != "Earth" and location['property'][0]['valueCode'] == district[0]:  # if parent is the district
                        if suburbs.get(key + ',' + district[1]) is None:
                            suburb = []
                        else:
                            suburb = suburbs.get(key + ',' + district[1])
                        suburb.append(location['display']) # NOT AS TUPLE, could do tuple for futher levels
                        suburbs[key + ',' + district[1]] = suburb  # parent code (country) mapped to list containing tuples of current code and name (states)
                        found = True
                        break # already found it move on?
            if found:
                break

print(suburbs)

with open("GlobalDataNeighbours(Sparql).txt", "w") as out:
    out.write(json.dumps(suburbs))