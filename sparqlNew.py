
import json

countries = {}
locations = []
country = None

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

with open("allNames.txt", "w") as out:
    out.write(json.dumps(suburbs))
    
