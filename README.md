# CSIRO Ontology

An application to produce [FHIR CodeSystem](https://www.hl7.org/fhir/codesystem.html) in JSON format 

## Requirements

Python 3

[fhir.resources 6.0.0](https://pypi.org/project/fhir.resources/)  `pip install fhir.resources`

## Input

1. [GeoNames](http://download.geonames.org/export/dump/) .txt file (allCountries.zip) containing details of all
geographical locations around the world.

2. countryInfo.txt file mapping between country name and country code (see GeoNames link)



## Output

JSON file in FHIR supported format containing all administrative divisions around the
world

Each location are asigned a *code* which is a 7 digit incremental number starting at 0000000, and a parent location

## Administrative Divisions
**Level 0**: Root - Earth

**Level 1**: Countries (e.g. Australia)

**Level 2**: States (e.g. State of Queensland)

**Level 3**: Cities (e.g. Brisbane City)

**Level 4**: Suburbs (e.g. Herston)

## Further Development

- Expand administrative divisions to level 5 and 6 as contained in GeoNames database

- Support data input from various sources not just GeoNames

- Effective handling of *unknown locations* and the *code* assignment