from .property import Property

class Inherit():
    def __init__(self, source: list[int], to: list[int], property: Property):
        self.source = source
        self.to = to
        self.property = property