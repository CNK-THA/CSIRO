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

LOCATION_NAME = 2
FEATURE_CLASS = 6
FEATURE_CODE = 7
COUNTRY_CODE = 8
ADMIN_1_CODE = 10
ADMIN_2_CODE = 11
ADMIN_3_CODE = 12

class Region:
    codeCounter = "0000000"

    def __init__(self, regionName, regionCode, parent):
        self.name = regionName
        self.FIPSCode = regionCode
        self.parent = parent
        self.FHIRCode = None
        self.parentFHIRCode = None
        self.assignFHIRCode()

    def assignFHIRCode(self):
        self.FHIRCode = Region.codeCounter
        Region.codeCounter = '%07d' % (int(Region.codeCounter) + 1)

    def output(self):
        return {"code": self.FHIRCode, "display": self.name, "Parent": self.parentFHIRCode}

    def __eq__(self, other):
        return self.regionName == other.regionName

    def __hash__(self):
        return hash(self.regionName)

    def __str__(self):
        return self.name + ", " + self.FIPSCode + ", " + self.parent + ',' + self.FHIRCode + ',' + self.parentFHIRCode

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.output(),  # was __dict__
                          sort_keys=True, indent=4)

def parse_countries(file_name):
    countries_list = {}
    with open(file_name, 'r', encoding="utf8") as countryFile:
        line_number = 0
        for line in countryFile:
            line_number += 1
            if line_number < 51:  # DATA STARTS AT LINE 51
                continue
            line_parsed = line.split('\t')
            countries_list[line_parsed[0]] = line_parsed[4]
    return countries_list


def create_code_system_instance(content, status, description, experimental, dateYearTime, id, url, version, name, publisher, caseSensitive, hierarchyMeaning):
    code = CodeSystem()
    code.concept = list()
    code.content = content
    code.status = status
    code.description = description
    code.experimental = experimental
    code.date = dateYearTime
    code.id = id
    code.url = url
    code.version = version
    code.name = name
    code.publisher = publisher
    code.caseSensitive = caseSensitive
    code.hierarchyMeaning = hierarchyMeaning

    populate_code_system_property_field(code)

    return code


def populate_code_system_property_field(code):
    code.property = list()
    properties = [("parent", "Parent codes", "code"), ("root", "Indicates if this concept is a root concept", "boolean"), ("deprecated", "Indicates if this concept is deprecated", "boolean")]
    for property in properties:
        property_instance = CodeSystemProperty()
        property_instance.code = property[0]
        property_instance.description = property[1]
        property_instance.type = property[2]
        code.property.append(property_instance)




def create_code_system_concept_instance(code, region):
    code_concept = CodeSystemConcept()
    code_concept.code = region.FHIRCode
    code_concept.display = region.name
    code_concept.property = list()
    code.concept.append(code_concept)
    return code_concept


def populate_code_system_concept_property_field(code_concept, property_code, property_value):
    concept_property = CodeSystemConceptProperty()
    concept_property.code = property_code
    if type(property_value) == bool:
        concept_property.valueBoolean = property_value
    elif type(property_value) == str:
        concept_property.valueCode = property_value
    code_concept.property.append(concept_property)


#
# code.count = codeCounter
# with open('resultSample.json', 'w') as fp:
#     json.dump(code.as_json(), fp, indent=4)


