import json
from pathlib import Path

# from pykson import JsonObject, IntegerField, StringField, ObjectListField



class Country:
    def __init__(self, countryName):
        self.countryName = countryName
        self.states = {}
        self.test = {"CountryName":self.countryName,"States":self.states}
        
    def add_region(self, region):
        key = region.regionCode
        if self.states.get(key) is None:
            self.states[key] = region
        
    def toJSON(self):

        return json.dumps(self, default=lambda o: o.test, # was __dict__
            sort_keys=True, indent=4)


class Region:
    def __init__(self, regionName, regionCode, parent):
        self.regionName = regionName
        self.regionCode = regionCode
        self.parentCode = parent
        self.subRegions = {}
        self.test = {"Region_Name":self.regionName, "Sub_Regions":self.subRegions}
        # self.__dict__ = {"testing":123}

    def add_sub_region(self, region):
        key = region.regionName
        if self.subRegions.get(key) is None:
            self.subRegions[key] = region

    def __eq__(self, other):
        return self.regionName == other.regionName

    def __hash__(self):
        return hash(self.regionName)

    def __str__(self):
        return self.regionName + ", " + self.regionCode + ", "

    # def __dict__(self):
    #     return {"name": "Dell Alienware", "processor": "Intel Core i7", "hdd": 512, "ram": 8, "cost": 2500.0}


class SmallestRegion:
    def __init__(self, regionName, parent):
        self.regionName = regionName
        self.parentCode = parent
        self.test = self.regionName

    def __eq__(self, other):
        return self.regionName == other.regionName

    def __hash__(self):
        return hash(self.regionName)

    def __str__(self):
        return self.regionName + ", " + self.regionCode + ", "



current = None
countriesList = {}


temporaryList = []
temporaryList3 = [] #level 3
with open("countryInfo.txt", 'r', encoding="utf8") as countryFile:
    lineNumber = 0
    for line1 in countryFile:
        lineNumber += 1
        if lineNumber < 51: #DATA STARTS AT LINE 51
            continue
        l = line1.split('\t')
        countriesList[l[0]] = l[4]




