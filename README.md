# CSIRO Mining Wikipedia to Generate a Geographic Location Ontology

A framework to represent coded geographical data in [FHIR CodeSystem](https://www.hl7.org/fhir/codesystem.html) in JSON format able to be shared and utilised across the healthcare industry.

## Requirements
The req.txt and environment.yml files specifies all packages needed to run all scripts contained in this repository and setting up of [Conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html). 

In addition, [Grakn Knowledge - Graph Core and Workbase components](https://grakn.ai/download) are also required.

## Administrative divisions
Geographical locations in this project utilise the following hierarchy:

**Level 0**: Root - Earth

**Level 1**: Continents (e.g. Oceania)

**Level 2**: Countries (e.g. Australia)

**Level 3**: States (e.g. State of Queensland)

**Level 4**: Cities (e.g. Brisbane City)

**Level 5**: Suburbs (e.g. Herston)

## Input
Prior to running any scripts in the current repository, data and supporting files needs to be downloaded from the 3 database servers. Note some required files are already contained in this repository:

1. [GeoNames](http://download.geonames.org/export/dump/) (allCountries.zip) containing details of all
geographical locations around the world. Once extracted a .txt file with data of all countries should exist.

2. [GeoNames](http://download.geonames.org/export/dump/) (countryInfo.txt) containing country code (e.g. Australia - AU, United States - US etc), used to map country code to it's full name during data extraction. This file is already contained in the repository.

3. [GADM](https://gadm.org/old_versions.html) (gadm28_levels.shp.zip) geo data in *six separate layers* as *shapefiles*. Version 2.8 is used in this current project.

4. [NGA GeoNames](https://geonames.nga.mil/gns/html/namefiles.html) (geonames_20210208.zip) entire country file dataset.

Place all extracted files inside the same directory as the python scripts.

## Output
Sets of .json and .txt file will be produced after running each of the scripts. Here is a guide to interpret the files:

1. GlobalData(GeoNamesx).json, x is a number 1, 2 or 3. These files contains global geographical data in FHIR CodeSystem format (except GeoNames3 where it is just JSON object) showing the parent-child relationship with the 5-level hierarchy as produced b their respective GeoNamesx.py scripts.

2. AustralianLocations.json and .txt files. These files contains only Australian data in FHIR CodeSystem (.json) and as JSON object dump (.txt) produced from GeoNames2.py

3. SuburbsLevelOnly(GeoNames2).txt produced from GeoNames2.py and contains only Australian suburbs as JSON object. This is only used with SPARQL querying which is no longer used in this project.

4. GlobalDataNeighbours(Sparql).txt produced from SparqlGlobal.py containing data of all suburbs and neighbours from around the world queried from DBPedia. Now unused in the project.

5. AustralianNeighbours(Sparql).json produced from SparqlAustralia.py containing data of all suburbs and neighbours in Australia queried from DBPedia and now unused in the current project.

6. AustralianNeighbours(Wptools).json produced from the WPToolsAustralia.py containing data of all suburbs and neighbours in Australia queried from Wikipedia pages, this is the latest and version used for development.

## Running the code
Python scripts can be run in the following order. Make sure that Conda environment has been activated and all required packages installed with the correct version. Each scripts will have to be manually ran one after the other:

1. GeoNames1/2/3.py These will open/parse all the downloaded database and it's supporting files ad produce outputs of relevant data in JSON and FHIR CodeSystem format. Note the 3 GeoNames scripts does not have to be run in parallel, and can be in any particular order.
2. CombineGeoNames.py will then attempt to combine the relevant files and produce one .json file for importation into Grakn Knowledge Graph (AustralianLocations.json)
3. WpToolsAustralia.py. This will read the output file from CombeinGeoNames.py and query Wikipedia pages to retrieve neighbouring information of Australian suburbs. Will produce AustralianNeighbours(Wptools).json. Alternatively SparqlAustralia.py or SparqlGlobal.py could be run instead here to query DBPedia database (now unused in the current project).
4. Activate (if haven't done so) the Grakn database following [these instructions](https://docs.grakn.ai/docs/general/quickstart) to start and import the schema (locations.gql, or locations_withVersioning.gql if viewing the versioning feature)
5. GraknJSONToKnowledge.py will import the produced AustralianNeighbours(WpTools).json file into the Grakn knowledge graph which shows both entity (suburb locations) and relationships (neighbour and directions)
6. Open Grakn Workbase application and query the knowledge graph (see bottom of GraknJSONToKnowledge.py file)
7. Test the produced FHIR CodeSystem (from step 1 and 2) that it complies with the FHIR standards and is bug free with FHIRJSONTesting.py

## Additional Files
FHIR_Example_Alejandro.json is an example of the FHIR CodeSystem in use in other project used as a development referenence.
locations.gql is the knowledge graph schema imported into Grakn database prior to importing data (see step 5 in Running the code).
locations_withVersioning.gql is the knolwedge graph schema with proof of concept withe versioning feature (still in development).

## Known Bugs / Limitations
- Some suburbs are producing errors when querying Wikipedia (WpToolsAustralia.py). Currently ignoring all errors and skipping suburbs that produce them.
- Combining different databases together with string matching algorithm is partially working, still requires future development in CombineGeoNames.py.
- Any errors produced in GeoNamesx.py files are ignore and record skipped.
- Some of the scripts will require manual edits to file paths/names/uncommenting/commenting sections of the code for different purposes and versions to inspect e.g. viewing only Australian information outputs vs global outputs, knowledge graph import with versioning and without versioning

## Further Development
- Expand administrative divisions to level 5 and 6 as contained in GeoNames database. Modifications to be made to GeoNames1/2/3.py

- Support data input from various sources not just GeoNames

- Effective handling of *unknown locations* and the *code* assignment

- Querying the knowledge graph to produce a FHIR CodeSystem instead of straight from step 1-2 (see Running the code section)

- Expand testing to be more inclusive and thorough in FHIRJSONTesting.py