def main():
    countries_list = parse_countries("countryInfo.txt")
    code_system = create_code_system_instance("complete", "draft", "CodeSystem for different administrative divisions around the world", True, FHIRDate(str(date.today())), "Ontology-CSIRO",
                                "SOME URL", "0.1", "Location Ontology", "Chanon K.", True, "is-a")

    code_counter = 0 # how many code system concept have we created so far

    # Populate the root concept location (Earth)
    root = Region("Earth", "Earth", None)
    code_concept = create_code_system_concept_instance(code_system, root)
    populate_code_system_concept_property_field(code_concept, "root", True)
    populate_code_system_concept_property_field(code_concept, "deprecated", False)
    code_counter += 1

    current_country = None
    countriesList = {}  # stores a mapping between country code and the country name
    FIPSToFHIRLevel1 = {}
    FIPSToFHIRLevel2 = {}
    FIPSToFHIRLevel3 = {}

    level2 = []
    level3 = []
    level4 = []  # level 4 ADM4

    with open(str(Path.home()) + "/Downloads/" + "allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile:
        for line in dataFile:
            data_row = line.split("\t")
            if len(data_row) != 19:  # Expecting 19 columns
                raise DataFileInWrongFormat()
            if (data_row[FEATURE_CLASS] != 'P' and data_row[FEATURE_CLASS] != 'A') or (data_row[FEATURE_CODE] != 'PPLX' and data_row[FEATURE_CODE] != 'ADM1' and data_row[
                FEATURE_CODE] != 'ADM2' and data_row[FEATURE_CODE] != 'ADM3'):  # ONLY GET CLASS A and P INFORMATION
                continue

            # DEBUGGING ONLY
            # try:
            #     data_row.index("AO") # Sambizanga, 2010629820
            #     # if d[8] == 'AN':
            #     # data_row.index("MA")
            #     # data_row.index("ADM3")
            #     # print(d[7])
            #     # print(d[7] == "ADM")
            #     # # d.index("US")
            #     print(data_row)
            # except:
            #     pass
            #     # print("ERROR")
            # continue

            if current_country is None:  # first country or we are moving on to a new country now
                current_country = Region(countriesList.get(data_row[COUNTRY_CODE]), data_row[COUNTRY_CODE], None)
                FIPSToFHIRLevel1[current_country.FIPSCode] = current_country.FHIRCode
            elif current_country is not None and current_country.FIPSCode != data_row[COUNTRY_CODE]: #CHECK IF THE LAST COUNTRY IS ADDED OR NOT???

                # output = open("test.txt", "a")

                unknown_state = None
                for city in level3:
                    if FIPSToFHIRLevel2.get(city.parent) is None:
                        if unknown_state is None:
                            unknown_state = Region("unknown_state", "unknown_state", current_country.FIPSCode)
                            unknown_state.parentFHIRCode = FIPSToFHIRLevel1.get(unknown_state.parent)

                            unknown_state_code_concept = create_code_system_concept_instance(code_system, unknown_state)
                            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", unknown_state.parentFHIRCode)
                            populate_code_system_concept_property_field(unknown_state_code_concept, "deprecated", False)
                            populate_code_system_concept_property_field(unknown_state_code_concept, "root", False)
                            code_counter += 1

                        city.parentFHIRCode = unknown_state.FHIRCode # set parent of this city to the unknown
                    else:
                        city.parentFHIRCode = FIPSToFHIRLevel2.get(city.parent)
                    # output.write(city.toJSON()) #Still need this?

                    city_code_concept = create_code_system_concept_instance(code_system, city)
                    populate_code_system_concept_property_field(city_code_concept, "parent", city.parentFHIRCode)
                    populate_code_system_concept_property_field(city_code_concept, "deprecated", False)
                    populate_code_system_concept_property_field(city_code_concept, "root", False)
                    code_counter += 1

                unknown_city = None
                for suburb in level4:
                    if FIPSToFHIRLevel3.get(suburb.parent) is None:
                        if unknown_state is None:
                            unknown_state = Region("unknown_state", "unknown_state", current_country.FIPSCode)
                            unknown_state.parentFHIRCode = FIPSToFHIRLevel1.get(unknown_state.parent)

                            unknown_state_code_concept = create_code_system_concept_instance(code_system, unknown_state)
                            populate_code_system_concept_property_field(unknown_state_code_concept, "parent",
                                                                        unknown_state.parentFHIRCode)
                            populate_code_system_concept_property_field(unknown_state_code_concept, "deprecated", False)
                            populate_code_system_concept_property_field(unknown_state_code_concept, "root", False)
                            code_counter += 1
    #
                        if unknown_city is None:  # ATM GROUP EVERYTHING UNDER UNKNOWN, MOST OF THESE HAVE KNOWN STATES
                            unknown_city = Region(data_row[2], "unknown_city", unknown_state.FHIRCode)
                            unknown_city.parentFHIRCode = unknown_state.FHIRCode

                            unknown_city_code_concept = create_code_system_concept_instance(code_system, unknown_city)
                            populate_code_system_concept_property_field(unknown_city_code_concept, "parent", unknown_city.parentFHIRCode)
                            populate_code_system_concept_property_field(unknown_city_code_concept, "deprecated", False)
                            populate_code_system_concept_property_field(unknown_city_code_concept, "root", False)
                            code_counter += 1

                        suburb.parentFHIRCode = unknown_city.FHIRCode
                    else:
                        suburb.parentFHIRCode = FIPSToFHIRLevel3.get(suburb.parent)

    #                 output.write(suburb.toJSON()) # still need this?

                    suburb_code_concept = create_code_system_concept_instance(code_system, suburb)
                    populate_code_system_concept_property_field(suburb_code_concept, "parent", suburb.parentFHIRCode)
                    populate_code_system_concept_property_field(suburb_code_concept, "deprecated", False)
                    populate_code_system_concept_property_field(suburb_code_concept, "root", False)
                    code_counter += 1

                level2 = [] #Why level is added straight to the file???
                level3 = []
                level4 = []
                FIPSToFHIRLevel2 = {}
                FIPSToFHIRLevel3 = {}

    #             output.write(current_country.toJSON())

                country_code_concept = create_code_system_concept_instance(code_system, current_country)
                populate_code_system_concept_property_field(country_code_concept, "parent", root.FHIRCode)
                populate_code_system_concept_property_field(country_code_concept, "deprecated", False)
                populate_code_system_concept_property_field(country_code_concept, "root", False)
                code_counter += 1

                current_country = Region(countriesList.get(data_row[COUNTRY_CODE]), data_row[COUNTRY_CODE], None)
                FIPSToFHIRLevel1[current_country.FIPSCode] = current_country.FHIRCode
                # output.close()

            if data_row[FEATURE_CODE] == "ADM1":  # States (level 2)
                if data_row[ADMIN_1_CODE] == '':
                    raise MissingFeatureCode("Missing Level 2 (states) location code")
                state = Region(data_row[LOCATION_NAME], data_row[ADMIN_1_CODE], data_row[COUNTRY_CODE])
                state.parentFHIRCode = FIPSToFHIRLevel1.get(state.parent)
                if FIPSToFHIRLevel2.get(state.FIPSCode) is not None:
                    raise DuplicateRegionCode("Level 1 locations has multiple level 2 children of same region code")

                FIPSToFHIRLevel2[state.FIPSCode] = state.FHIRCode

                # output = open("test.txt", "a")
                # output.write(state.toJSON())
                # output.close()

                state_code_concept = create_code_system_concept_instance(code_system, state)
                populate_code_system_concept_property_field(state_code_concept, "parent", current_country.FHIRCode)
                populate_code_system_concept_property_field(state_code_concept, "deprecated", False)
                populate_code_system_concept_property_field(state_code_concept, "root", False)

                code_counter += 1

            elif data_row[FEATURE_CODE] == "ADM2":  # City (level 3)
                if data_row[ADMIN_2_CODE] == '' or data_row[ADMIN_1_CODE] == '':
                    raise MissingFeatureCode("Missing Level 3 (city) location code")
                # do a plus between level 2 and 3 as a city in different states may have same name (but different location)
                city = Region(data_row[LOCATION_NAME], data_row[ADMIN_1_CODE] + data_row[ADMIN_2_CODE], data_row[ADMIN_1_CODE])
                level3.append(city)
                if FIPSToFHIRLevel3.get(city.FIPSCode) is not None:
                    raise DuplicateRegionCode("Level 2 locations has multiple level 3 children of same region code")
                FIPSToFHIRLevel3[city.FIPSCode] = city.FHIRCode

            elif data_row[FEATURE_CODE] == "ADM3":  # Suburb (level 4)
                if data_row[ADMIN_1_CODE] == '': # there're only 5 of these at are blank, will decide what TODO with it
                    pass
                suburb = None
                if data_row[ADMIN_2_CODE] == '': # check data_row[12] if going down more than ADM3?
                    suburb = Region(data_row[LOCATION_NAME], data_row[ADMIN_3_CODE], "unknown") #ATM ignore the 'state' level code, drop that, FIX
                else:
                    suburb = Region(data_row[LOCATION_NAME], data_row[ADMIN_3_CODE], data_row[ADMIN_1_CODE] + data_row[ADMIN_2_CODE])
                level4.append(suburb)
            elif data_row[FEATURE_CODE] == "PPLX":  # find the latest non-empty one and use it instead of fixed [12]?
                if data_row[ADMIN_1_CODE] == "": # The adminitrative division codes are blank, cannot link to existing ones, ignore
                    pass
                elif data_row[ADMIN_2_CODE] == "":  # this one must belong under AMD2
                    level3.append(Region(data_row[LOCATION_NAME], "XXXX", data_row[ADMIN_1_CODE]))
                elif data_row[ADMIN_3_CODE] == "":
                    level4.append(Region(data_row[LOCATION_NAME], "YYYY", data_row[ADMIN_1_CODE] + data_row[ADMIN_2_CODE]))

            # ignore anything else that doesn't fit the criteria above i.e. malformed data, AMD4, AMD5


    with open('resultSample.json', 'w') as fp:
        json.dump(code_system.as_json(), fp, indent=4)

if __name__ == "__main__":
    main()

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

