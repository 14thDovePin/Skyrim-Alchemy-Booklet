import sqlite3


class ParseQuery:
    """Manages talking with the SQLite3 database."""

    def __init__(self):
        """Creates a connection to the database and pulls in data."""
        # Connection & cursor object for "skyrim_ingredients.db".
        self.con = sqlite3.connect("skyrim_ingredients.db")
        self.cur = self.con.cursor()

        self.index_key = None

        self._pull_data()

    def _pull_data(self):
        """Pulls data in from the database.

        Data is stored in 2 class variables:
        data_pool:
            Contains all the values of each row inside "INGREDIENTS" table from 
            "skyrim_ingredients.db", with each row structured as a list.
        word_pool:
            Contains all the NAME value of each row inside "INGREDIENTS" table.
        """
        self.data_pool = []
        self.word_pool = []

        # Convert item's data type into string before appending to data_pool.
        for i in self.cur.execute("SELECT * FROM INGREDIENTS"):
            i = list(i)
            for index, item in enumerate(i[:]):
                if type(item) is not str:
                    i.pop(index)
                    i.insert(index, str(item))

            self.data_pool.append(i)
            self.word_pool.append(i[0])  # NAME value at index 0.

    def search_suggestions(self, qeury_text):
        """Returns a list of ingredients name search suggestions."""
        items = []
        qtext = qeury_text.lower().replace(' ', '')

        if qtext:
            for item in self.word_pool:
                if qtext in item.lower().replace(' ', ''):
                    items.append(item)

        return items

    def update_idx_key(self, qeury_text):
        """Updates/sets the index key to be used to pull data from data_pool.
        """
        for x, item in enumerate(self.word_pool):
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
