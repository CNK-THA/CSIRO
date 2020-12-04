import json



class Region:
    def __init__(self, regionName, regionCode, parent):
        self.regionName = regionName
        self.regionCode = regionCode
        self.parentCode = parent
        self.subRegions = {}
        self.test = {"Region_Name":self.regionName, "Sub_Regions":self.subRegions}

    def add_sub_region(self, region):
        key = region.regionCode
        if self.subRegions.get(key) is None:
            self.subRegions[key] = region

    def __eq__(self, other):
        return self.regionName == other.regionName

    def __hash__(self):
        return hash(self.regionName)

    def __str__(self):
        return self.regionName + ", " + self.regionCode + ", "

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.test, # was __dict__
            sort_keys=True, indent=4)


current = None
countriesList = {} # stores a mapping between country code and the country name


temporaryList = []
temporaryList3 = [] #level 3 PPLX
temporaryList3_2 = [] #level 3 ADM3
temporaryList4 = [] #level 4 ADM4
with open("countryInfo.txt", 'r', encoding="utf8") as countryFile:
    lineNumber = 0
    for line1 in countryFile:
        lineNumber += 1
        if lineNumber < 51: #DATA STARTS AT LINE 51
            continue
        l = line1.split('\t')
        countriesList[l[0]] = l[4]




with open("allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile: #str(Path.home())+"/Downloads/
    suburbCounter = 0
    for line in dataFile:
        d = line.split("\t")



        
            
        if len(d) != 19: # Expecting 19 columns
            print(d)
            input("STOP")
        if d[6] != 'P' and d[6] != 'A': #ONLY GET CLASS A INFORMATION
            continue

        try:
            d.index("IT")
            d.index("PPLX")
            # d.index("ADM4")
            # print(d[7])
            # print(d[7] == "ADM")
            # # d.index("US")
            print(d)
        except:
            pass
        continue

        
        #if this is the first one or have moved on to next country
        if current is None:
            # current = Country(countriesList.get(d[8]))
            current = Region(countriesList.get(d[8]), d[8], None)
        elif current is not None and current.regionName != countriesList.get(d[8]):
            for stuff in temporaryList: #find states for each city, stuff is LEVEL 2
                # #delete from list so better efficiency?? Same with nested

                #SOME REGIONS CAN"T FIND THEIR PARENTS!! FIX!!
                    top = current.subRegions.get(stuff.parentCode)
                    if current.regionName == "Australia" and top is None:
                        print(stuff)
                        print(current.states)
                        print(top)
                        input('stop')

                    if top is None:
                        print("NONETYPE")
                    else:
                        top.add_sub_region(stuff)


                        tmp = []
                        while temporaryList3_2:
                            level3 = temporaryList3_2.pop()
                            if stuff.regionCode == level3.parentCode:
                                stuff.add_sub_region(level3)

                                tmp2 = []
                                while temporaryList4:
                                    level4 = temporaryList4.pop()
                                    if level4.parentCode == level3.regionCode:
                                        level3.add_sub_region(level4)
                                    else:
                                        tmp2.append(level4)
                                temporaryList4 = tmp2

                            else:
                                tmp.append(level3)
                        temporaryList3_2 = tmp



                        tmp = []
                        while temporaryList3: # while it is not empty
                            stuff2 = temporaryList3.pop()
                            if stuff2.parentCode == stuff.regionCode:
                                stuff.add_sub_region(stuff2)
                            else:
                                tmp.append(stuff2)

                        temporaryList3 = tmp



            temporaryList = []
            temporaryList3 = []
            temporaryList3_2 = []
            temporaryList4 = []

            output = open("test.txt", "a")
            output.write(current.toJSON())
            output.close()

            # current = Country(countriesList.get(d[8])) #parse country, CHECK NULL VALUE??
            current = Region(countriesList.get(d[8]), d[8], None)


        if d[7] == "ADM1":
            currentRegion = Region(d[2], d[10], d[8]) # level 2, STATES
            current.add_sub_region(currentRegion)
        elif d[7] == "ADM2":
            currentRegion = Region(d[2], d[11], d[10])
            temporaryList.append(currentRegion)
        elif d[7] == "ADM3":
            currentRegion = Region(d[2], d[12], d[11])
            temporaryList3_2.append(currentRegion)
        elif d[7] == "ADM4":
            currentRegion = Region(d[2], d[13], d[12])
            temporaryList4.append(currentRegion)

        elif d[7] == "PPLX": #Get the last level, check blank then add it there??
            #ATM IT IS ADDING TO LEVEL 3
            #use a counter here since the suburb doesn't have a code!
            currentRegion = Region(d[2], d[11] + str(suburbCounter), d[11]) #DOUBLE CHECK THIS
            temporaryList3.append(currentRegion)
            suburbCounter += 1









        
        



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
