# import pandas as pd
import json


from pathlib import Path


##df = pd.read_table('allCountries.txt', header=None, index_col=0) #THIS TAKES BOTH THE NUMBER AND NAME!!! FIXX

##print(df)
# df.sort_values(["10"])

##print(df.groupby(7).head(100))


##print(df.iloc[:,0])






# print(df.iloc[20])


# print(df.iloc[100])



# class Jsonable(object):
#     def __iter__(self):
#         for attr, value in self.__dict__.iteritems():
#             if isinstance(value, datetime.datetime):
#                 iso = value.isoformat()
#                 yield attr, iso
#             elif isinstance(value, decimal.Decimal):
#                 yield attr, str(value)
#             elif(hasattr(value, '__iter__')):
#                 if(hasattr(value, 'pop')):
#                     a = []
#                     for subval in value:
#                         if(hasattr(subval, '__iter__')):
#                             a.append(dict(subval))
#                         else:
#                             a.append(subval)
#                     yield attr, a
#                 else:
#                     yield attr, dict(value)
#             else:
#                 yield attr, value


class Country:
    def __init__(self, countryCode):
        self.countryCode = countryCode
        self.regions = {}
        
    def add_region(self, region):
        key = region.regionCode
        if self.regions.get(key) is None:
            self.regions[key] = region
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Region:
    def __init__(self, regionFIPS):
        self.regionCode = regionFIPS
        self.subRegions = {}

    def add_sub_region(self, region):
        key = region.regionCode
        if self.subRegions.get(key) == None:
            self.subRegions[key] = region
    
    def __eq__(self, other):
        return self.regionCode == other.regionCode

    def __hash__(self):
        return hash(self.regionCode)

class SmallestRegion:
    def __init__(self, regionFIPS):
        self.regionCode = regionFIPS

    def __eq__(self, other):
        return self.regionCode == other.regionCode

    def __hash__(self):
        return hash(self.regionCode)



current = None
countriesList = {}
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
        if d[6] != 'A': #ONLY GET CLASS A INFORMATION
            continue

        # input(d)
        
        #if this is the first one or have moved on to next country
        if current == None or current.countryCode != countriesList.get(d[8]):
            if current != None:
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


        else: #same country still
            # print(d[2])
            # print(current)
            currentRegion = SmallestRegion(d[2]) #level 1
            current.add_region(currentRegion)



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
