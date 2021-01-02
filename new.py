
# import csv
import json

# csv.field_size_limit(100000000)

# RAN THIS ONE!!!
# import pandas as pd
# import sqlite3
#
# con = sqlite3.connect("C:\\Users\\s4445655\\Downloads\\gadm36_AUS_1_sp.rds")
#
# cursor = con.cursor()
# cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
# print(cursor.fetchall())
#
#
# df = pd.read_sql_query("SELECT * FROM level3;", con)
# print(df.head(100))
# df.to_csv('outputTest.txt', encoding='utf-8') #or utf-8 ??

# import fiona
# shape = fiona.open("C:\\Users\\s4445655\\Downloads\\gadm36_AUS_1_sp.rds")
# print(shape.schema)

# import shapefile
# shape = shapefile.Reader("C:\\Users\\s4445655\\Downloads\\gadm28.shp\gadm28.dbf")
# input('done reading?')
# print(shape.numRecords)
# #first feature of the shapefile
# feature = shape.shapeRecords()[0]
# input('done getting?')
# first = feature.shape.__geo_interface__
# input('continue?')
# print(first) # (GeoJSON format)

# import fiona
# shape = fiona.open("gadm28.shp")
# print(shape.schema)
#
# first = shape.next()
# while first is not None:
#     if first['properties']['NAME_0'] == "Australia" and first['properties']['NAME_1'] == "Queensland":
#         print("Name1", first['properties']['NAME_1'])
#         print("Name2", first['properties']['NAME_2'])
#         print("Name3", first['properties']['NAME_3'])
#         input(first)
#     first = shape.next()

class Region2:
    fhir_code_counter = "0000000"

    def __init__(self, name, parent):
        # self.name = name
        # self.parent_code = parent
        # self.my_fhir_code = Region.fhir_code_counter

        self.name = name
        # self.FIPSCode = regionCode
        self.parent = parent
        self.FHIRCode = Region2.fhir_code_counter
        # self.parentFHIRCode = None
        Region2.fhir_code_counter = '%07d' % (int(Region2.fhir_code_counter) + 1)


    def output(self):
        return {"code": self.FHIRCode, "display": self.name, "Parent": self.parent}

    def __str__(self):
        return "Region: " + self.name + " with parent " + self.parent + " and self code " + self.FHIRCode

    def toJSON(self):
        """
        Produce the current Region object in json format. Note: The json produced is NOT a FHIR format and is not
        used to produce the final output file.

        :return: A Json dict string format of the Region class data.
        """
        return json.dumps(self, default=lambda o: o.output(),
                          sort_keys=True, indent=4)




countries = {}
states = {}
districts = {}
suburbs = {}
import fiona
from main import *

from fhir.resources.codesystem import CodeSystem
from fhir.resources.codesystem import CodeSystemConcept
# from fhir.resources.fhirdate import FHIRDate
from fhir.resources.codesystem import CodeSystemProperty
from fhir.resources.codesystem import CodeSystemConceptProperty
from fhir.resources.codesystem import CodeSystemFilter


