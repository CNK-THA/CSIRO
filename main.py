import json
from pathlib import Path

from fhir.resources.codesystem import CodeSystem
from fhir.resources.codesystem import CodeSystemConcept
from fhir.resources.fhirdate import FHIRDate
from fhir.resources.codesystem import CodeSystemProperty
from fhir.resources.codesystem import CodeSystemConceptProperty

from datetime import date

from CustomExceptions import *

# https://github.com/nazrulworld/fhir.resources
# https://www.hl7.org/fhir/resourcelist.html

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
        return {"code": self.currentFHIRCode, "display": self.name, "Parent": self.parentFHIRCode}

    def __eq__(self, other):
        return self.regionName == other.regionName

    def __hash__(self):
        return hash(self.regionName)

    def __str__(self):
        return self.name + ", " + self.regionCode + ", " + self.parent + ',' + self.currentFHIRCode + ','+ self.parentFHIRCode

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.output(),  # was __dict__
                          sort_keys=True, indent=4)


allData = []

level1 = None
countriesList = {}  # stores a mapping between country code and the country name
FIPS_To_FHIR = {}
FIPSToFHIRLevel1 = {}
FIPSToFHIRLevel2 = {}
FIPSToFHIRLevel3 = {}

level2 = []
level3 = []
temporaryList3 = []  # level 3 PPLX
temporaryList3_2 = []  # level 3 ADM3
level4 = []  # level 4 ADM4
with open("countryInfo.txt", 'r', encoding="utf8") as countryFile:
    lineNumber = 0
    for line1 in countryFile:
        lineNumber += 1
        if lineNumber < 51:  # DATA STARTS AT LINE 51
            continue
        l = line1.split('\t')
        countriesList[l[0]] = l[4]

endResult = {"status": "THIS IS A TEST"}

code = CodeSystem()
code.concept = list()
code.content = "complete"
code.status = "draft"
code.description = "CodeSystem for different administrative divisions around the world"
code.experimental = True
code.date = FHIRDate(str(date.today()))
code.id = "Ontology-CSIRO"
code.url = "SOME URL"
code.version = "0.0"
code.name = "some name?"
code.publisher = "Me"
code.caseSensitive = False #??

code.property = list()
codeProperty = CodeSystemProperty()
codeProperty.code = "parent"
codeProperty.description = "Parent codes"
codeProperty.type = "code"
code.property.append(codeProperty)






codeCounter = 0

