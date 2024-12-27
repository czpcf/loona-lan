from collections import defaultdict
from typing import Tuple

from .inherit import Inherit
from .morpheme import Morpheme
from .pallete import Pallete
from .property import Property

class Rule():
    rules: list['Rule'] = []

    def __init__(self, source: Morpheme, to: list[Morpheme], inherit: list[Inherit]):
        self.source = source
        self.to = to
        self.inherit = inherit
    
    def format(self, **kwargs) -> str:
        show_inherit = kwargs.get('show_inherit', True)
        inherit_source = defaultdict(list[Property])
        inherit_to = defaultdict(list[Property])
        if show_inherit:
            for i in self.inherit:
                inherit_source[i.source].append(i.property)
                for to in i.to:
                    inherit_to[to].append(i.property)
        res = self.source.format(**kwargs, inherit_source=inherit_source[0], inherit_to=inherit_to[0])
        res += Pallete.color(' -> ', 'none')
        res += ' '.join([x.format(**kwargs, inherit_source=inherit_source[id+1], inherit_to=inherit_to[id+1]) for (id, x) in enumerate(self.to)])
        return res

    @classmethod
    def register(cls, rule: str):
        m = rule.strip().split(' ')
        inherit_source = {}
        inherit_to = defaultdict(list[int])
        
        def push(p: list[str], id: int):
            for x in p:
                if x.startswith('+'):
                    y = Property(x[1:])
                    if inherit_source.get(y) is not None:
                        raise RuntimeError(f"multipe inherit source {y.type}({y.abbr}) found")
                    inherit_source[y] = id
                elif x.startswith('-'):
                    y = Property(x[1:])
                    inherit_to[y].append(id)
                else:
                    raise ValueError(f"not source nor to, perhaps you should put properties in front of inheritance")
        
        if m[1] != '->':
            raise RuntimeError(f"arrow not found, perhaps you're missing backspaces")
        source, p = Morpheme.parse(m[0])
        push(p, 0)
        if len(source.properties) != 0:
            raise ValueError(f"source cannot have properties")
        to = []
        for (id, x) in enumerate(m[2:]):
            g, p = Morpheme.parse(x)
            to.append(g)
            push(p, id + 1)
        
        inherit = []
        for p in inherit_source:
            p_to = []
            for x in inherit_to[p]:
                p_to.append(x)
            inherit.append(Inherit(source=inherit_source[p], to=p_to, property=p))
        cls.rules.append(Rule(source=source, to=to, inherit=inherit))
    
    @classmethod
    def get_rules(cls) -> list['Rule']:
        return cls.rules
    
    @classmethod
    def format_rules(cls, **kwargs) -> str:
        rules = cls.rules
        res = '\n'.join([r.format(**kwargs) for r in rules])
        return res