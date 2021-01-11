import wptools
import json

# https://github.com/siznax/wptools/wiki/Examples#get-all-the-page-info
# https://github.com/siznax/wptools/
locations = []

with open('newResultOutput2.json') as json_file:
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
for country in locations:
    countryName = country[0].strip()
    remove_space = countryName.replace(" ", "_")
    ink = None
    if country[1] == "0000002":  # NSW DOESN'T NEED THE EXTENSION??
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
        print(country)  # The islands and states skip!
        continue
    try:
        print(link)
        page = wptools.page(link) # get the last one
        # p = page.get_query()
        # print(page)
        # p = page.get_more()
        # print(page.data)
        so = page.get_parse()

        near = {}
        near['n'] = so.data['infobox']['near-n']
        near['ne'] = so.data['infobox']['near-ne']
        near['w'] = so.data['infobox']['near-w']
        near['e'] = so.data['infobox']['near-e']
        near['sw'] = so.data['infobox']['near-sw']
        near['s'] = so.data['infobox']['near-s']
        neighbours[link] = near
        # print(neighbours)
        # print(type(txt))
        # print(txt.split("\n"))
        # input('')
    except LookupError:
        print("LookupError")
        pass
    except:
        print("exception")
        pass

with open("neighboursAustralia.json", "w") as out:
    out.write(json.dumps(neighbours))





# print(so)
# infobox = so.data['infobox']
# print(infobox)
# printt(type(infobox))