with open(str(Path.home()) + "/Downloads/" + "allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile:
    for line in dataFile:
        dataRow = line.split("\t")
        if len(dataRow) != 19:  # Expecting 19 columns
            print(dataRow)
            input("STOP")
        if (dataRow[6] != 'P' and dataRow[6] != 'A') or (dataRow[7] != 'PPLX' and dataRow[7] != 'ADM1' and dataRow[
            7] != 'ADM2' and dataRow[7] != 'ADM3'):  # ONLY GET CLASS A and P INFORMATION
            continue

        # try:
        #     dataRow.index("AO") # Sambizanga, 2010629820
        #     # if d[8] == 'AN':
        #     # dataRow.index("MA")
        #     # dataRow.index("ADM3")
        #     # print(d[7])
        #     # print(d[7] == "ADM")
        #     # # d.index("US")
        #     print(dataRow)
        # except:
        #     pass
        #     # print("ERROR")
        # continue

        # if this is the first one or have moved on to next country
        if level1 is None:
            # current = Country(countriesList.get(d[8]))
            level1 = Region(countriesList.get(dataRow[8]), dataRow[8], None)
            FIPSToFHIRLevel1[level1.regionCode] = level1.currentFHIRCode
        elif level1 is not None and level1.regionCode != dataRow[8]:

            output = open("test.txt", "a")

            unknownState = None
            for city in level3:
                if FIPSToFHIRLevel2.get(city.parent) is None:
                    if unknownState is None:
                        unknownState = Region("unknownState", "unknownState", level1.regionCode)
                        unknownState.parentFHIRCode = FIPSToFHIRLevel1.get(unknownState.parent)

                        unknownLocationObject = CodeSystemConcept()
                        unknownLocationObject.code = unknownState.currentFHIRCode
                        unknownLocationObject.display = unknownState.name
                        unknownLocationObject.property = list()
                        conceptProperty1 = CodeSystemConceptProperty()
                        conceptProperty1.code = "parent"
                        conceptProperty1.valueCode = unknownState.parentFHIRCode
                        unknownLocationObject.property.append(conceptProperty1)

                        code.concept.append(unknownLocationObject)
                        codeCounter += 1

                    city.parentFHIRCode = unknownState.currentFHIRCode # set parent of this city to the unknown
                else:
                    city.parentFHIRCode = FIPSToFHIRLevel2.get(city.parent)
                allData.append(city.toJSON())  # write it already, need to save still?
                output.write(city.toJSON())

                locationObject = CodeSystemConcept()
                locationObject.code = city.currentFHIRCode
                locationObject.display = city.name
                locationObject.property = list()
                conceptProperty = CodeSystemConceptProperty()
                conceptProperty.code = "parent"
                conceptProperty.valueCode = city.parentFHIRCode
                locationObject.property.append(conceptProperty)

                code.concept.append(locationObject)
                codeCounter += 1

            unknownCity = None
            for suburb in level4:
                if FIPSToFHIRLevel3.get(suburb.parent) is None:
                    if unknownState is None:
                        unknownState = Region("unknownState", "unknownState", level1.regionCode)
                        unknownState.parentFHIRCode = FIPSToFHIRLevel1.get(unknownState.parent)

                        unknownLocationObject = CodeSystemConcept()
                        unknownLocationObject.code = unknownState.currentFHIRCode
                        unknownLocationObject.display = unknownState.name
                        unknownLocationObject.property = list()
                        conceptProperty1 = CodeSystemConceptProperty()
                        conceptProperty1.code = "parent"
                        conceptProperty1.valueCode = unknownState.parentFHIRCode
                        unknownLocationObject.property.append(conceptProperty1)

                        code.concept.append(unknownLocationObject)
                        codeCounter += 1

                    if unknownCity is None: # ATM GROUP EVERYTHING UNDER UNKNOWN, MOST OF THESE HAVE KNOWN STATES
                        unknownCity = Region(dataRow[2], "unknownCity", unknownState.currentFHIRCode)
                        unknownCity.parentFHIRCode = unknownState.currentFHIRCode

                        unknownCityObject = CodeSystemConcept()
                        unknownCityObject.code = unknownCity.currentFHIRCode
                        unknownCityObject.display = unknownCity.name
                        unknownCityObject.property = list()
                        conceptProperty2 = CodeSystemConceptProperty()
                        conceptProperty2.code = "parent"
                        conceptProperty2.valueCode = unknownCity.parentFHIRCode
                        unknownCityObject.property.append(conceptProperty2)

                        code.concept.append(unknownCityObject)
                        codeCounter += 1

                    suburb.parentFHIRCode = unknownCity.currentFHIRCode
                    suburb.name = suburb.name
                else:
                    suburb.parentFHIRCode = FIPSToFHIRLevel3.get(suburb.parent)
                    # allData.append(suburb.toJSON())  # write it already, need to save still?

                output.write(suburb.toJSON())

                locationObject = CodeSystemConcept()
                locationObject.code = suburb.currentFHIRCode
                locationObject.display = suburb.name
                locationObject.property = list()
                conceptProperty = CodeSystemConceptProperty()
                conceptProperty.code = "parent"
                conceptProperty.valueCode = suburb.parentFHIRCode
                locationObject.property.append(conceptProperty)

                code.concept.append(locationObject)
                codeCounter += 1

            level2 = []
            level3 = []
            level4 = []
            FIPSToFHIRLevel2 = {}
            FIPSToFHIRLevel3 = {}

            allData.append(level1.toJSON())
            output.write(level1.toJSON())

            locationObject = CodeSystemConcept()
            locationObject.code = level1.currentFHIRCode
            locationObject.display = level1.name
            # locationObject.definition = level1.parentFHIRCode  # THIS IS SET TO THE PARENT

            locationObject.property = list()
            conceptProperty = CodeSystemConceptProperty()
            conceptProperty.code = "parent"
            conceptProperty.valueCode = "Earth" # TEMPORARILY SET AS EARTH
            locationObject.property.append(conceptProperty)

            code.concept.append(locationObject)
            codeCounter += 1

            level1 = Region(countriesList.get(dataRow[8]), dataRow[8], None)
            FIPSToFHIRLevel1[level1.regionCode] = level1.currentFHIRCode

            output.close()

        child = None
        regionLevel = 0
        if dataRow[7] == "ADM1":  # LEVEL 2 STATES
            if dataRow[10] == '':
                print(dataRow)
                raise MissingFeatureCode("Missing Level 2 location codes")
            child = Region(dataRow[2], dataRow[10], dataRow[8])
            child.parentFHIRCode = FIPSToFHIRLevel1.get(child.parent)
            regionLevel = 2
            if FIPSToFHIRLevel2.get(child.regionCode) is not None:
                raise DuplicateRegionCode("Level 1 locations has multiple level 2 children of same region code")

            FIPSToFHIRLevel2[child.regionCode] = child.currentFHIRCode
            output = open("test.txt", "a")
            output.write(child.toJSON())
            output.close()
            allData.append(child.toJSON())

            locationObject = CodeSystemConcept()
            locationObject.code = child.currentFHIRCode
            locationObject.display = child.name
            # locationObject.definition = child.parentFHIRCode  # THIS IS SET TO THE PARENT

            locationObject.property = list()
            conceptProperty = CodeSystemConceptProperty()
            conceptProperty.code = "parent"
            conceptProperty.valueCode = level1.currentFHIRCode
            locationObject.property.append(conceptProperty)

            code.concept.append(locationObject)

            codeCounter += 1

        elif dataRow[7] == "ADM2":  # LEVEL 3 CITY
            if dataRow[11] == '' or dataRow[10] == '':
                print(dataRow)
                raise MissingFeatureCode("Missing Level 3 location codes")
            else: # do a plus between level 2 and 3 as a city in different states may have same name (but different location)
                child = Region(dataRow[2], dataRow[10] + dataRow[11], dataRow[10])
            level3.append(child)
            regionLevel = 3
            if FIPSToFHIRLevel3.get(child.regionCode) is not None:
                raise DuplicateRegionCode("Level 2 locations has multiple level 3 children of same region code")

            FIPSToFHIRLevel3[child.regionCode] = child.currentFHIRCode
        elif dataRow[7] == "ADM3":  # LEVEL 4 Suburbs #CHECK THIS AGAIN
            if dataRow[10] == '': # there're only 5 of these at are blank, will decide what TODO with it
                pass
                # input(dataRow)
            if dataRow[11] == '': # check dataRow[12] if going down more than ADM3?
                # input(dataRow)
                child = Region(dataRow[2], dataRow[12], "unknown") #ATM ignore the 'state' level code, drop that, FIX
            else:
                child = Region(dataRow[2], dataRow[12], dataRow[10] + dataRow[11])

            level4.append(child)


        elif dataRow[7] == "PPLX":  # find the latest non-empty one and use it instead of fixed [12]?
            if dataRow[10 + 0] == "": # The adminitrative division codes are blank, cannot link to existing ones, ignore
                pass
            elif dataRow[11] == "":  # this one must belong under AMD2
                child = Region(dataRow[2], "XXXX", dataRow[10])
                level3.append(child)
                regionLevel = 3
                # FIPSToFHIRLevel3[child.regionCode] = child.currentFHIRCode
            elif dataRow[12] == "":
                child = Region(dataRow[2], "YYYY", dataRow[10] + dataRow[11])
                level4.append(child)
                regionLevel = 4



        # ignore anything else that doesn't fit the criteria above i.e. malformed data, AMD4, AMD5

code.count = codeCounter

with open('result.json', 'w') as fp:
    json.dump(code.as_json(), fp, indent=4)



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

