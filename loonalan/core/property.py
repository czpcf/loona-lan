from typing import Tuple

from .pallete import Pallete

class Property():
    info: dict[str, Tuple[str, str]] = {}
    abbr: dict[str, str] = {}

    @classmethod
    def get_list(cls) -> list['Property']:
        res = []
        for type in cls.info:
            res.append(Property(type=type))
        return res

    def __init__(self, type: str):
        if type not in self.__class__.info and type not in self.__class__.abbr:
            raise RuntimeError(f"type {type} not found")
        if type not in self.__class__.info:
            type = self.__class__.abbr[type]
        self.type = type
        self.abbr = self.__class__.info[type][0]
        self.color = self.__class__.info[type][1]
    
    def __eq__(self, other):
        if isinstance(other, Property):
            return self.type == other.type and self.abbr == other.abbr
        return False

    def __hash__(self):
        return hash((self.type, self.abbr))

    def format(self, **kwargs) -> str:
        use_color: bool = kwargs.get('use_color', True)
        use_abbr: bool = kwargs.get('use_abbr', True)
        s = self.abbr if use_abbr else self.type
        if use_color:
            return Pallete.color(s, self.color)
        return s

    @classmethod
    def parse(cls, s: str) -> Tuple[list['Property'], list[str]]:
        all = s.strip().removeprefix('(').removesuffix(')').split(',')
        properties = all[0].split(',')
        # inherit
        if properties[0].startswith('+') or properties[0].startswith('-'):
            return [], all
        raise ValueError(f"property must start with +(source) or -(to)")

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