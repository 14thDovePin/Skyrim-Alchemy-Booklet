import json


class AlchemyQuery:
    """For parsing and processing ingredient search query."""

    def __init__(self):
        # Load json database as 'adata'.
        with open('default_ingredients_database.json', 'r') as f:
            self.adata = json.load(f)

        self._construct_data_pool()
        # Main key for pulling data.
        self.main_key = None

    def _construct_data_pool(self):
        """Constructs the data pool with as the following.
        [
        [name, weight, value, obtained, primary,  # List 1
        secondary, tertiary, quaternary],
        ...
        [name,weight, value, obtained, primary,  # List N
        secondary, tertiary, quaternary],
        ]
        """
        self.data_pool = []

        for x in range((len(self.adata['Ingredient'].keys()))):
            name = self.adata['Ingredient'][str(x)]
            weight = self.adata['Weight'][str(x)]
            value = self.adata['Value'][str(x)]
            obtained = self.adata['Obtained'][str(x)]
            primary = self.adata['Primary Effect'][str(x)]
            secondary = self.adata['Secondary Effect'][str(x)]
            tertiary = self.adata['Tertiary Effect'][str(x)]
            quaternary = self.adata['Quaternary Effect'][str(x)]

            self.data_pool.append(
                [name, str(weight), str(value), obtained, \
                primary, secondary, tertiary, quaternary]
                )

        self.word_pool = [i[0] for i in self.data_pool]

    def search_suggestions(self, qeury_text):
        """Returns possible search suggestions."""
        items = []
        qtext = qeury_text.lower().replace(' ', '')
        if qtext:
            for item in self.word_pool:
                if qtext in item.lower().replace(' ', ''):
                    items.append(item)
        return items

    def search(self, qeury_text):
        """Sets the key to be used to pull data."""
        for x, item in enumerate(self.word_pool):
            if qeury_text.lower().replace(' ', '') == \
            item.lower().replace(' ', ''):
                self.main_key = x

    def details(self):
        """Returns a list with the following structure.
        [Name, Weight, Value, Obtain, Primary Effect,
        Secondary Effect, Tertiary Effect, Quaternary Effect]
        """
        name = self.data_pool[self.main_key][0]
        weight = self.data_pool[self.main_key][1]
        value = self.data_pool[self.main_key][2]
        obtained = self.data_pool[self.main_key][3]
        primary = self.data_pool[self.main_key][4]
        secondary = self.data_pool[self.main_key][5]
        tertiary = self.data_pool[self.main_key][6]
        quaternary = self.data_pool[self.main_key][7]

        return [name, weight, value, obtained, \
        primary, secondary, tertiary, quaternary]

    def effects(self,):
        """Returns a nested list with the following structure.
        [
        [Ingredient 1, ..2, ..3, Ingredient N],  # Primary Effect
        [Ingredient 1, ..2, ..3, Ingredient N],  # Secondary Effect
        [Ingredient 1, ..2, ..3, Ingredient N],  # Tertiary Effect
        [Ingredient 1, ..2, ..3, Ingredient N]  # Quaternary Effect
        ]"""
        primary, secondary, tertiary, quaternary = [], [], [], []

        for x, y in enumerate(self.data_pool):
            for i in y:
                if i == self.data_pool[self.main_key][4]:
                    primary.append(self.data_pool[x][0])
                if i == self.data_pool[self.main_key][5]:
                    secondary.append(self.data_pool[x][0])
                if i == self.data_pool[self.main_key][6]:
                    tertiary.append(self.data_pool[x][0])
                if i == self.data_pool[self.main_key][7]:
                    quaternary.append(self.data_pool[x][0])

        return [primary, secondary, tertiary, quaternary]

    def tabs(self):
        """Returns a list with the following structure.
        [Primary Effect, Secondary Effect, Tertiary Effect, Quaternary Effect]
        """
        primary = self.data_pool[self.main_key][4]
        secondary = self.data_pool[self.main_key][5]
        tertiary = self.data_pool[self.main_key][6]
        quaternary = self.data_pool[self.main_key][7]

        return [primary, secondary, tertiary, quaternary]
