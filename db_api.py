import sqlite3


class Database:
    """Manage data and communication with the database.

    Methods
    -------
    add_ingredient
        Add and commit a custom ingredient entry to the database.
    search_suggestions
        Return a list of search suggestions.
    update_pull_key
        Set the new value of the search_key attribute.
    details
        Return the searched item from the data_pool attribute.
    effects
        Return a list of other ingredients with similar effects.
    tabs
        Return a list of tab names.
    """

    def __init__(self):
        """Pull data in from the database and make it its own attribute.

        Class Attributes
        ----------------
        search_key: string
            The key used to return the correct set of data.
        """
        # Create a connection and cursor to the database.
        self.con = sqlite3.connect("skyrim_ingredients.db")
        self.cur = self.con.cursor()
        self.search_key = None

        self._pull_data()

    def _pull_data(self):
        """Extension of the constructor. Pull data from the database.

        Class Attributes
        ----------------
        data_pool: list
            Contains all the items from the 2 tables of the database, with
            each item structured as a list.
        ingredient_names: list
            Contains all the NAME values of the data_pool attribute.

        Notes
        -----
        The Class Attributes are purposed to be used as an object attribute in
        any part of the program where the data from the database is needed. It
        is recommended to keep the communication and data management of the
        program with the database inside this class, to promote a clean working
        environment and code structure.

        Database Structure

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
        self.data_pool = []
        self.ingredient_names = []

        # Pull data from the INGREDIENTS table of the database.
        for row in self.cur.execute("SELECT * FROM INGREDIENTS"):
            row = list(row)
            for index, item in enumerate(row[:]):
                if type(item) is not str:
                    row.pop(index)
                    row.insert(index, str(item))

            self.data_pool.append(row)
            self.ingredient_names.append(row[0])  # NAME column at index 0.

        # Pull data from the CUSTOM_INGREDIENTS table of the database.
        for row in self.cur.execute("SELECT * FROM CUSTOM_INGREDIENTS"):
            row = list(row)
            for index, item in enumerate(row[:]):
                if type(item) is not str:
                    row.pop(index)
                    row.insert(index, str(item))

            self.data_pool.append(row)
            self.ingredient_names.append(row[0])  # NAME column at index 0.

    def add_ingredient(self, ingredient_entry):
        """Add and commit a custom ingredient entry to the database.

        Arguments
        ---------
        ingredient_entry: list
            Contains the entry values of the "Add Ingredient" panel.

        Notes
        -----
        TODO: Add method notes.
        """
        pass

    def search_suggestions(self, qeury_text):
        """Return a list of search suggestions.

        Arguments
        ---------
        query_text: string
            The text inside the input box of the search bar.

        Notes
        -----
        The list returned contains the possible ingredient names that is
        determined by seeing if an ingredient name contains the characters or
        text of the qeury_text argument. If such characters or text is found in
        the ingredient name, this name will be appended to the list that is
        returned.
        """
        suggestions = []
        qtext = qeury_text.lower().replace(' ', '')

        if qtext:
            for item in self.ingredient_names:
                if qtext in item.lower().replace(' ', ''):
                    suggestions.append(item)

        return suggestions

    def update_pull_key(self, qeury_text):
        """Set the new value of the search_key attribute.

        Arguments
        ---------
        query_text: string
            The current text inside the input box of the search bar.

        Notes
        -----
        The search_key is used in the class' "details", "effects", and "tabs"
        method to set the correct data to be returned when called.
        """
        for x, item in enumerate(self.ingredient_names):
            if qeury_text.lower().replace(' ', '') == \
            item.lower().replace(' ', ''):
                self.search_key = x

    def details(self):
        """Return the searched item from the data_pool attribute.

        Notes
        -----
        The item returned will just be a list from the data_pool attribute with
        its specified index set by the search_key class attribute.
        """
        return self.data_pool[self.search_key]

    def effects(self):
        """Return a list of other ingredients with similar effects.

        Notes
        -----
        For simplicity let us refer to the main ingredient as the ingredient
        searched by the user.

        The list consists of 4 sublists that that are specified as primary,
        secondary, tertiary, and quaternary. All pertaining to the main
        ingredient's 4 effects. Therefor the contents one of these sublist is
        an ingredient name from the database with the same effect found in the
        main ingredient.

        As an example, if the main ingredient is "Chicken's Egg", it's four
        effects from primary to quaternary are: "Resist Magic", "Damage Magicka
        Regen", "Waterbreathing", and "Lingering Damage Stamina".

        Its primary effect is "Resist Magic" so lets say an ingredient is found
        that has "Resist Magic" as their tertiary effect. It doesn't matter if
        the effect of the said ingredeint is at their secondary or tertiary. As
        long as they have the resist magic effect, its ingredient name will be
        appended to the primary sublist. This is because we tied things to the
        effects of the main ingredient, i. e. resist magic is set to be the
        primary sub list because it is the main ingredient's primary effect.
        Therefore all the ingredients with the same effect will be found here.
        All is the same for the secondary, tertiary, and quaternary sublists.
        """
        primary, secondary, tertiary, quaternary = [], [], [], []

        for x, y in enumerate(self.data_pool):
            for i in y:
                if i == self.data_pool[self.search_key][4]:
                    primary.append(self.data_pool[x][0])
                if i == self.data_pool[self.search_key][5]:
                    secondary.append(self.data_pool[x][0])
                if i == self.data_pool[self.search_key][6]:
                    tertiary.append(self.data_pool[x][0])
                if i == self.data_pool[self.search_key][7]:
                    quaternary.append(self.data_pool[x][0])

        return [primary, secondary, tertiary, quaternary]

    def tabs(self):
        """Return a list of tab names.

        Notes
        -----
        The list returned is just the list of the searched ingredient's four
        effects namely: Primary Effect, Secondary Effect, Tertiary Effect, and
        Quaternary Effect accordingly.
        """
        primary = self.data_pool[self.search_key][4]
        secondary = self.data_pool[self.search_key][5]
        tertiary = self.data_pool[self.search_key][6]
        quaternary = self.data_pool[self.search_key][7]

        return [primary, secondary, tertiary, quaternary]
