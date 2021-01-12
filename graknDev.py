from grakn.client import GraknClient
# https://docs.grakn.ai/docs/examples/phone-calls-schema
# https://docs.grakn.ai/docs/client-api/python


# https://docs.grakn.ai/docs/general/quickstart
with GraknClient(uri="localhost:48555") as client:
    with client.session(keyspace="locations") as session:
        # pass
        ## Insert a Person using a WRITE transaction
        # with session.transaction().write() as write_transaction:
        #     insert_iterator = write_transaction.query('insert $x isa suburb, has name "suburbD";').get()
        #     concepts = [ans.get("x") for ans in insert_iterator]
        #     print("Inserted a suburb with ID: {0}".format(concepts[0].id))
        #     ## to persist changes, write transaction must always be committed (closed)
        #     write_transaction.commit()

        ## Read the person using a READ only transaction
        with session.transaction().read() as read_transaction:
            answer_iterator = read_transaction.query("match $x isa suburb; get $name; limit 10;").get()

            input("All good?")
            for answer in answer_iterator:
                print(answer)
                person = answer.map().get("x")
                print("Retrieved suburb with id " + person.id)

        ## Or query and consume the iterator immediately collecting all the results
        # with session.transaction().read() as read_transaction:
        #     # pass
        #     answer_iterator = read_transaction.query("match $x isa suburb; get; limit 10;").get()
        #     persons = [ans.get("x") for ans in answer_iterator]
        #     for person in persons:
        #         print("Retrieved person with id "+ person.id)

        ## if not using a `with` statement, then we must always close the session and the read transaction
        # read_transaction.close()
        # session.close()
        # client.close()