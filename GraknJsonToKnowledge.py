"""
@author Chanon Kachornvuthij, kac016@csiro.au, chanon.kachorn@gmail.com

Transform sburbs JSON into a knowledge graph on Grakn.
"""
from grakn.client import GraknClient
# https://docs.grakn.ai/docs/examples/phone-calls-schema
# https://docs.grakn.ai/docs/client-api/python

import json

# with GraknClient(uri="localhost:48555") as client:
#     with client.session(keyspace="locations_with_versioning") as session:
#         client.keyspaces().delete('locations_with_versioning')
# input('done')

list_of_all_suburbs = set()
with open('AustralianNeighbours(Wptools).json') as json_file1:
    data = json.load(json_file1)
    for location in data:
        for direction in data[location]:
            processed = data[location][direction].replace('[', '').replace(']', '').replace("'", '').replace(" ",'_').split(',')[0].split('|')
            location_processed = location.split(',')
            if "Queensland" in location_processed[1] and "Herston" in processed: # only get Queensland locations
                list_of_all_suburbs.add(processed[0])
                list_of_all_suburbs.add(location_processed[0])
# input('stop')


with open('AustralianNeighbours(Wptools).json') as json_file1:
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace="locations_with_versioning") as session:

            count = 0
            for suburb in list_of_all_suburbs:
            # Adding the suburbs to the database, ran once!
                with session.transaction().write() as write_transaction:
                    query = 'insert $x isa suburb, has name "{suburbName}", has versionNumber 1;'.format(suburbName=suburb)
                    insert_iterator = write_transaction.query(query).get()
                    concepts = [ans.get("x") for ans in insert_iterator]
                    # print("Inserted a suburb with ID: {0}".format(concepts[0].id))
                    print("Inserted a suburb with name", suburb)
                    ## to persist changes, write transaction must always be committed (closed)
                    write_transaction.commit()
                    count += 1

            print("in total there are", count)


            count = 0
            data = json.load(json_file1)
            for location in data:

                count += 1
                # print("currently adding", count)
                for direction in data[location]:
                    # print(direction)
                    # print(data[location][direction].replace('[','').replace(']',''))
                    processed = data[location][direction].replace('[','').replace(']','').replace("'",'').replace(" ",'_').split(',')[0].split('|')


                    location_processed = location.split(',') # if have multiple then just get the first one
                    if "Queensland" not in location_processed[1] or ("Herston" not in processed and "Herston" not in location_processed[0]):  # only get Queensland locations
                        continue

                    try:
                        with session.transaction().write() as write_transaction:
                            query = 'match $x isa suburb, has name "{suburbA}", has versionNumber 1; $y isa suburb, has name "{suburbB}", has versionNumber 1; ' \
                                    'insert $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $relationship has direction "{direct}", has versionNumber 1;'.format(suburbA=location_processed[0], suburbB=processed[0], direct=direction)
                            # input(query)
                            insert_iterator = write_transaction.query(query).get()
                            concepts = [ans.get("x") for ans in insert_iterator]
                            print("Inserted a neighbour with ID: {0}".format(concepts[0].id))
                            print("added", location_processed[0], "with", processed[0], "direction", direction)
                            ## to persist changes, write transaction must always be committed (closed)
                            write_transaction.commit()
                    except:
                        print("ERROR")
                        pass

            with session.transaction().write() as write_transaction:
                query = 'insert $x isa version_tracker, has versionNumber 1, has date 2021-01-22;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("Inserted a version_tracker with ID: {0}".format(concepts[0].id))

                ## to persist changes, write transaction must always be committed (closed)
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'insert $x isa version_tracker, has versionNumber 2, has date 2022-01-22;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("Inserted a version_tracker with ID: {0}".format(concepts[0].id))

                ## to persist changes, write transaction must always be committed (closed)
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'match $x isa version_tracker, has versionNumber 1; $y isa version_tracker, has versionNumber 2; ' \
                        'insert $relationship (current: $x, next: $y) isa version_update;'
                # input(query)
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                # print("Inserted a neighbour with ID: {0}".format(concepts[0].id))
                print("added", "version 1", "with", "version 2")
                ## to persist changes, write transaction must always be committed (closed)
                write_transaction.commit()

            # TESTING ONLY
            with session.transaction().write() as write_transaction:
                query = 'insert $x isa suburb, has name "New_Spring_Hill", has versionNumber 2;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                # print("Inserted a suburb with ID: {0}".format(concepts[0].id))
                print("Inserted a suburb with name", "New_Spring_Hill")
                ## to persist changes, write transaction must always be committed (closed)
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'match $x isa suburb, has name "Herston", has versionNumber 1; $y isa suburb, has name "New_Spring_Hill", has versionNumber 2; ' \
                        'insert $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $relationship has direction "s", has versionNumber 2;'
                # input(query)
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                # print("Inserted a neighbour with ID: {0}".format(concepts[0].id))
                print("added", "New_Spring_Hill", "with", "Herston", "direction", "s")
                ## to persist changes, write transaction must always be committed (closed)
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'match $x isa suburb, has name "Spring_Hill", has versionNumber 1; $y isa suburb, has name "New_Spring_Hill", has versionNumber 2; ' \
                        'insert $relationship (old: $x, new: $y) isa suburb_update;'
                # input(query)
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                # print("Inserted a neighbour with ID: {0}".format(concepts[0].id))
                print("added", "New_Spring_Hill", "with", "Spring_Hill")
                ## to persist changes, write transaction must always be committed (closed)
                write_transaction.commit()


# Queries to run on Grakn graph
# # show entity with attributes link
# # match $x isa suburb; $x has attribute $a; get;
# # show relationship with attribute direction
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $emp has attribute $b; get; offset 0; limit 30;
# # Like abbove bbut show all attributes!
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has attribute $m; $y has attribute $p; $emp has attribute $b; get; offset 0; limit 2;

# # Show specific suburb with all it's neighbours
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $x has attribute $q; $y has attribute $f; $y has attribute $o; $emp has attribute $k; $emp has attribute $b; get; offset 0; limit 30;
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $y has attribute $f; $emp has attribute $k; get; offset 0; limit 30;

# Show version control
# # match $emp (current: $x, next: $y) isa version_update; $x has attribute $t; $y has attribute $f; get; offset 0; limit 30;

# Show suburb updates
# # match $emp (old: $x, new: $y) isa suburb_update; $x has attribute $t; $y has attribute $f; get; offset 0; limit 30;

# Show all updates
#  match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $y has attribute $f; get; offset 0; limit 30;

# Get direction South most up to date
# match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $y has attribute $f; $emp has direction "s"; $emp has attribute $u; get; offset 0; limit 30;