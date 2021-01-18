"""
@author Chanon Kachornvuthij, kac016@csiro.au, chanon.kachorn@gmail.com

Similarly to SparqlGlobal, only focus on Australian locations to produce neighbours using Sparql and DBpedia.
"""
# http://dev.grakn.ai/docs/examples/phone-calls-migration-python
# https://medium.com/virtuoso-blog/dbpedia-basic-queries-bc1ac172cc09
# http://dev.grakn.ai/docs/examples/phone-calls-migration-python
# https://sparqlwrapper.readthedocs.io/en/latest/main.html#how-to-use
# https://towardsdatascience.com/where-do-mayors-come-from-querying-wikidata-with-python-and-sparql-91f3c0af22e2


# PREFIX http://prefix.cc/dbr,dbo,dct,owl,prov,qb,qudt,rdf,rdfs,schema,skos,unit,xsd,sdmx.sparql
# http://prefix.cc/dbp
import json



class SetEncoder(json.JSONEncoder):
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

for country in countries:
    countryName = country[0].strip()
    remove_space = countryName.replace(" ", "_")
    link = None
    if country[1] == "0000002": # NSW DOESN'T NEED THE EXTENSION??
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
        print(country) # The islands and states skip!
        continue

    query = "PREFIX dbp: <http://dbpedia.org/property/> SELECT ?north ?northeast ?northwest ?south ?southeast ?southwest ?east ?west WHERE { <{link}> dbp:nearN ?north; dbp:nearNe ?northeast; dbp:nearNw ?northwest;" \
           "dbp:nearS ?south; dbp:nearSe ?southeast; dbp:nearSw ?southwest; dbp:nearE ?east; dbp:nearW ?west }".replace("{link}", link)

    # print(query)
    try: # <http://dbpedia.org/resource/Al_Isma`iliyah> causing error!!!
      sparql.setQuery(query)
      sparql.setReturnFormat(JSON)
      results = sparql.query().convert()
    except: # what ever error we ignore it
      print("error")
      continue

    # print(results)
    linking = {}


    if len(results["results"]["bindings"]) == 0:
      # link = 'http://dbpedia.org/page/' + remove_space + "_Province"
      # query = "PREFIX dbo: <http://dbpedia.org/ontology/> SELECT ?label WHERE { <{link}> rdfs:label ?label }".replace(
      #    "{link}", link)
      # # query = """SELECT *WHERE{?location rdfs:label "{name}"@en}""".replace("{name}", country)
      #
      # # print(query)
      # sparql.setQuery(query)
      # sparql.setReturnFormat(JSON)
      # results = sparql.query().convert()
      # # print(results)
      # # print("SKIPPING")
      # print("--------------------------------------------ERROR-----------------------------------------")
      continue # Something went wrong. Either it's not a suburb or broken link

    for data in results["results"]["bindings"]:
      for direction in ['north', 'northeast', 'northwest', 'south', 'southeast', 'southwest', 'east', 'west']:
         neighbour = data[direction]['value'].replace('Province','').split(',')[0].strip() # SPLIT ON COMMA, ANY NAME WITH THAT???
         existing = linking.get(direction)
         if existing is None:
            existing = set()
         existing.add(neighbour)
         linking[direction] = existing


    # print(linking)
    collection[country[0]] = linking

    # print(query)
    # print("GOT HERE")
with open("test2.txt", "w") as testingFile:
    testingFile.write(json.dumps(collection, cls=SetEncoder))
