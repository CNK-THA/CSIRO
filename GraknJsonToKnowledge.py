"""
@author Chanon Kachornvuthij, kac016@csiro.au, chanon.kachorn@gmail.com

Transform sburbs JSON into a knowledge graph on Grakn.
"""
# from grakn.client import GraknClient
# https://docs.grakn.ai/docs/examples/phone-calls-schema
# https://docs.grakn.ai/docs/client-api/python

import json

# with GraknClient(uri="localhost:48555") as client:
#     with client.session(keyspace="locations") as session:
#         client.keyspaces().delete('locations')
# input('done')

list_of_all_suburbs = set()
with open('AustralianNeighbours(Wptools).json') as json_file1:
    data = json.load(json_file1)
    for location in data:
        print(location.split(',')[0])
        for direction in data[location]:
            processed = data[location][direction].replace('[', '').replace(']', '').replace("'", '').replace(" ",'_').split(',')[0].split('|')
            location_processed = location.split(',')
            list_of_all_suburbs.add(processed[0])
            list_of_all_suburbs.add(location_processed[0])
# input('stop')


with open('AustralianNeighbours(Wptools).json') as json_file1:
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace="locations") as session:
            # client.keyspaces().delete('locations')
            for suburb in list_of_all_suburbs:
            # Adding the suburbs to the database, ran once!
                with session.transaction().write() as write_transaction:
                    query = 'insert $x isa suburb, has name "{suburbName}";'.format(suburbName=suburb)
                    insert_iterator = write_transaction.query(query).get()
                    concepts = [ans.get("x") for ans in insert_iterator]
                    print("Inserted a suburb with ID: {0}".format(concepts[0].id))
                    ## to persist changes, write transaction must always be committed (closed)
                    write_transaction.commit()

            data = json.load(json_file1)
            for location in data:

                # print(location)
                # input(data[location])

                # Adding the suburbs to the database, ran once!
                # with session.transaction().write() as write_transaction:
                #     location = location.split(',')
                #     # print(location[0])
                #     query = 'insert $x isa suburb, has name "{suburbName}";'.format(suburbName=location[0])
                #     print(query)
                #     insert_iterator = write_transaction.query(query).get()
                #     concepts = [ans.get("x") for ans in insert_iterator]
                #     print("Inserted a suburb with ID: {0}".format(concepts[0].id))
                #     ## to persist changes, write transaction must always be committed (closed)
                #     write_transaction.commit()

                for direction in data[location]:
                    # print(direction)
                    # print(data[location][direction].replace('[','').replace(']',''))
                    processed = data[location][direction].replace('[','').replace(']','').replace("'",'').replace(" ",'_').split(',')[0].split('|')

                    location_processed = location.split(',') # if have multiple then just get the first one
                    try:
                        with session.transaction().write() as write_transaction:
                            query = 'match $x isa suburb, has name "{suburbA}"; $y isa suburb, has name "{suburbB}"; ' \
                                    'insert $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $relationship has direction "{direct}";'.format(suburbA=location_processed[0], suburbB=processed[0], direct=direction)
                            # input(query)
                            insert_iterator = write_transaction.query(query).get()
                            concepts = [ans.get("x") for ans in insert_iterator]
                            print("Inserted a suburb with ID: {0}".format(concepts[0].id))
                            ## to persist changes, write transaction must always be committed (closed)
                            write_transaction.commit()
                    except:
                        print("ERROR")
                        pass


                        # with session.transaction().read() as read_transaction:
                        #     answer_iterator = read_transaction.query("match $name isa suburb; $name has name 'Annerley'; get $name; offset 0; limit 10;").get()
                        #     for answer in answer_iterator:
                        #         # print(answer)
                        #         person = answer.map().get("name")
                        #         # print(answer.map())
                        #         # print(person)
                        #         print("Retrieved suburb with id " + person.id)






# # https://docs.grakn.ai/docs/general/quickstart
# with GraknClient(uri="localhost:48555") as client:
#     # client.keyspaces().delete('locations')
#
#     with client.session(keyspace="locations") as session:
#         # pass
#         ## Insert a Person using a WRITE transaction
#         # with session.transaction().write() as write_transaction:
#         #     insert_iterator = write_transaction.query('insert $x isa suburb, has name "suburbE";').get()
#         #     concepts = [ans.get("x") for ans in insert_iterator]
#         #     print("Inserted a suburb with ID: {0}".format(concepts[0].id))
#         #     ## to persist changes, write transaction must always be committed (closed)
#         #     write_transaction.commit()
#
#     #     ## Insert Relation!
#         with session.transaction().write() as write_transaction:
#             insert_iterator = write_transaction.query('match $x isa suburb, has name "suburbD"; $y isa suburb, has name "suburbE";'
#                                                       'insert $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $relationship has direction "west";').get()
#             concepts = [ans.get("x") for ans in insert_iterator]
#             print("Inserted a suburb with ID: {0}".format(concepts[0].id))
#             ## to persist changes, write transaction must always be committed (closed)
#             write_transaction.commit()
#     #
#     #     # Read the person using a READ only transaction
#     #     # with session.transaction().read() as read_transaction:
#     #     #     answer_iterator = read_transaction.query("match $name isa suburb; get $name; limit 10;").get()
#     #     # # match $tra (traveler: $per) isa travel; (located-travel: $tra, travel-location: $loc) isa location-of-travel; $loc has name "French Lick"; $per has full-name $fn; get $fn;
#     #     #
#     #     #     for answer in answer_iterator:
#     #     #         # print(answer)
#     #     #         person = answer.map().get("name")
#     #     #         # print(answer.map())
#     #     #         # print(person)
#     #     #         print("Retrieved suburb with id " + person.id)
#     #
#     #     ## Or query and consume the iterator immediately collecting all the results
#     #     # with session.transaction().read() as read_transaction:
#     #     #     # pass
#     #     #     answer_iterator = read_transaction.query("match $x isa suburb; get; limit 10;").get()
#     #     #     persons = [ans.get("x") for ans in answer_iterator]
#     #     #     for person in persons:
#     #     #         print("Retrieved person with id "+ person.id)
#     #
#     #     ## if not using a `with` statement, then we must always close the session and the read transaction
#     #     # read_transaction.close()
#     #     # session.close()
#     #     # client.close()
#
#

# Queries to run on Grakn graph
# # show entity with attributes link
# # match $x isa suburb; $x has attribute $a; get;
# # show relationship with attribute direction
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $emp has attribute $b; get; offset 0; limit 30;
# # Like abbove bbut show all attributes!
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has attribute $m; $y has attribute $p; $emp has attribute $b; get; offset 0; limit 2;
# # Show specific suburb with all it's neighbours
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $y has attribute $o; $emp has attribute $b; get; offset 0; limit 30;