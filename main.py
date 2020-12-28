import json
from pathlib import Path

from fhir.resources.codesystem import CodeSystem
from fhir.resources.codesystem import CodeSystemConcept
from fhir.resources.fhirdate import FHIRDate
from fhir.resources.codesystem import CodeSystemProperty
from fhir.resources.codesystem import CodeSystemConceptProperty
from fhir.resources.codesystem import CodeSystemFilter


from datetime import date

from CustomExceptions import *

import traceback # for debugging


LOCATION_NAME = 2
FEATURE_CLASS = 6
FEATURE_CODE = 7
COUNTRY_CODE = 8
ADMIN_1_CODE = 10
ADMIN_2_CODE = 11
ADMIN_3_CODE = 12

class Region:
    """
    All geographical information across all administrative levels will be stored as Region class before transforming
    into a FHIR CodeSystem object for JSON serialisation.
    """

    codeCounter = "0000000" # FHIR Code, incremental

    def __init__(self, regionName, regionCode, parent):
        """
        Initialise a Region object.

        :param regionName: (str) Ascii name of the region
        :param regionCode: (str) GeoName assigned code for this region (FIPS or ISO code)
        :param parent: (str) FHIR code of the parent's Region object
        """
        self.name = regionName
        self.FIPSCode = regionCode
        self.parent = parent
        self.FHIRCode = None
        self.parentFHIRCode = None
        self.assignFHIRCode()

    def assignFHIRCode(self):
        """
        Automatically run after each initialisation of new Region object.
        Assign a FHIR code to the current object and increment it by one.
        """
        self.FHIRCode = Region.codeCounter
        Region.codeCounter = '%07d' % (int(Region.codeCounter) + 1)

    def output(self):
        """
        Helper method used to produce a json string of Region object. Note: The json produced is NOT a FHIR format and
        is not used to produce the final output file.

        :return: A Json dict string format of the Region class data.
        """
        return {"code": self.FHIRCode, "display": self.name, "Parent": self.parentFHIRCode}

    def __eq__(self, other):
        """Overrides the equality method implementation."""
        return self.regionName == other.regionName

    def __hash__(self):
        """Overrides the hash function implementation."""
        return hash(self.regionName)

    def __str__(self):
        """Overrides the string function implementation."""
        return str(self.name) + ", " + str(self.FIPSCode) + ", " + str(self.parent) + ',' + str(self.FHIRCode) + ',' + str(self.parentFHIRCode)

    def toJSON(self):
        """
        Produce the current Region object in json format. Note: The json produced is NOT a FHIR format and is not
        used to produce the final output file.

        :return: A Json dict string format of the Region class data.
        """
        return json.dumps(self, default=lambda o: o.output(),
                          sort_keys=True, indent=4)


def parse_countries(file_name):
    """
    :param file_name: (str) directory to the countryInfo.txt file
    :return: Dictionary mapping of FIPS country code to country name e.g. "AU" = "Australia"
    """
    countries_list = {}
    with open(file_name, 'r', encoding="utf8") as countryFile:
        line_number = 0
        for line in countryFile:
            line_number += 1
            if line_number < 51:  # DATA STARTS AT LINE 51
                continue
            line_parsed = line.split('\t')
            countries_list[line_parsed[0]] = (line_parsed[4], line_parsed[8])
    return countries_list


def create_code_system_instance(content, status, description, experimental, dateYearTime, id, url, version, name, publisher, caseSensitive, hierarchyMeaning, valueSet):
    """
    Create a codeSystem object instance.
    See https://www.hl7.org/fhir/codesystem.html for documentation and value constriants of these parameters.

    :return: a FHIR CodeSystem object instance.
    """

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
    code.valueSet = valueSet

    populate_code_system_filter_field(code)
    populate_code_system_property_field(code)

    return code

def populate_code_system_filter_field(code):
    """
    Populate the filter field of the created codeSystem instance. Currently hardcoded 2 filters.

    :param code: codeSystem instance to be populated
    """

    code.filter = list()
    filters = [("root", ["="], "True or false."), ("deprecated", ["="], "True or false.")]
    for filter in filters:
        filter_instance = CodeSystemFilter()
        filter_instance.code = filter[0]
        filter_instance.operator = filter[1]
        filter_instance.value = filter[2]
        code.filter.append(filter_instance)

