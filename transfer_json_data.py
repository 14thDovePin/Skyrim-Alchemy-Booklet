"""
Convert "default_ingredients_database.json" contents into a query inside the
"skyrim_ingredients.db" file.
DO NOT COMMIT ANYTHING UNTIL JSON DATA HAS BEEN CONVERTED FULL!!!
"""
import json
import sqlite3


# =============================================================================
# Create the database file, a connection object, and a cursor object.
con = sqlite3.connect('skyrim_ingredients.db')
cur = con.cursor()

# Uncomment either of the 2 belolw to recreate either table.
# cur.execute('DROP TABLE INGREDIENTS')
# cur.execute('DROP TABLE CUSTOM_INGREDIENTS')

# Uncomment either one of the 2 lines below to create either of the table.
# cur.execute("""CREATE TABLE INGREDIENTS(
# cur.execute("""CREATE TABLE CUSTOM_INGREDIENTS(
#     NAME TEXT,
#     WEIGHT REAL,
#     VALUE INT,
#     OBTAINED_AT TEXT,
#     PRIMARY_EFFECT TEXT,
#     SECONDARY_EFFECT TEXT,
#     TERTIARY_EFFECT TEXT,
#     QUATERNARY_EFFECT TEXT
#     )
#     """)


# =============================================================================
# # Test add ingredient.
# cur.execute("""INSERT INTO INGREDIENTS
#     VALUES(
#     'Netch Jelly',
#     0.5,
#     20,
#     'Netch',
#     'Paralysis',
#     'Fortify Carry Weight',
#     'Restore Stamina',
#     'Fear'
#     )
#     """)

# # Test print added ingredient.
# for i in cur.execute("""SELECT * FROM INGREDIENTS
#     """):
#     print(i)

# x = cur.execute("""SELECT * FROM INGREDIENTS WHERE NAME == 'Netch'
#     """).fetchone()
# print(x)


# =============================================================================
# Reconstruct json data into database columns as Python lists.

# Load json data as dictionary.
with open('default_ingredients_database.json', 'r') as f:
    json_data = json.load(f)

# Create columns as lists inside a 'columns' list for looping.
name, weight, value, obtained_at, primary_effect, secondary_effect, \
tertiary_effect, quaternary_effect, = [], [], [], [], [], [], [], []
columns = [  # This order is from the json file.
    name,
    primary_effect,
    secondary_effect,
    tertiary_effect,
    quaternary_effect,
    weight,
    value,
    obtained_at
    ]

# Pull dictionary keys.
keys = json_data.keys()

# Store data in their respective columns.
for i, key in enumerate(keys):
    for item in json_data[key].values():
        columns[i].append(item)

# # Check data inside columns.
# for i in columns:
#     print(f'{i}\n\n')


# =============================================================================
# Insert columns data into database table INGREDIENTS.

# for i in range(len(name)):
#     a, b, c, d, e, f, g, h = name[i], weight[i], value[i], obtained_at[i], \
#     primary_effect[i], secondary_effect[i], tertiary_effect[i], \
#     quaternary_effect[i]

#     cur.execute("INSERT INTO INGREDIENTS VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#         (a, b, c, d, e, f, g, h)
#         )

# Check database contents.
data = cur.execute("""SELECT * FROM INGREDIENTS""")
for i, item in enumerate(data):
    print(i, item, '\n')


# =============================================================================
# COMMIT DATABASE
# con.commit()

# Data has been commited!
# When you run this script without changing any comments, it should output all
# the data inside the database!