for layername in fiona.listlayers("gadm28_levels.shp"):
    with fiona.open("gadm28_levels.shp", layer=layername) as c:
        current_location = c.next()
        print("there are:", len(c), "in total")
        while True:
            if layername == "gadm28_adm0": # countries level
                 new_country = Region2(current_location['properties']['NAME_ENGLI'], "None")
                 countries[current_location['properties']['ISO']] = new_country
            elif layername == "gadm28_adm1": # states level
                if countries.get(current_location['properties']['ISO']) is not None and current_location['properties']['NAME_1'] is not None and states.get(current_location['properties']['NAME_1']) is None: # Bonaire, Saint Eustatius and Saba MISSPELLED #instead of name_0
                    new_state = Region2(current_location['properties']['NAME_1'], countries.get(current_location['properties']['ISO']).FHIRCode)
                    states[new_state.name] = new_state
                # else:
                #     print('these are in else')
                #     # print(current_location)
                #     print(countries.get(current_location['properties']['ISO']))
                #     print(current_location['properties'])
                #     input(states.get(current_location['properties']['NAME_1']))
            elif layername == "gadm28_adm2": # district level
                if states.get(current_location['properties']['NAME_1']) is not None and current_location['properties']['NAME_2'] is not None and districts.get(current_location['properties']['NAME_2']) is None:
                    new_district = Region2(current_location['properties']['NAME_2'], states.get(current_location['properties']['NAME_1']).FHIRCode)
                    districts[new_district.name] = new_district
                # else:
                #     print('in district level')
                #     print(districts.get(current_location['properties']['NAME_2']))
                #     input(current_location['properties']['NAME_2'])
            elif layername == "gadm28_adm3":
                if districts.get(current_location['properties']['NAME_2']) is not None and current_location['properties']['NAME_3'] is not None and suburbs.get(current_location['properties']['NAME_3']) is None:
                    new_suburb = Region2(current_location['properties']['NAME_3'], districts.get(current_location['properties']['NAME_2']).FHIRCode)
                    suburbs[new_suburb.name] = new_suburb
                # else:
                #     print('in suburbs level')
                #     print(suburbs.get(current_location['properties']['NAME_3']))
                #     input(current_location['properties']['NAME_3'])
            try:
                current_location = c.next()
            except StopIteration:
                break
    if layername == "gadm28_adm3": # can go further to 4 and 5, LATER
        break


code_system = create_code_system_instance("complete", "draft", "CodeSystem for different administrative divisions around the world", True, FHIRDate(str(date.today())), "Ontology-CSIRO",
                                "http://csiro.au/geographic-locations", "0.4", "Location Ontology", "Chanon K.", True, "is-a", "http://csiro.au/geographic-locations?vs") # FHIRDate(str(date.today()))

root = Region("Earth", "Earth", None)
code_concept = create_code_system_concept_instance(code_system, root)
populate_code_system_concept_property_field(code_concept, "root", True)
populate_code_system_concept_property_field(code_concept, "deprecated", False)

# continents_to_FHIR = create_continents_region(code_system, root.FHIRCode) # TODO

print("got", len(countries))
print("got", len(states))
print("got", len(districts))
print("got", len(suburbs))
for element in countries.values():
    unknown_state_code_concept = create_code_system_concept_instance(code_system, element)
    populate_code_system_concept_property_field(unknown_state_code_concept, "parent", root.FHIRCode)
    populate_code_system_concept_property_field(unknown_state_code_concept, "deprecated", False)
    populate_code_system_concept_property_field(unknown_state_code_concept, "root", False)

for element in states.values():
    unknown_state_code_concept = create_code_system_concept_instance(code_system, element)
    populate_code_system_concept_property_field(unknown_state_code_concept, "parent", element.parent)
    populate_code_system_concept_property_field(unknown_state_code_concept, "deprecated", False)
    populate_code_system_concept_property_field(unknown_state_code_concept, "root", False)

for element in districts.values():
    unknown_state_code_concept = create_code_system_concept_instance(code_system, element)
    populate_code_system_concept_property_field(unknown_state_code_concept, "parent", element.parent)
    populate_code_system_concept_property_field(unknown_state_code_concept, "deprecated", False)
    populate_code_system_concept_property_field(unknown_state_code_concept, "root", False)

for element in suburbs.values():
    unknown_state_code_concept = create_code_system_concept_instance(code_system, element)
    populate_code_system_concept_property_field(unknown_state_code_concept, "parent", element.parent)
    populate_code_system_concept_property_field(unknown_state_code_concept, "deprecated", False)
    populate_code_system_concept_property_field(unknown_state_code_concept, "root", False)

code_system.count = int(Region2.fhir_code_counter)

with open('newResultOutput.json', 'w') as fp:
    json.dump(code_system.as_json(), fp, indent=4)

with open("newOutputTest.txt", "w") as out:
    for element in countries.values():
        out.write(element.toJSON())
    for element in states.values():
        out.write(element.toJSON())
    for element in districts.values():
        out.write(element.toJSON())
    for element in suburbs.values():
        out.write(element.toJSON())






