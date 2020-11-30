import pandas as pd
import json


from pathlib import Path


##df = pd.read_table('allCountries.txt', header=None, index_col=0) #THIS TAKES BOTH THE NUMBER AND NAME!!! FIXX

##print(df)
# df.sort_values(["10"])

##print(df.groupby(7).head(100))


##print(df.iloc[:,0])






# print(df.iloc[20])


# print(df.iloc[100])


class Country:
    def __init__(self, countryCode):
        self.countryCode = countryCode
        self.regions = set()
        
    def add_region(self, region):
        self.regions.add(region)
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Region:
    def __init__(self, regionFIPS):
        self.regionCode = regionFIPS
        self.subRegions = set()

    def add_sub_region(self, region):
        self.subRegions.add(region)
    
    def __eq__(self, other):
        return self.regionCode == other.regionCode

    def __hash__(self):
        return hash(self.regionCode)
  

class Region2:
    def __init__(self, region):
        self.region = region
        
    def __eq__(self, other):
        return self.region == other.region

    def __hash__(self):
        return hash(self.region)




current = None



with open(str(Path.home())+"/Downloads/allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile:
    for line in dataFile:
        d = line.split("\t")
        print(d)
        
            
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
                current.regions = list(current.regions) # make it serialisable
                output = open("test.txt", "a")
                output.write(current.toJSON())
                output.close()
            current = Country(d[8])
            
        else:
            current.add_region(Region(d[10]))
    



        
        



