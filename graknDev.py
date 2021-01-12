from grakn.client import GraknClient
# https://docs.grakn.ai/docs/examples/phone-calls-schema
# https://docs.grakn.ai/docs/client-api/python

# query = [
#                 'match',
#                 '  $customer isa person, has phone-number $phone-number;',
#                 '  $company isa company, has name "Telecom";',
#                 '  (customer: $customer, provider: $company) isa contract;',
#                 '  $target isa person, has phone-number "+86 921 547 9004";',
#                 '  (caller: $customer, callee: $target) isa call, has started-at $started-at;',
#                 '  $min-date == 2018-09-14T17:18:49; $started-at > $min-date;',
#                 'get $phone-number;'
#             ]
#
# print("\nQuery:\n", "\n".join(query))
# query = "".join(query)
# input('')

# https://docs.grakn.ai/docs/general/quickstart
with GraknClient(uri="localhost:48555") as client:
    # client.keyspaces().delete('locations')

    with client.session(keyspace="locations") as session:
        # pass
        ## Insert a Person using a WRITE transaction
        # with session.transaction().write() as write_transaction:
        #     insert_iterator = write_transaction.query('insert $x isa suburb, has name "suburbE";').get()
        #     concepts = [ans.get("x") for ans in insert_iterator]
        #     print("Inserted a suburb with ID: {0}".format(concepts[0].id))
        #     ## to persist changes, write transaction must always be committed (closed)
        #     write_transaction.commit()

    #     ## Insert Relation!
        with session.transaction().write() as write_transaction:
            insert_iterator = write_transaction.query('match $x isa suburb, has name "suburbD"; $y isa suburb, has name "suburbE";'
                                                      'insert $relationship (me: $x, neighbourOfMe: $y) isa neighbour; $relationship has direction "west";').get()
            concepts = [ans.get("x") for ans in insert_iterator]
            print("Inserted a suburb with ID: {0}".format(concepts[0].id))
            ## to persist changes, write transaction must always be committed (closed)
            write_transaction.commit()
    #
    #     # Read the person using a READ only transaction
    #     # with session.transaction().read() as read_transaction:
    #     #     answer_iterator = read_transaction.query("match $name isa suburb; get $name; limit 10;").get()
    #     # # match $tra (traveler: $per) isa travel; (located-travel: $tra, travel-location: $loc) isa location-of-travel; $loc has name "French Lick"; $per has full-name $fn; get $fn;
    #     #
    #     #     for answer in answer_iterator:
    #     #         # print(answer)
    #     #         person = answer.map().get("name")
    #     #         # print(answer.map())
    #     #         # print(person)
    #     #         print("Retrieved suburb with id " + person.id)
    #
    #     ## Or query and consume the iterator immediately collecting all the results
    #     # with session.transaction().read() as read_transaction:
    #     #     # pass
    #     #     answer_iterator = read_transaction.query("match $x isa suburb; get; limit 10;").get()
    #     #     persons = [ans.get("x") for ans in answer_iterator]
    #     #     for person in persons:
    #     #         print("Retrieved person with id "+ person.id)
    #
    #     ## if not using a `with` statement, then we must always close the session and the read transaction
    #     # read_transaction.close()
    #     # session.close()
    #     # client.close()


# show entity with attributes link
# match $x isa suburb; $x has attribute $a; get;
# show relationship with attribute direction
# match $emp (me: $x, neighbourOfMe: $y) isa neighbour; $emp has attribute $b; get; offset 0; limit 30;