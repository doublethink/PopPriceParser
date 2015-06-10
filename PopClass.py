class Pop():

    def __init__(self, category, name, number, value, is_variant, url):
        self.category = category
        self.name = name
        self.number = number
        self.value = value
        self.is_variant = is_variant
        self.url = url

    def __str__(self):
        return "{0}, {2}, {1}, {3}, {4}".format(self.category, self.name, self.number,  self.value, self.is_variant)