def populate_code_system_property_field(code):
    """
    Populate the property field of the created codeSystem instance. Currently hardcoded 3 properties.

    :param code: codeSystem instance to be populated
    """

    code.property = list()
    properties = [("parent", "Parent codes", "code"), ("root", "Indicates if this concept is a root concept", "boolean"), ("deprecated", "Indicates if this concept is deprecated", "boolean")]
    for property in properties:
        property_instance = CodeSystemProperty()
        property_instance.code = property[0]
        property_instance.description = property[1]
        property_instance.type = property[2]
        code.property.append(property_instance)


def create_code_system_concept_instance(code, region):
    """
    Populate the codeSystem instance with new codeSystemConcept instance. Transforming the Region class instance into
    a new codeSystemConcept instance, FHIR compatible format.

    :param code: codeSystem instance to be populated.
    :param region: Region class object to be transformed.
    :return: the newly created codeSystemConcept instance.
    """

    code_concept = CodeSystemConcept()
    code_concept.code = region.FHIRCode
    code_concept.display = region.name
    code_concept.property = list()
    code.concept.append(code_concept)
    return code_concept


def populate_code_system_concept_property_field(code_concept, property_code, property_value):
    """
    Populate the codeSystemConcept instance with it's own properties. Create a new codeSystemConceptProperty.

    :param code_concept: codeSystemConcept instance to be populated.
    :param property_code: (str) specifies which property of the codeSystemConcept to be added. As defined in codeSystem properties.
    :param property_value: (str) or (bool) value of the property to be added.
    """

    concept_property = CodeSystemConceptProperty()
    concept_property.code = property_code
    if type(property_value) == bool:
        concept_property.valueBoolean = property_value
    elif type(property_value) == str:
        concept_property.valueCode = property_value
    code_concept.property.append(concept_property)

def create_continents_region(code, earth):
    continents = [("North America", "NA"), ("South America", "SA"), ("Africa","AF"), ("Antarctica","AN"), ("Europe","EU"), ("Oceania","OC"), ("Asia","AS")]
    continents_to_FHIR = {}
    for location in continents:
        current_location = Region(location[0], location[1], earth)
        code_concept = create_code_system_concept_instance(code, current_location)
        populate_code_system_concept_property_field(code_concept, "parent", current_location.parent)
        populate_code_system_concept_property_field(code_concept, "root", False)
        populate_code_system_concept_property_field(code_concept, "deprecated", False)
        continents_to_FHIR[location[1]] = current_location.FHIRCode
    return continents_to_FHIR

