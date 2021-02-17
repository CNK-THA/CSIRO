"""
2020-2021 Vacation Project
@author: Chanon Kachornvuthidej, kac016@csiro.au, chanon.kachorn@gmail.com
@Supervisors: Dr Alejandro Metke Jimenez, Alejandro.Metke@csiro.au and Dr Hoa Ngo Hoa.Ngo@csiro.au

Generate txt containing neighbours of all Global suburbs.

Note: This file is unused!
"""


import json

class SetEncoder(json.JSONEncoder):
   """
   Helper class to encode data into JSON object.
   """
   def default(self, obj):
      if isinstance(obj, set):
         return list(obj)
      return json.JSONEncoder.default(self, obj)

countries = []

with open('newResultOutput.json') as json_file:
   data = json.load(json_file)
   for location in data['concept']: # Note that these valueCode is hardCoded, future implementation needs to change these
      # Ignore the continents level and extract only the countries and below!
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


   try: # <http://dbpedia.org/resource/Al_Isma`iliyah> causing error!!!
      sparql.setQuery(query)
      sparql.setReturnFormat(JSON)
      results = sparql.query().convert()
   except: # what ever error we ignore it
      print("error")
      continue


   linking = {}


   if len(results["results"]["bindings"]) == 0:

      continue # Something went wrong. Either it's not a suburb or broken link, ignore it for now

   for data in results["results"]["bindings"]:
      for direction in ['north', 'northeast', 'northwest', 'south', 'southeast', 'southwest', 'east', 'west']:
         neighbour = data[direction]['value'].replace('Province','').split(',')[0].strip() # SPLIT ON COMMA
         existing = linking.get(direction)
         if existing is None:
            existing = set()
         existing.add(neighbour)
         linking[direction] = existing



   collection[country] = linking

with open("GlobalDataNeighbours(Sparql).txt", "a") as testingFile:
   testingFile.write(json.dumps(collection, cls=SetEncoder))
