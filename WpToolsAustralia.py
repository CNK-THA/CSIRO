"""
2020-2021 Vacation Project
@author: Chanon Kachornvuthidej, kac016@csiro.au, chanon.kachorn@gmail.com
@Supervisors: Dr Alejandro Metke Jimenez, Alejandro.Metke@csiro.au and Dr Hoa Ngo Hoa.Ngo@csiro.au

Generate json containing neighbours of each Australian suburbs.
"""

import wptools
import json


locations = []

with open('AustralianLocations.json') as json_file:
    data = json.load(json_file)
    for location in data['concept']:
        if location['display'] != "Earth" and (location['code'] != '0001387' and
                                               location['code'] != '0001388' and
                                               location['code'] != '0001389' and
                                               location['code'] != '0001390' and
                                               location['code'] != '0001391' and
                                               location['code'] != '0001392' and
                                               location['code'] != '0001393' and
                                               location['code'] != '0000000'):  # Also skip Australia!
            # Not the contients label and not the country levels
            locations.append((location['display'], location['property'][0]['valueCode']))

neighbours = {}

# Similar to using SPARQL, construct the link (or pages name in this case) to query in Wikipedia
for country in locations:
    countryName = country[0].strip()
    remove_space = countryName.replace(" ", "_")  # replace spaces with underscore
    ink = None
    if country[1] == "0000002":
        link = remove_space + ', Australian Capital Territory'
    elif country[1] == "0000005":
        link = remove_space + ', New South Wales'
    elif country[1] == "0000006":
        link = remove_space + ', Northern Territory'
    elif country[1] == "0000007":
        link = remove_space + ', Queensland'
    elif country[1] == "0000008":
        link = remove_space + ', South Australia'
    elif country[1] == "0000009":
        link = remove_space + ', Tasmania'
    elif country[1] == "0000010":
        link = remove_space + ', Victoria'
    elif country[1] == "0000011":
        link = remove_space + ', Western Australia'
    else:
        # The islands and states skip!
        continue

    try:
        page = wptools.page(link) # retrieve the page and parse it, extract neighbouring info.
        so = page.get_parse()
        near = {}
        near['n'] = so.data['infobox']['near-n']
        near['ne'] = so.data['infobox']['near-ne']
        near['w'] = so.data['infobox']['near-w']
        near['nw'] = so.data['infobox']['near-nw']
        near['e'] = so.data['infobox']['near-e']
        near['sw'] = so.data['infobox']['near-sw']
        near['se'] = so.data['infobox']['near-se']
        near['s'] = so.data['infobox']['near-s']
        neighbours[link] = near
    except LookupError:
        print("LookupError")
        pass
    except:
        print("exception")
        pass

with open("AustralianNeighbours(Wptools).json", "w") as out:
    out.write(json.dumps(neighbours))




