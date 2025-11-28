from data.prototypes.connector import Connector

conn = Connector()

conn.loadWorld("test") # The test world specified in the first test case

conn.createDeck(["Corky", "Kira"])

conn.prepareFight("Teszt1a Kazamata")

# iterateFight is a generator!
for status in conn.iterateFight():
    print(status)
    # Do smth