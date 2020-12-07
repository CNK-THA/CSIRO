import json
from pathlib import Path

from fhir.resources.codesystem import CodeSystem

#https://github.com/nazrulworld/fhir.resources
#https://www.hl7.org/fhir/resourcelist.html

allData = []
class Region:
    codeCounter = "0000000"

    def __init__(self, regionName, regionCode, parent):
        self.name = regionName
        self.regionCode = regionCode
        self.parent = parent
        self.currentFHIRCode = None
        self.parentFHIRCode = None
        self.assignFHIRCode()
        # self.__output = {"code":self.currentFHIRCode, "display":self.name, "Parent":self.parentFHIRCode}

        # self.subRegions = {}
        # self.test = {"Region_Name":self.regionName, "Sub_Regions":self.subRegions}

    # def add_sub_region(self, region):
    #     key = region.regionCode
    #     if self.subRegions.get(key) is None:
    #         self.subRegions[key] = region

    def assignFHIRCode(self):
        self.currentFHIRCode = Region.codeCounter
        Region.codeCounter = '%07d' % (int(Region.codeCounter) + 1)

    def output(self):
        return {"code":self.currentFHIRCode, "display":self.name, "Parent":self.parentFHIRCode}

    def __eq__(self, other):
        return self.regionName == other.regionName

    def __hash__(self):
        return hash(self.regionName)

    def __str__(self):
        return self.regionName + ", " + self.regionCode + ", "

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.output(), # was __dict__
            sort_keys=True, indent=4)


allData = []

level1 = None
countriesList = {} # stores a mapping between country code and the country name
FIPS_To_FHIR = {}
FIPSToFHIRLevel1 = {}
FIPSToFHIRLevel2 = {}
FIPSToFHIRLevel3 = {}

level2 = []
level3 = []
temporaryList3 = [] #level 3 PPLX
temporaryList3_2 = [] #level 3 ADM3
level4 = [] #level 4 ADM4
with open("countryInfo.txt", 'r', encoding="utf8") as countryFile:
    lineNumber = 0
    for line1 in countryFile:
        lineNumber += 1
        if lineNumber < 51: #DATA STARTS AT LINE 51
            continue
        l = line1.split('\t')
        countriesList[l[0]] = l[4]




with open(str(Path.home())+"/Downloads/"+ "allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile:



    for line in dataFile:
        dataRow = line.split("\t")
        if len(dataRow) != 19: # Expecting 19 columns
            print(dataRow)
            input("STOP")
        if dataRow[6] != 'P' and dataRow[6] != 'A': #ONLY GET CLASS A and P INFORMATION
            continue

        # try:
        #     dataRow.index("FM")
        #     # if d[8] == 'AN':
        #     dataRow.index("MA")
        #     # dataRow.index("ADM3")
        #     # print(d[7])
        #     # print(d[7] == "ADM")
        #     # # d.index("US")
        #     print(dataRow)
        # except:
        #     pass
        #     # print("ERROR")
        # continue

        
        #if this is the first one or have moved on to next country
        if level1 is None:
            # current = Country(countriesList.get(d[8]))
            level1 = Region(countriesList.get(dataRow[8]), dataRow[8], None)
            FIPSToFHIRLevel1[level1.regionCode] = level1.currentFHIRCode
        elif level1 is not None and level1.regionCode != dataRow[8]:

            output = open("test.txt", "a")



            for city in level3:
                #SOME REGIONS CAN"T FIND THEIR PARENTS!! FIX!!
                city.parentFHIRCode = FIPSToFHIRLevel2.get(city.parent)
                allData.append(city.toJSON()) # write it already, need to save still?
                output.write(city.toJSON() + "\n")

            for suburb in level4:
                suburb.parentFHIRCode = FIPSToFHIRLevel3.get(suburb.parent)
                allData.append(suburb.toJSON())  # write it already, need to save still?
                output.write(suburb.toJSON() + "\n")


            level2 = []
            level3 = []
            level4 = []
            FIPSToFHIRLevel2 = {}
            FIPSToFHIRLevel3 = {}

            allData.append(level1.toJSON())
            output.write(level1.toJSON() + "\n")
            level1 = Region(countriesList.get(dataRow[8]), dataRow[8], None)
            FIPSToFHIRLevel1[level1.regionCode] = level1.currentFHIRCode
            output.close()


        child = None
        regionLevel = 0
        if dataRow[7] == "ADM1": # LEVEL 2 STATES
            # print("ONE")
            child = Region(dataRow[2], dataRow[10], dataRow[8])
            child.parentFHIRCode = FIPSToFHIRLevel1.get(child.parent)
            regionLevel = 2
            if FIPSToFHIRLevel2.get(child.regionCode) is not None:
                print(dataRow)
                print(child.regionCode)
                input("SHIT2")
            FIPSToFHIRLevel2[child.regionCode] = child.currentFHIRCode
            output = open("test.txt", "a")
            output.write(child.toJSON() + "\n")
            output.close()
            allData.append(child.toJSON())

        elif dataRow[7] == "ADM2": # LEVEL 3 CITY
            # print("TWO")
            child = Region(dataRow[2], dataRow[10] + dataRow[11], dataRow[10])
            level3.append(child)
            regionLevel = 3
            if FIPSToFHIRLevel3.get(child.regionCode) is not None:
                print(dataRow)
                print(child.regionCode)
                input("SHIT3")
            FIPSToFHIRLevel3[child.regionCode] = child.currentFHIRCode
        elif dataRow[7] == "ADM3": # LEVEL 4 Suburbs #CHECK THIS AGAIN
            # print("THREE")
            child = Region(dataRow[2], dataRow[12], dataRow[10] + dataRow[11])
            level4.append(child)
            regionLevel = 4
        elif dataRow[7] == "PPLX": #find the latest non-empty one and use it instead of fixed [12]?
            child = Region(dataRow[2], dataRow[12], dataRow[10] + dataRow[11])
            level4.append(child)
        else:
            continue #Change the Class filter above?

        # elif dataRow[7] == "ADM4":
        #     currentRegion = Region(d[2], d[13], d[12])
        #     temporaryList4.append(currentRegion)

        # elif dataRow[7] == "PPLX": #Get the last level, check blank then add it there??
        #     #ATM IT IS ADDING TO LEVEL 3
        #     #use a counter here since the suburb doesn't have a code!
        #     currentRegion = Region(d[2], d[11] + str(suburbCounter), d[11]) #DOUBLE CHECK THIS
        #     temporaryList3.append(currentRegion)
        #     suburbCounter += 1

        # print(FIPSToFHIR)
        # print(dataRow, "assigned", level1.regionCode + child.regionCode)
        # if level1.regionCode + child.regionCode == "BEBRU":
        #     print(dataRow)
        # if FIPSToFHIR.get(str(regionLevel) + level1.regionCode + child.regionCode) is not None and regionLevel != 4:
        #     # print(FIPSToFHIR)
        #     print(dataRow)
        #     print(str(regionLevel) + level1.regionCode + child.regionCode)
        #     # print(FIPSToFHIR.get(level1.regionCode + child.regionCode))
        #     input("SHIT")

        # if regionLevel != 4: #no need to add the 4th level, won't have child anyway #AT THE MOMENT IT IS REPLACING OLD, FIXX!!
        #     FIPSToFHIR[str(regionLevel) + level1.regionCode + child.regionCode] = child.currentFHIRCode







data1 = {"status":"THIS IS A TEST", "content": ''.join(allData)}

code = CodeSystem(data1)
print(code.content)
# print(code.as_json())


# output = open("haha.txt", "a")
# output.write(str(code.as_json()))
# output.close()


        
        



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
