from collections import defaultdict
from copy import deepcopy
from typing import Tuple
import math

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
    
    @classmethod
    def find(cls, m: Morpheme) -> list['Rule']:
        found = []
        for rule in cls.rules:
            if m.type == rule.source.type:
                found.append(rule)
        return found
    
    def pushdown(self, morpheme: Morpheme) -> Tuple[list[Morpheme], list[Inherit]]:
        if morpheme.type != self.source.type:
            raise RuntimeError(f"type do not match, expect {self.source.type}")
        return deepcopy(self.to), deepcopy(self.inherit)
    
    def format(self, **kwargs) -> str:
        show_inherit = kwargs.get('show_inherit', True)
        inherit_source = defaultdict(list[Property])
        inherit_to = defaultdict(list[Property])
        if show_inherit:
            for i in self.inherit:
                for x in i.source:
                    inherit_source[x].append(i.property)
                for to in i.to:
                    inherit_to[to].append(i.property)
        res = self.source.format(**kwargs, inherit_source=inherit_source[0], inherit_to=inherit_to[0])
        res += Pallete.color(' -> ', 'none')
        res += ' '.join([x.format(**kwargs, inherit_source=inherit_source[id+1], inherit_to=inherit_to[id+1]) for (id, x) in enumerate(self.to)])
        return res

    @classmethod
    def parse(cls, rule: str):
        m = rule.strip().split(' ')
        inherit_source = defaultdict(list[int])
        inherit_to = defaultdict(list[int])
        
        def push(p: list[str], id: int):
            for x in p:
                if x.startswith('+'):
                    y = Property(x[1:])
                    inherit_source[y].append(id)
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
            if len(inherit_to[p]) > 1 and len(inherit_source[p]) > 1:
                raise ValueError(f"there should be either one source or one end")
            for x in inherit_to[p]:
                if x in inherit_source[p]:
                    raise ValueError(f"loop found")
                p_to.append(x)
            inherit.append(Inherit(source=inherit_source[p], to=p_to, property=p))
        return Rule(source=source, to=to, inherit=inherit)

    @classmethod
    def register(cls, rule: str):
        cls.rules.append(cls.parse(rule=rule))
    
    @classmethod
    def get_rules(cls) -> list['Rule']:
        return cls.rules
    
    @classmethod
    def format_rules(cls, **kwargs) -> str:
        use_index = kwargs.get('use_index', False)
        
        rules = cls.rules
        max_len = int(math.log10(len(rules) - 1))   # start from 0
        a = []
        for (i, r) in enumerate(rules):
            s = r.format(**kwargs)
            if use_index:
                bias = max_len - int(math.log10(max(1, i)))
                s = ' '*bias + str(i) + ": " + s
            a.append(s)
        res = '\n'.join(a)
        return res