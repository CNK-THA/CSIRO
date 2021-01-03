

def create_continents_region2(code, earth):
    continents = [("North America", "NA"), ("South America", "SA"), ("Africa","AF"), ("Antarctica","AN"), ("Europe","EU"), ("Oceania","OC"), ("Asia","AS")]
    continents_to_FHIR = {}
    for location in continents:
        current_location = Region2(location[0], earth)
        code_concept = create_code_system_concept_instance(code, current_location)
        populate_code_system_concept_property_field(code_concept, "parent", current_location.parent)
        populate_code_system_concept_property_field(code_concept, "root", False)
        populate_code_system_concept_property_field(code_concept, "deprecated", False)
        continents_to_FHIR[location[1]] = current_location.FHIRCode
    return continents_to_FHIR

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

import fiona
from main import *


if __name__ == '__main__':

    countries = {}
    states = {}
    districts = {}
    suburbs = {}


    for layername in fiona.listlayers("gadm28_levels.shp"):
        with fiona.open("gadm28_levels.shp", layer=layername) as c:
            current_location = c.next()
            print("there are:", len(c), "in total")
            while True:
                if layername == "gadm28_adm0": # countries level
                    new_country = Region2(current_location['properties']['NAME_ENGLI'], "None")
                    if current_location['properties']['UNREGION1'] is None:
                        countries[current_location['properties']['ISO']] = (current_location['properties']['NAME_ENGLI'], new_country)
                    else:
                        countries[current_location['properties']['ISO']] = (current_location['properties']['UNREGION1'], new_country)
                elif layername == "gadm28_adm1": # states level
                    if countries.get(current_location['properties']['ISO']) is not None and current_location['properties']['NAME_1'] is not None and states.get(current_location['properties']['NAME_1']) is None: # Bonaire, Saint Eustatius and Saba MISSPELLED #instead of name_0
                        new_state = Region2(current_location['properties']['NAME_1'], countries.get(current_location['properties']['ISO'])[1].FHIRCode)
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

    root = Region2("Earth", None)
    code_concept = create_code_system_concept_instance(code_system, root)
    populate_code_system_concept_property_field(code_concept, "root", True)
    populate_code_system_concept_property_field(code_concept, "deprecated", False)

    continents_to_FHIR = create_continents_region2(code_system, root.FHIRCode)

    print("got", len(countries))
    print("got", len(states))
    print("got", len(districts))
    print("got", len(suburbs))
    for element in countries.values():
        unknown_state_code_concept = create_code_system_concept_instance(code_system, element[1])
        if "Asia" in element[0] or "British Indian Ocean Territory" in element[0] or "Caspian Sea" in element[0] or "Paracel Islands" in element[0] or \
                "Spratly islands" in element[0]: # the sea could be in Europe?
            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", continents_to_FHIR.get("AS"))
        elif "Europe" in element[0] or "Akrotiri and Dhekelia" in element[0] or "Kosovo" in element[0] or "Northern Cyprus" in element[0]:
            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", continents_to_FHIR.get("EU"))
        elif "Africa" in element[0] or "South Sudan" in element[0]:
            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", continents_to_FHIR.get("AF"))
        elif "Polynesia" in element[0] or "Australia" in element[0] or "Christmas Island" in element[0] or "Cocos Islands" in element[0] or "Melanesia" in element[0] or \
                "Micronesia" in element[0]: # part of Oceania
            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", continents_to_FHIR.get("OC"))
        elif "Caribbean" in element[0] or "Central America" in element[0] or "Clipperton Island" in element[0] or "Saint-Martin" in element[0] or \
                "United States Minor Outlying Islands" in element[0] or "Northern America" in element[0]: # North America
            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", continents_to_FHIR.get("NA"))
        elif "Antarctica" in element[0] or "Bouvet Island" in element[0] or "French Southern Territories" in element[0] or "Heard Island and McDonald Islands" in element[0] or \
                "South Georgia and the South Sandwich Islands" in element[0] or "Antartica" in element[0]:
            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", continents_to_FHIR.get("AN"))
        elif "South America" in element[0]:
            populate_code_system_concept_property_field(unknown_state_code_concept, "parent", continents_to_FHIR.get("SA"))
        else:
            input(element[0])

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
            out.write(element[1].toJSON())
        for element in states.values():
            out.write(element.toJSON())
        for element in districts.values():
            out.write(element.toJSON())
        for element in suburbs.values():
            out.write(element.toJSON())
