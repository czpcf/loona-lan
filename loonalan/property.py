from typing import Tuple

from .pallete import Pallete

class Property():
    info: dict[str, Tuple[str, str]] = {}
    abbr: dict[str, str] = {}

    def __init__(self, type: str):
        if type not in self.__class__.info and type not in self.__class__.abbr:
            raise RuntimeError(f"type {type} not found")
        if type not in self.__class__.info:
            type = self.__class__.abbr[type]
        self.type = type
        self.abbr = self.__class__.info[type][0]
        self.color = self.__class__.info[type][1]

    def format(self, **kwargs) -> str:
        use_color: bool = kwargs.get('use_color', True)
        use_abbr: bool = kwargs.get('use_abbr', True)
        s = self.abbr if use_abbr else self.type
        if use_color:
            return Pallete.color(s, self.color)
        return s

    @classmethod
    def parse(cls, s: str) -> list['Property']:
        properties = s.strip().removeprefix('(').removesuffix(')').split('|')
        res = []
        for p in properties:
            res.append(Property(p))
        return res

    @classmethod
    def get_abbr(cls, type: str) -> str:
        if type in cls.abbr:
            return type
        if type not in cls.info:
            raise ValueError(f"type {type} not found")
        return cls.info[type][0]
    
    @classmethod
    def register(cls, type: str, abbreviation: str, color: str):
        if type in cls.info:
            raise RuntimeError(f"type {type} exists")
        if abbreviation in cls.abbr:
            raise RuntimeError(f"abbreviation {abbreviation} exists")
        cls.info[type] = (abbreviation, color)
        cls.abbr[abbreviation] = type