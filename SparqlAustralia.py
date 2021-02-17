"""
2020-2021 Vacation Project
@author: Chanon Kachornvuthidej, kac016@csiro.au, chanon.kachorn@gmail.com
@Supervisors: Dr Alejandro Metke Jimenez, Alejandro.Metke@csiro.au and Dr Hoa Ngo Hoa.Ngo@csiro.au

Only focus on Australian locations to produce neighbours using Sparql to query DBpedia database for data.

Some useful resources to check out:
# http://dev.grakn.ai/docs/examples/phone-calls-migration-python
# https://medium.com/virtuoso-blog/dbpedia-basic-queries-bc1ac172cc09
# http://dev.grakn.ai/docs/examples/phone-calls-migration-python
# https://sparqlwrapper.readthedocs.io/en/latest/main.html#how-to-use
# https://towardsdatascience.com/where-do-mayors-come-from-querying-wikidata-with-python-and-sparql-91f3c0af22e2


# PREFIX http://prefix.cc/dbr,dbo,dct,owl,prov,qb,qudt,rdf,rdfs,schema,skos,unit,xsd,sdmx.sparql
# http://prefix.cc/dbp

Note: This file is unused!

"""

import json



class SetEncoder(json.JSONEncoder):
    """
    Helper class to encode objects in JSON format.
    """
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

countries = []

with open('newResultOutput2.json') as json_file:
   data = json.load(json_file)
   for location in data['concept']:
      if location['display'] != "Earth" and  (location['code'] != '0001387' and
                                             location['code'] != '0001388' and
                                             location['code'] != '0001389' and
                                             location['code'] != '0001390' and
                                             location['code'] != '0001391' and
                                             location['code'] != '0001392' and
                                             location['code'] != '0001393' and
                                             location['code'] != '0000000'): #Also skip Australia!
                                             # Not the contients label and not the country levels
         countries.append((location['display'], location['property'][0]['valueCode']))

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

collection = {}

# construct link to query based on location names
for country in countries:
    countryName = country[0].strip()
    remove_space = countryName.replace(" ", "_")
    link = None
    if country[1] == "0000002":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_Australian_Capital_Territory'
    elif country[1] == "0000005":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_New_South_Wales'
    elif country[1] == "0000006":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_Northern_Territory'
    elif country[1] == "0000007":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_Queensland'
    elif country[1] == "0000008":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_South_Australia'
    elif country[1] == "0000009":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_Tasmania'
    elif country[1] == "0000010":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_Victoria'
    elif country[1] == "0000011":
        link = 'http://dbpedia.org/resource/' + remove_space + ',_Western_Australia'
    else:
        print(country) # The islands and states skip for now!
        continue

    query = "PREFIX dbp: <http://dbpedia.org/property/> SELECT ?north ?northeast ?northwest ?south ?southeast ?southwest ?east ?west WHERE { <{link}> dbp:nearN ?north; dbp:nearNe ?northeast; dbp:nearNw ?northwest;" \
           "dbp:nearS ?south; dbp:nearSe ?southeast; dbp:nearSw ?southwest; dbp:nearE ?east; dbp:nearW ?west }".replace("{link}", link)


    # Perform the querying
    try:
      sparql.setQuery(query)
      sparql.setReturnFormat(JSON)
      results = sparql.query().convert()
    except: # what ever error we ignore it for now, most of the time the error is from invalid link
      continue

    linking = {}


    if len(results["results"]["bindings"]) == 0:
      continue # Something went wrong. Either it's not a suburb or broken link, just keep going

    # extract data from the query. Only info on neighbouring suburbs are extracted.
    for data in results["results"]["bindings"]:
      for direction in ['north', 'northeast', 'northwest', 'south', 'southeast', 'southwest', 'east', 'west']:
         neighbour = data[direction]['value'].replace('Province','').split(',')[0].strip() # extract neighbour information
         existing = linking.get(direction)
         if existing is None:
            existing = set()
         existing.add(neighbour)
         linking[direction] = existing


    collection[country[0]] = linking


with open("AustralianNeighbours(Sparql).json", "w") as testingFile:
    testingFile.write(json.dumps(collection, cls=SetEncoder))
