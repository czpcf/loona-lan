from collections import defaultdict
from typing import Tuple

from .morpheme import Morpheme
from .pallete import Pallete
from .property import Property

class Rule():
    rules: dict[Morpheme, list[list[Morpheme]]] = defaultdict(list[list[Morpheme]])

    def __init__(self, source: Morpheme, to: list[Morpheme]):
        self.source = source
        self.to = to
    
    def format(self, **kwargs) -> str:
        res = self.source.format(**kwargs)
        res += Pallete.color(' -> ', 'none')
        res += ' '.join([x.format(**kwargs) for x in self.to])
        return res

    @classmethod
    def register(cls, rule: str):
        m = rule.strip().split(' ')
        if m[1] != '->':
            raise RuntimeError(f"arrow not found, perhaps you're missing backspaces")
        source = Morpheme.parse(m[0])
        if len(source.properties) != 0:
            raise ValueError(f"source cannot have properties")
        to = []
        for x in m[2:]:
            to.append(Morpheme.parse(x))
        cls.rules[source].append(to)
    
    @classmethod
    def get_rules(cls) -> list['Rule']:
        rules = []
        for s in cls.rules:
            for t in cls.rules[s]:
                rules.append(Rule(source=s, to=t))
        return rules
    
    @classmethod
    def format_rules(cls, **kwargs) -> str:
        rules = cls.get_rules()
        res = '\n'.join([r.format(**kwargs) for r in rules])
        return res