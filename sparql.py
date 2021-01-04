from SPARQLWrapper import SPARQLWrapper, JSON

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
    SELECT ?label
    WHERE { <http://dbpedia.org/resource/Australia> rdfs:label ?label }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

print(results)

for result in results["results"]["bindings"]:
    print(result["label"]["value"])

print('---------------------------')

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