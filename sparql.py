
# http://dev.grakn.ai/docs/examples/phone-calls-migration-python
# https://medium.com/virtuoso-blog/dbpedia-basic-queries-bc1ac172cc09
# http://dev.grakn.ai/docs/examples/phone-calls-migration-python
# https://sparqlwrapper.readthedocs.io/en/latest/main.html#how-to-use
# https://towardsdatascience.com/where-do-mayors-come-from-querying-wikidata-with-python-and-sparql-91f3c0af22e2


# PREFIX http://prefix.cc/dbr,dbo,dct,owl,prov,qb,qudt,rdf,rdfs,schema,skos,unit,xsd,sdmx.sparql
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
      if location['display'] != "Earth" and (location['property'][0]['valueCode'] != '0151626' and
                                             location['property'][0]['valueCode'] != '0151620' and
                                             location['property'][0]['valueCode'] != '0151621' and
                                             location['property'][0]['valueCode'] != '0151622' and
                                             location['property'][0]['valueCode'] != '0151623' and
                                             location['property'][0]['valueCode'] != '0151624' and
                                             location['property'][0]['valueCode'] != '0151625') and \
                                             (location['code'] != '0151626' and
                                             location['code'] != '0151620' and
                                             location['code'] != '0151621' and
                                             location['code'] != '0151622' and
                                             location['code'] != '0151623' and
                                             location['code'] != '0151624' and
                                             location['code'] != '0151625'):
                                             #(location['property'][0]['valueCode'] == "0151625" ): # Not the contients label and not the country levels
         countries.append(location['display'])

from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")

collection = {}

for country in countries:
   country = country.strip()
   remove_space = country.replace(" ", "_")
   link = 'http://dbpedia.org/resource/' + remove_space

   query = "PREFIX dbo: <http://dbpedia.org/ontology/> SELECT ?north ?northeast ?northwest ?south ?southeast ?southwest ?east ?west WHERE { <{link}> dbp:north ?north; dbp:northeast ?northeast; dbp:northwest ?northwest;" \
           "dbp:south ?south; dbp:southeast ?southeast; dbp:southwest ?southwest; dbp:east ?east; dbp:west ?west }".replace("{link}", link)   #  """SELECT *WHERE{?location rdfs:label "New Zealand"@en}"""

   # query = "PREFIX dbo: <http://dbpedia.org/ontology/> SELECT ?north ?northeast ?northwest ?south ?southeast ?southwest ?east ?west WHERE { <{link}> dbp:nearN ?north; dbp:nearNe ?northeast; dbp:nearNw ?northwest;" \
   #         "dbp:nearS ?south; dbp:nearSe ?southeast; dbp:nearSw ?southwest; dbp:nearE ?east; dbp:nearW ?west }".replace("{link}", link)

   # query = "PREFIX dbo: <http://dbpedia.org/ontology/> SELECT ?north ?northeast ?northwest ?south ?southeast ?southwest ?east ?west WHERE { <http://dbpedia.org/resource/Sunnybank,_Queensland> dbp:nearN ?north; dbp:nearNe ?northeast; dbp:nearNw ?northwest;" \
   #         "dbp:nearS ?south; dbp:nearSe ?southeast; dbp:nearSw ?southwest; dbp:nearE ?east; dbp:nearW ?west }"

   print(query)
   try: # <http://dbpedia.org/resource/Al_Isma`iliyah> causing error!!!
      sparql.setQuery(query)
      sparql.setReturnFormat(JSON)
      results = sparql.query().convert()
   except: # what ever error we ignore it
      print("error")
      continue

   print(results)
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
   collection[country] = linking

   print(query)
   print("GOT HERE")
with open("test2.txt", "a") as testingFile:
   testingFile.write(json.dumps(collection, cls=SetEncoder))



   # print(results["results"]["bindings"][2]['location']['value'])




# for result in results["results"]["bindings"]:
#     print('%s: %s' % (result["label"]["xml:lang"], result["label"]["value"]))


# from SPARQLWrapper import SPARQLWrapper
#
# queryString = "SELECT ?craft{?craft a space:Spacecraft}LIMIT 50"
# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
#
# sparql.setQuery(queryString)
#
# try :
#    ret = sparql.query()
#    print(ret)
#    # ret is a stream with the results in XML, see <http://www.w3.org/TR/rdf-sparql-XMLres/>
# except :
#    print("ERROR")