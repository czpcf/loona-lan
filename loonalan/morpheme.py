from typing import Tuple

from .pallete import Pallete
from .property import Property

class Morpheme():
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
        self.properties: list[Property] = []

    def format(self, **kwargs) -> str:
        use_color: bool = kwargs.get('use_color', True)
        show_property: bool = kwargs.get('show_property', True)
        use_abbr: bool = kwargs.get('use_abbr', True)
        c = self.color if use_color else 'none'
        s = self.abbr if use_abbr else self.type
        res = Pallete.color(s, c)
        if show_property and len(self.properties) != 0:
            res += (
                Pallete.color('(', 'none') +
                '|'.join([p.format(use_color=use_color, use_abbr=use_abbr) for p in self.properties]) +
                Pallete.color(')', 'none')
            )
        return res

    @classmethod
    def parse(cls, s: str) -> 'Morpheme':
        s = s.strip()
        first_p = s.find('(')
        if first_p != -1:
            m = Morpheme(s[:first_p])
            m.properties = Property.parse(s[first_p+1:-1])
        else:
            m = Morpheme(s)
        return m
    
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