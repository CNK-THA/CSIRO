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
        if self.regions.get(key) == None:
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



with open("allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile: #str(Path.home())+"/Downloads/
    for line in dataFile:
        d = line.split("\t")
        # input(d)
        
            
        if len(d) != 19: # Expecting 19 columns
            print(d)
            input("STOP")

##        if d[8] == "": # ONE OF THE RECORD (Asian/Aden, "Gulf of Aden") is blank
##            print(d)
##            input("BREAK")

##        print(d[11]) #DIVISION 2??


        
        #if this is the first one or have moved on to next country
        if current == None or current.countryCode != d[8]:
            if current != None:
##                input(current.regions)
                # current.regions = list(current.regions) # make it serialisable
                output = open("test.txt", "a")
                output.write(current.toJSON())
                output.close()

            current = Country(d[8]) #parse country

            currentRegion = Region(d[10])  # parse region level 1
            current.add_region(currentRegion)

            currentRegion2 = Region(d[11])  # parse region level 2
            currentRegion.add_sub_region(currentRegion2)

            currentRegion3 = Region(d[12])  # parse region level 3
            currentRegion2.add_sub_region(currentRegion3)

            currentRegion4 = SmallestRegion(d[13])  # parse region level 4
            currentRegion3.add_sub_region(currentRegion4)

            # print(current.regions, currentRegion.subRegions, currentRegion2.subRegions, currentRegion3.subRegions, currentRegion4.subRegions)

        else: #same country still

            currentRegion = Region(d[10])  # parse region level 1
            currentRegion2 = Region(d[11])  # parse region level 2
            currentRegion3 = Region(d[12])  # parse region level 3
            currentRegion4 = SmallestRegion(d[13])  # parse region level 4

            # print(current.regions.keys())
            g = current.regions.get(d[10])

            # print(g)
            if g is None: #doesn't exist, add them
                current.add_region(currentRegion)
            else: #already exist, use the new one
                currentRegion = g

            g2 = currentRegion.subRegions.get(d[11])
            if g2 is None:  # doesn't exist, add them
                currentRegion.add_sub_region(currentRegion2)
            else:  # already exist, use the new one
                currentRegion2 = g2

            g3 = currentRegion2.subRegions.get(d[12])
            if g3 is None:  # doesn't exist, add them
                currentRegion2.add_sub_region(currentRegion3)
            else:  # already exist, use the new one
                currentRegion3 = g3

            g4 = currentRegion3.subRegions.get(d[13])
            if g4 is None:  # doesn't exist, add them
                currentRegion3.add_sub_region(currentRegion4)
            else:  # already exist, use the new one
                currentRegion4 = g4






        
        



