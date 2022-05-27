import sqlite3


class ParseQuery:
    """Manage data and communication with the database."""

    def __init__(self):
        """Pull data in from the database and make it as an attribute.

        Class Attributes
        ----------------
        data_pool: list
            A list of all the items from the 2 tables of the database, with
            each item structured as a list.
        ingredient_names: list
            A list of all the NAME values of the data_pool.

        Notes
        -----
            The Class Attributes are purposed to be used as an object attribute
        in any part of the program where the data from the database is needed.
        It is recommended to keep the communication and management of the
        program with the database inside this class, to promote a clean code
        environment and structure.

        Database Structure
        ------------------
        The database has 2 tables:
            INGREDIENTS
            CUSTOM_INGREDIENTS
        With each table consisting of the same 8 columns from left to right:
            NAME
            VALUE
            WEIGHT
            OBTAINED_AT
            PRIMARY_EFFECT
            SECONDARY_EFFECT
            TERTIARY_EFFECT
            QUATERNARY_EFFECT
        """
        # Connection & cursor object for "skyrim_ingredients.db".
        self.con = sqlite3.connect("skyrim_ingredients.db")
        self.cur = self.con.cursor()

        self.index_key = None

        self._pull_data()

    def _pull_data(self):
        """Extension of the constructor.

        Read more details from the "__doc__" of the class' "__init__" method.
        """
        self.data_pool = []
        self.ingredient_names = []

        # TODO: Code currently is not true to docs of "__init__" method.
        # Convert item's data type into string before appending to data_pool.
        for i in self.cur.execute("SELECT * FROM INGREDIENTS"):
            i = list(i)
            for index, item in enumerate(i[:]):
                if type(item) is not str:
                    i.pop(index)
                    i.insert(index, str(item))

            self.data_pool.append(i)
            self.ingredient_names.append(i[0])  # NAME value at index 0.

    def add_ingredient(self, ingredient_entry):
        """Add and commit an ingredient entry.

        Arguement
        ---------
        ingredient_entry: list
            A list that contains the data for the ingredient that will be
            appended to the database.
        """
        pass

    def search_suggestions(self, qeury_text):
        """Returns a list of ingredients name search suggestions."""
        items = []
        qtext = qeury_text.lower().replace(' ', '')

        if qtext:
            for item in self.ingredient_names:
                if qtext in item.lower().replace(' ', ''):
                    items.append(item)

        return items

    def update_idx_key(self, qeury_text):
        """Updates/sets the index key to be used to pull data from data_pool.
        """
        for x, item in enumerate(self.ingredient_names):
            if qeury_text.lower().replace(' ', '') == \
            item.lower().replace(' ', ''):
                self.index_key = x

    def details(self):
        """Returns the item from data_pool.

        Returns an item from data pool with a specific index set before.
        """
        return self.data_pool[self.index_key]

    def effects(self):
        """Returns the list of effects.

        The nested list has the following structure:
        [[Ingredient 1, ..2, ..3, Ingredient N],  # Primary Effect
            [Ingredient 1, ..2, ..3, Ingredient N],  # Secondary Effect
            [Ingredient 1, ..2, ..3, Ingredient N],  # Tertiary Effect
            [Ingredient 1, ..2, ..3, Ingredient N]  # Quaternary Effect
            ]
        """
        primary, secondary, tertiary, quaternary = [], [], [], []

        for x, y in enumerate(self.data_pool):
            for i in y:
                if i == self.data_pool[self.index_key][4]:
                    primary.append(self.data_pool[x][0])
                if i == self.data_pool[self.index_key][5]:
                    secondary.append(self.data_pool[x][0])
                if i == self.data_pool[self.index_key][6]:
                    tertiary.append(self.data_pool[x][0])
                if i == self.data_pool[self.index_key][7]:
                    quaternary.append(self.data_pool[x][0])

        return [primary, secondary, tertiary, quaternary]

    def tabs(self):
        """Returns the list of tab names."""
        primary = self.data_pool[self.index_key][4]
        secondary = self.data_pool[self.index_key][5]
        tertiary = self.data_pool[self.index_key][6]
        quaternary = self.data_pool[self.index_key][7]

        return [primary, secondary, tertiary, quaternary]