# import geopandas as gpd
# # Download from https://data.cityofnewyork.us/City-Government/Projected-Sea-Level-Rise/6an6-9htp directly...
# data = gpd.read_file("gadm28_levels.gdb", driver='FileGDB', layer=0)

# from poster.encode import multipart_encode
# from poster.streaminghttp import register_openers
# import urllib2
# import sys
#
# # Register the streaming http handlers with urllib2
# register_openers()
#
# # Use multipart encoding for the input files
# datagen, headers = multipart_encode({ 'files[]': open('gadm28_levels/gadm28_levels', 'rb')})
#
# # Create the request object
# request = urllib2.Request('https://www.rebasedata.com/api/v1/convert', datagen, headers)
#
# # Do the request and get the response
# # Here the GDB file gets converted to CSV
# response = urllib2.urlopen(request)
#
# # Check if an error came back
# if response.info().getheader('Content-Type') == 'application/json':
#     print response.read()
#     sys.exit(1)
#
# # Write the response to /tmp/output.zip
# with open('/tmp/output.zip', 'wb') as local_file:
#     local_file.write(response.read())
#
# print 'Conversion result successfully written to /tmp/output.zip!'
#
# input('done')
#
#
# with open('C:\\Users\\s4445655\\Downloads\\outputTest.txt', encoding="ISO-8859-1") as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0
#     header = []
#
#     for row in csv_reader:
#         if "Australia" in row:
#             print(row)
#             input('')
#         print(row)
#         input('')
            
##code_counter = "0000000"
##
##class Region:
##    def __init__(self, name, FHIR_code, parent_code):
##        self.name = name
##        self.FHIR_code = FHIR_code
##        self.parent_FHIR_code = parent_code
##
##    def __str__(self):
##        return 'Location name: ' + self.name + ' with code: ' + self.FHIR_code + ' and parent: ' + self.parent_FHIR_code
##
##    def output(self):
##        return {"name": self.name, "FHIR_code":self.FHIR_code, "parent_FHIR":self.parent_FHIR_code}
##
##    def toJSON(self):
##        return json.dumps(self, default=lambda o: o.output(),  # was __dict__
##                          sort_keys=True, indent=4)
##        
##

##
##

##
##countries_mapping = {}
##states_mapping = {}
##suburbs_mapping = {}
##
###TO DO, ADD EARTH AND CONTINENTS
##
##with open('C:\\Users\\s4445655\\Downloads\\outputTest.csv', encoding="ISO-8859-1") as csv_file:
##    csv_reader = csv.reader(csv_file, delimiter=',')
##    line_count = 0
##    header = []
##
##    for row in csv_reader:
##        if line_count == 0:
##            header = row
##        else:
##
##            if "Australia" in row:
##                print(row[6:])
####                print('21 is', row[21])
##            current_country = countries_mapping.get(row[6])
##            current_state = states_mapping.get(row[9])
##            current_suburb = suburbs_mapping.get(row[21])
##            if current_country is None:
##                current_country = Region(row[6], code_counter, "None")
##                countries_mapping[row[6]] = current_country
##                code_counter = '%07d' % (int(code_counter) + 1)
##            if current_state is None and row[9] != '': # Those that are islands, no state
##                current_state = Region(row[9], code_counter, current_country.FHIR_code)
##                states_mapping[row[9]] = current_state
##                code_counter = '%07d' % (int(code_counter) + 1)
##            if current_suburb is None and row[21] != '': # Those that doesn't have suburbs, just country/state
##                current_suburb = Region(row[21], code_counter, current_state.FHIR_code)
##                suburbs_mapping[row[21]] = current_suburb
##                code_counter = '%07d' % (int(code_counter) + 1)
##
##
##        line_count+=1
##
##with open('file.txt', 'w') as file:
##    for elements in list(countries_mapping.values()):
##        file.write(elements.toJSON())
##    for elements in list(states_mapping.values()):
##        file.write(elements.toJSON())
##    for elements in list(suburbs_mapping.values()):
##        file.write(elements.toJSON())
##        
####     file.write(simplejson.dumps(countries_mapping))
####     file.write(simplejson.dumps(states_mapping))
####     file.write(simplejson.dumps(suburbs_mapping))

