import json









class Region:
    codeCounter = "0000000"

    def __init__(self, regionName, regionCode, parent):
        self.name = regionName
        self.regionCode = regionCode
        self.parent = parent
        self.currentFHIRCode = None
        self.parentFHIRCode = None
        self.assignFHIRCode()
        self.__output = {"FHIRCode":self.currentFHIRCode, "Name":self.name, "Parent":self.parentFHIRCode}

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
        return {"FHIRCode":self.currentFHIRCode, "Name":self.name, "Parent":self.parentFHIRCode}

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
FIPSToFHIR = {}

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




with open("allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile: #str(Path.home())+"/Downloads/



    for line in dataFile:
        dataRow = line.split("\t")
        if len(dataRow) != 19: # Expecting 19 columns
            print(dataRow)
            input("STOP")
        if dataRow[6] != 'P' and dataRow[6] != 'A': #ONLY GET CLASS A and P INFORMATION
            continue

        # try:
        #     dataRow.index("DE")
        #     # if d[8] == 'AN':
        #     d.index("PPLX")
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
            FIPSToFHIR[level1.regionCode] = level1.currentFHIRCode
        elif level1 is not None and level1.regionCode != dataRow[8]:

            output = open("test.txt", "a")



            for city in level3:
                #SOME REGIONS CAN"T FIND THEIR PARENTS!! FIX!!
                city.parentFHIRCode = FIPSToFHIR.get(city.parent)
                allData.append(city) # write it already, need to save still?
                output.write(city.toJSON())
            for suburb in level4:
                suburb.parentFHIRCode = FIPSToFHIR.get(suburb.parent)
                allData.append(suburb) # write it already, need to save still?
                output.write(suburb.toJSON())




            level2 = []
            level3 = []
            level4 = []

            allData.append(level1)
            output.write(level1.toJSON())
            level1 = Region(countriesList.get(dataRow[8]), dataRow[8], None)
            output.close()


        child = None
        if dataRow[7] == "ADM1": # LEVEL 2 STATES
            print("ONE")
            child = Region(dataRow[2], dataRow[10], dataRow[8])
        elif dataRow[7] == "ADM2": # LEVEL 3 CITY
            print("TWO")
            child = Region(dataRow[2], dataRow[11], dataRow[10])
            level3.append(child)
        elif dataRow[7] == "ADM3": # LEVEL 4 Suburbs #CHECK THIS AGAIN
            print("THREE")
            child = Region(dataRow[2], dataRow[12], dataRow[11])
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
        # print(dataRow)
        if FIPSToFHIR.get(level1.regionCode + child.regionCode) is not None:
            print(FIPSToFHIR)
            print(level1.regionCode + child.regionCode)
            print(FIPSToFHIR.get(level1.regionCode + child.regionCode))
            input("SHIT")
        FIPSToFHIR[level1.regionCode + child.regionCode] = child.currentFHIRCode










        
        



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
