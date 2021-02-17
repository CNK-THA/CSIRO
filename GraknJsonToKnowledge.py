"""
2020-2021 Vacation Project
@author: Chanon Kachornvuthidej, kac016@csiro.au, chanon.kachorn@gmail.com
@Supervisors: Dr Alejandro Metke Jimenez, Alejandro.Metke@csiro.au and Dr Hoa Ngo Hoa.Ngo@csiro.au

Import subrbs from JSON file into a knowledge graph on Grakn.
"""
from grakn.client import GraknClient
import json

# Uncomment and run this if want to remove a keyspace
# with GraknClient(uri="localhost:48555") as client:
#     with client.session(keyspace="locations_with_versioning") as session:
#         client.keyspaces().delete('locations_with_versioning')


list_of_all_suburbs = set()

# Read only locations in Queensland
with open('AustralianNeighbours(Wptools).json') as json_file1:
    data = json.load(json_file1)
    for location in data:
        for direction in data[location]:
            processed = \
                data[location][direction].replace('[', '').replace(']', '').replace("'", '').replace(" ", '_').split(
                    ',')[
                    0].split('|')
            location_processed = location.split(',')
            if "Queensland" in location_processed[1]:  # and "Herston" in processed: # only get Queensland locations
                list_of_all_suburbs.add(processed[0])
                list_of_all_suburbs.add(location_processed[0])

# Once locations are read from the file, import it into the knowledge graph
with open('AustralianNeighbours(Wptools).json') as json_file1:
    with GraknClient(uri="localhost:48555") as client:
        with client.session(keyspace="locations_with_versioning") as session:

            count = 0
            for suburb in list_of_all_suburbs:
                # Adding the suburbs to the database, ran once!
                with session.transaction().write() as write_transaction:
                    query = 'insert $x isa suburb, has name "{suburbName}", has versionNumber 1;'.format(
                        suburbName=suburb)
                    insert_iterator = write_transaction.query(query).get()
                    concepts = [ans.get("x") for ans in insert_iterator]
                    # print("Inserted a suburb with ID: {0}".format(concepts[0].id))
                    print("Inserted a suburb with name", suburb)
                    # to persist changes, write transaction must always be committed
                    write_transaction.commit()
                    count += 1

            print("in total there are", count)

            # Add the locations relationship (neighbouring informations)
            count = 0
            data = json.load(json_file1)
            for location in data:
                count += 1
                for direction in data[location]:  # extract just the name of the location and igore other details
                    processed = \
                        data[location][direction].replace('[', '').replace(']', '').replace("'", '').replace(" ",
                                                                                                             '_').split(
                            ',')[0].split('|')
                    location_processed = location.split(',')
                    if "Queensland" not in location_processed[
                        1]:  # or ("Herston" not in processed and "Herston" not in location_processed[0]):  # only get Queensland locations
                        continue
                    try:
                        with session.transaction().write() as write_transaction:
                            query = 'match $x isa suburb, has name "{suburbA}", has versionNumber 1; $y isa suburb, has name "{suburbB}", has versionNumber 1; ' \
                                    'insert $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $relationship has direction "{direct}", has versionNumber 1;'.format(
                                suburbA=location_processed[0], suburbB=processed[0], direct=direction)
                            # input(query)
                            insert_iterator = write_transaction.query(query).get()
                            concepts = [ans.get("x") for ans in insert_iterator]
                            print("Inserted a neighbour with ID: {0}".format(concepts[0].id))
                            print("added", location_processed[0], "with", processed[0], "direction", direction)
                            ## to persist changes, write transaction must always be committed
                            write_transaction.commit()
                    except:
                        print("ERROR")
                        pass

            # The following code is only for demonstration purposes to test out the knowledge graph versioning. Uncomment if only want to see normal Knowledge graph without versioning features
            with session.transaction().write() as write_transaction:
                query = 'insert $x isa version_tracker, has versionNumber 1, has date 2021-01-22;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("Inserted a version_tracker with ID: {0}".format(concepts[0].id))
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'insert $x isa version_tracker, has versionNumber 2, has date 2022-01-22;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("Inserted a version_tracker with ID: {0}".format(concepts[0].id))
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'match $x isa version_tracker, has versionNumber 1; $y isa version_tracker, has versionNumber 2; ' \
                        'insert $relationship (current: $x, next: $y) isa version_update;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("added", "version 1", "with", "version 2")
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'insert $x isa suburb, has name "New_Spring_Hill", has versionNumber 2;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("Inserted a suburb with name", "New_Spring_Hill")
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'match $x isa suburb, has name "Herston", has versionNumber 1; $y isa suburb, has name "New_Spring_Hill", has versionNumber 2; ' \
                        'insert $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $relationship has direction "s", has versionNumber 2;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("added", "New_Spring_Hill", "with", "Herston", "direction", "s")
                write_transaction.commit()

            with session.transaction().write() as write_transaction:
                query = 'match $x isa suburb, has name "Spring_Hill", has versionNumber 1; $y isa suburb, has name "New_Spring_Hill", has versionNumber 2; ' \
                        'insert $relationship (old: $x, new: $y) isa suburb_update;'
                insert_iterator = write_transaction.query(query).get()
                concepts = [ans.get("x") for ans in insert_iterator]
                print("added", "New_Spring_Hill", "with", "Spring_Hill")
                write_transaction.commit()

# Queries to run on Grakn graph

# # show entity with attributes link
# # match $x isa suburb; $x has attribute $a; get;

# # show relationship with attribute direction
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has attribute $m; $y has attribute $p; $emp has attribute $b; get; offset 0; limit 2;
# match $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $x has attribute $name1; $y has attribute $name2; $relationship has attribute $direction; get; offset 0; limit 10;

# # Show specific suburb with all it's neighbours
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $x has attribute $q; $y has attribute $f; $y has attribute $o; $emp has attribute $k; $emp has attribute $b; get; offset 0; limit 30;
# # match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $y has attribute $f; $emp has attribute $k; get; offset 0; limit 30;


# Queries including the version control features - still in development
# Show version control entity - still in development
# # match $emp (current: $x, next: $y) isa version_update; $x has attribute $t; $y has attribute $f; get; offset 0; limit 30;

# Show suburb updates
# # match $emp (old: $x, new: $y) isa suburb_update; $x has attribute $t; $y has attribute $f; get; offset 0; limit 30;

# Show all updates
#  match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $y has attribute $f; get; offset 0; limit 30;

# Get direction South most up to date
# match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $x has name "Herston"; $x has attribute $t; $y has attribute $f; $emp has direction "s"; $emp has attribute $u; get; offset 0; limit 30;
