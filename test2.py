from data.prototypes.connector import Connector

conn = Connector()


idk = Connector().fetchWorlds()
conn.loadWorld("")
cards: dict = conn.fetchCards("collection")


for i in cards:
    a = cards[i]
    print(f"{i} health = {a['health']} damage = {a['damage']} element = {a['element']}")