def main():
    countries_list = parse_countries("countryInfo.txt") # stores a mapping between country code and the country name
    code_system = create_code_system_instance("complete", "draft", "CodeSystem for different administrative divisions around the world", True, FHIRDate(str(date.today())), "Ontology-CSIRO",
                                "http://csiro.au/geographic-locations", "0.4", "Location Ontology", "Chanon K.", True, "is-a", "http://csiro.au/geographic-locations?vs")

    # Populate the root concept location (Earth)
    root = Region("Earth", "Earth", None)
    code_concept = create_code_system_concept_instance(code_system, root)
    populate_code_system_concept_property_field(code_concept, "root", True)
    populate_code_system_concept_property_field(code_concept, "deprecated", False)
    continents_to_FHIR = create_continents_region(code_system, root.FHIRCode)

    current_country = None
    FIPSToFHIRLevel1 = {}
    FIPSToFHIRLevel2 = {}
    FIPSToFHIRLevel3 = {}

    # no need for level2 (states) since the level 1 will already be known prior to adding.
    level3 = []
    level4 = []  # level 4 ADM4

    # with open(str(Path.home()) + "/Downloads/" + "Countries.txt", 'r', encoding="utf8", errors='ignore') as dataFile:
    #     for line in dataFile:
    #         data = line.split("\t")
    #         input(data)


    with open(str(Path.home()) + "/Downloads/" + "allCountries.txt", 'r', encoding="utf8", errors='ignore') as dataFile:
        lines = dataFile.readlines()
        last = lines[-1]
        for line in lines:
            data_row = line.split("\t")
            if len(data_row) != 19:  # Expecting 19 columns
                raise DataFileInWrongFormat()
            if line != last and ((data_row[FEATURE_CLASS] != 'P' and data_row[FEATURE_CLASS] != 'A') or (data_row[FEATURE_CODE] != 'PPLX' and data_row[FEATURE_CODE] != 'ADM1' and data_row[
                FEATURE_CODE] != 'ADM2' and data_row[FEATURE_CODE] != 'ADM3')):  # ONLY GET CLASS A and P INFORMATION AND IT's NOT THE LAST LINE
                continue

            if data_row[LOCATION_NAME] == "":
                raise MissingFeatureCode("location name is missing")

            # DEBUGGING ONLY
            # try:
            #     data_row.index("VN") # Sambizanga, 2010629820
            #     # if d[8] == 'AN':
            #     # data_row.index("MA")
            #     data_row.index("ADM4")
            #     # print(d[7])
            #     # print(d[7] == "ADM")
            #     # # d.index("US")
            #     print(data_row)
            # except:
            #     pass
            #     # print("ERROR")
            # continue

            if current_country is None:  # first country or we are moving on to a new country now
                current_country = Region(countries_list.get(data_row[COUNTRY_CODE])[0], data_row[COUNTRY_CODE], countries_list.get(data_row[COUNTRY_CODE])[1])
                FIPSToFHIRLevel1[current_country.FIPSCode] = current_country.FHIRCode
            elif (current_country is not None and current_country.FIPSCode != data_row[COUNTRY_CODE]) or line == last:

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

                        city.parentFHIRCode = unknown_state.FHIRCode # set parent of this city to the unknown
                    else:
                        city.parentFHIRCode = FIPSToFHIRLevel2.get(city.parent)

                    city_code_concept = create_code_system_concept_instance(code_system, city)
                    populate_code_system_concept_property_field(city_code_concept, "parent", city.parentFHIRCode)
                    populate_code_system_concept_property_field(city_code_concept, "deprecated", False)
                    populate_code_system_concept_property_field(city_code_concept, "root", False)

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

                        if unknown_city is None:  # ATM GROUP EVERYTHING UNDER UNKNOWN, MOST OF THESE HAVE KNOWN STATES
                            unknown_city = Region(data_row[2], "unknown_city", unknown_state.FHIRCode)
                            unknown_city.parentFHIRCode = unknown_state.FHIRCode

                            unknown_city_code_concept = create_code_system_concept_instance(code_system, unknown_city)
                            populate_code_system_concept_property_field(unknown_city_code_concept, "parent", unknown_city.parentFHIRCode)
                            populate_code_system_concept_property_field(unknown_city_code_concept, "deprecated", False)
                            populate_code_system_concept_property_field(unknown_city_code_concept, "root", False)

                        suburb.parentFHIRCode = unknown_city.FHIRCode
                    else:
                        suburb.parentFHIRCode = FIPSToFHIRLevel3.get(suburb.parent)


                    suburb_code_concept = create_code_system_concept_instance(code_system, suburb)
                    populate_code_system_concept_property_field(suburb_code_concept, "parent", suburb.parentFHIRCode)
                    populate_code_system_concept_property_field(suburb_code_concept, "deprecated", False)
                    populate_code_system_concept_property_field(suburb_code_concept, "root", False)



                level3 = []
                level4 = []
                FIPSToFHIRLevel2 = {}
                FIPSToFHIRLevel3 = {}


                country_code_concept = create_code_system_concept_instance(code_system, current_country)
                populate_code_system_concept_property_field(country_code_concept, "parent", continents_to_FHIR.get(current_country.parent))
                populate_code_system_concept_property_field(country_code_concept, "deprecated", False)
                populate_code_system_concept_property_field(country_code_concept, "root", False)

                if line == last:
                    break

                current_country = Region(countries_list.get(data_row[COUNTRY_CODE])[0], data_row[COUNTRY_CODE], countries_list.get(data_row[COUNTRY_CODE])[1])
                FIPSToFHIRLevel1[current_country.FIPSCode] = current_country.FHIRCode

            if data_row[FEATURE_CODE] == "ADM1":  # States (level 2)
                if data_row[ADMIN_1_CODE] == '':
                    raise MissingFeatureCode("Missing Level 2 (states) location code")
                state = Region(data_row[LOCATION_NAME], data_row[ADMIN_1_CODE], data_row[COUNTRY_CODE])
                state.parentFHIRCode = FIPSToFHIRLevel1.get(state.parent)
                if FIPSToFHIRLevel2.get(state.FIPSCode) is not None:
                    raise DuplicateRegionCode("Level 1 locations has multiple level 2 children of same region code")

                FIPSToFHIRLevel2[state.FIPSCode] = state.FHIRCode

                state_code_concept = create_code_system_concept_instance(code_system, state)
                populate_code_system_concept_property_field(state_code_concept, "parent", current_country.FHIRCode)
                populate_code_system_concept_property_field(state_code_concept, "deprecated", False)
                populate_code_system_concept_property_field(state_code_concept, "root", False)


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

    code_system.count = int('%07d' % (int(Region.codeCounter))) # add 1 since root (earth) started at 0000000


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