with open("allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile: #str(Path.home())+"/Downloads/

    for line in dataFile:
        d = line.split("\t")



        
            
        if len(d) != 19: # Expecting 19 columns
            print(d)
            input("STOP")
        if d[6] != 'P' and d[6] != 'A': #ONLY GET CLASS A INFORMATION
            continue

        # try:
        #     d.index("AU")
        #     d.index("PPLX")
        #     # d.index("ADM3")
        #     # print(d[7])
        #     # print(d[7] == "ADM")
        #     # # d.index("US")
        #     print(d)
        # except:
        #     pass


        # input(d)
        
        #if this is the first one or have moved on to next country
        if current == None:
            current = Country(countriesList.get(d[8]))
        elif current != None and current.countryName != countriesList.get(d[8]):


            for stuff in temporaryList: #delete from list so better efficiency?? Same with nested

                try: #SOME REGIONS CAN"T FIND THEIR PARENTS!! FIX!!
                    top = current.states.get(stuff.parentCode)
                    if current.countryName == "Australia" and top is None:
                        print(stuff)
                        print(current.states)
                        print(top)
                        input('stop')



                    top.add_sub_region(stuff)

                    tmp = []
                    while temporaryList3: # while it is not empty
                        stuff2 = temporaryList3.pop()
                        if stuff2.parentCode == stuff.regionCode:
                            stuff.add_sub_region(stuff2)
                        else:
                            tmp.append(stuff2)
                    temporaryList3 = tmp

                    # if current.countryCode == "Australia":
                    #     print(stuff)
                    #     print(top)
                    #     print(top.subRegions)
                    #
                    #     print("For each states we have")
                    #     print(top.subRegions.get(3).subRegions)
                    #     input('pause')


                except:
                    pass


            # print(temporaryList)
            # input(temporaryList3)



            temporaryList = []

            output = open("test.txt", "a")
            output.write(current.toJSON())
            output.close()

            current = Country(countriesList.get(d[8])) #parse country, CHECK NULL VALUE??

            # if d[10] != '':
            #     currentRegion = Region(d[10])  # parse region level 1
            #     current.add_region(currentRegion)

            # if d[11] != '':
            #     currentRegion2 = Region(d[11])  # parse region level 2
            #     currentRegion.add_sub_region(currentRegion2)
            #
            # if d[12] != '':
            #     currentRegion3 = Region(d[12])  # parse region level 3
            #     currentRegion2.add_sub_region(currentRegion3)
            #
            # if d[13] != '':
            #     currentRegion4 = SmallestRegion(d[13])  # parse region level 4
            #     currentRegion3.add_sub_region(currentRegion4)


        # else: #same country still
            # print(d[2])
            # print(current)
        if d[7] == "ADM1":
            currentRegion = Region(d[2], d[10], d[8]) # level 2, STATES
            current.add_region(currentRegion)
        elif d[7] == "ADM2":
            currentRegion = Region(d[2], d[11], d[10])
            temporaryList.append(currentRegion)
        elif d[7] == "PPLX":
            currentRegion = SmallestRegion(d[2], d[11]) #DOUBLE CHECK THIS
            temporaryList3.append(currentRegion)
            # top = current.regions.get(d[10])
            # currentRegion = SmallestRegion(d[2], d[10])
            # if top is None:
            #     temporaryList.append(currentRegion)
            # else:
            #     top.add_sub_region(currentRegion)



            # currentRegion = Region(d[10])  # parse region level 1
            # currentRegion2 = Region(d[11])  # parse region level 2
            # currentRegion3 = Region(d[12])  # parse region level 3
            # currentRegion4 = SmallestRegion(d[13])  # parse region level 4
            #
            # # print(current.regions.keys())
            # g = current.regions.get(d[10])
            #
            # # print(g)
            # if g is None: #doesn't exist, add them
            #     current.add_region(currentRegion)
            # else: #already exist, use the existing
            #     currentRegion = g

            # g2 = currentRegion.subRegions.get(d[11])
            # if g2 is None:  # doesn't exist, add them
            #     currentRegion.add_sub_region(currentRegion2)
            # else:  # already exist, use the new one
            #     currentRegion2 = g2
            #
            # g3 = currentRegion2.subRegions.get(d[12])
            # if g3 is None:  # doesn't exist, add them
            #     currentRegion2.add_sub_region(currentRegion3)
            # else:  # already exist, use the new one
            #     currentRegion3 = g3
            #
            # g4 = currentRegion3.subRegions.get(d[13])
            # if g4 is None:  # doesn't exist, add them
            #     currentRegion3.add_sub_region(currentRegion4)
            # else:  # already exist, use the new one
            #     currentRegion4 = g4






        
        



# The main 'geoname' table has the following fields :
# ---------------------------------------------------
# geonameid         : integer id of record in geonames database
# name              : name of geographical point (utf8) varchar(200)
# asciiname         : name of geographical point in plain ascii characters, varchar(200)
# alternatenames    : alternatenames, comma separated, ascii names automatically transliterated, convenience attribute from alternatename table, varchar(10000)
# latitude          : latitude in decimal degrees (wgs84)
# longitude         : longitude in decimal degrees (wgs84)
# feature class     : see http://www.geonames.org/export/codes.html, char(1)
# feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
# country code      : ISO-3166 2-letter country code, 2 characters
# cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 200 characters
# admin1 code       : fipscode (subject to change to iso code), see exceptions below, see file admin1Codes.txt for display names of this code; varchar(20)
# admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; varchar(80)
# admin3 code       : code for third level administrative division, varchar(20)
# admin4 code       : code for fourth level administrative division, varchar(20)
# population        : bigint (8 byte int)
# elevation         : in meters, integer
# dem               : digital elevation model, srtm3 or gtopo30, average elevation of 3''x3'' (ca 90mx90m) or 30''x30'' (ca 900mx900m) area in meters, integer. srtm processed by cgiar/ciat.
# timezone          : the iana timezone id (see file timeZone.txt) varchar(40)
# modification date : date of last modification in yyyy-MM-dd format
