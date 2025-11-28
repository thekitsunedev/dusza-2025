# Import and connector object
from data.prototypes.connector import Connector

conn = Connector()

### Worlds

# Fetching worlds
worlds: list[str] = conn.fetchWorlds()

# Loading
conn.loadWorld(world_name)
"""
world_name: str # Name of the world.
If left empty it will load the default world.
"""

# Difficulty
difficulty: int = conn.difficulty
"""
0: Difficulty disabled
1 - 10 Difficulty level

Setting difficulty e.g.:
conn.difficulty = 3
"""

### Saves

# Fetching
saves: list[str] = conn.fetchSaves()

# Loading
conn.loadSave(save_name)
"""
Literaly the same as loadWorld,
but it tries to load a save.
If not found it will fall back to:
loadWorld(default)
"""

# Creating (and saving)
conn.createSave(save_name)

# Deleting
conn.deleteSave(save_name)


### Cards


# Fetching
cards: dict = conn.fetchCards(*filters)

"""
Returns with a dictionary object.

Filters (comma separated)
"cards"
"leaders"
"collection"
"deck"

example:
fetchCards("cards") Returns all cards
fetchCards("leaders", "collection") Returns all leaders and collection.
fetchCards() Return everything

Return format

{
    "cards": {
        "card_name": {
            "health": int,
            "damage": int,
            "element": <"Tűz" | "Víz" | "Levegő" | "Föld">
        },
        ...
    },
    "leaders": {
        "card_name": {
            "health": int,
            "damage": int,
            "element": <"Tűz" | "Víz" | "Levegő" | "Föld">
        },
        ...
    },
    "collection": {
        "card_name": {
            "health": int,
            "damage": int,
            "element": <"Tűz" | "Víz" | "Levegő" | "Föld">
        },
        ...
    },
    "deck": {
        "card_name": {
            "health": int,
            "damage": int,
            "element": <"Tűz" | "Víz" | "Levegő" | "Föld">
        },
        ...
    }
}

If only one filter is specified, then it will return all results in the root object.
Example:
fetchCards("cards")
{
    "card_name": {
        "health": int,
        "damage": int,
        "element": <"Tűz" | "Víz" | "Levegő" | "Föld">
    },
    ...
}
"""

# Creating a deck
deck: dict = conn.createDeck(list[str])
"""
If more card names are listed than the maximum allowed,
then only the first N amount of cards are added,
til' the cap is reached.

Returns the same format as fetchCards with one filter.
"""


### Dungeon

# Fetching
dungeons: dict = conn.fetchDungeons()
"""
Return format:
{
    "dungeon_name": {
        "available": bool (Only matters if the dungeon is BIG),
        "reward": <"Életerő" | "Sebzés" | "Kártya">,
        "type": <"Egyszerű" | "Kis" | "Nagy">,
        "cards": {
            "card_name" : {
                ...
            },
            ...
        },
        !! Leader is empty if the dungeon doesn't have a leader !!
        "leader": {
            "health": int,
            "damage": int,
            "element": <"Tűz" | "Víz" | "Levegő" | "Föld">
        }
    }
}

"""


### Fight

# Initialize a match
cards: dict = conn.prepareFight(dungeon_name)
"""
Returns
{
    "deck": {
        ...
    },
    "enemy_deck": {
        ...
    },
    "active_card": card # always empty here
    "active_enemy": card # always empty here
}
"""

# Iterate
status: dict = conn.iterateFight()
"""
Yields the same object as prepareFight,
but active_card and active_enemy contains
the cards currently fighting, and not in line.
"""