from typing import Tuple

from .inherit import Inherit
from .morpheme import Morpheme
from .property import Property
from .rule import Rule

class ID():
    def __init__(self, sequence: list[Morpheme]):
        self.sequence = sequence
    
    def format(self, **kwargs) -> str:
        return ' '.join([s.format(**kwargs) for s in self.sequence])
    
    def pushdown(self, rule: Rule, id: int) -> Tuple['ID', list[Inherit]]:
        new_s, inherit = rule.pushdown(morpheme=self.sequence[id])
        new_s = self.sequence[:id] + new_s + self.sequence[id+1:]
        return ID(sequence=new_s), inherit

class InheritEdge():
    def __init__(self, layer: int, cross: bool, source: int, to: int, property: Property):
        self.layer = layer
        self.cross = cross
        self.source = source
        self.to = to
        self.property = property

class IDTable():
    def __init__(self, morpheme: Morpheme):
        self.ids: list[ID] = [ID(sequence=[morpheme])]
        self.edges: list[InheritEdge] = []
    
    def format(self, **kwargs):
        return '\n'.join([i.format(**kwargs) for i in self.ids])
    
    def last(self) -> ID:
        return self.ids[-1]
    
    def pushdown(self, rule: Rule, id: int):
        layer = len(self.edges) - 1
        new_id, inherit = self.ids[-1].pushdown(rule=rule, id=id)
        for i in inherit:
            cross = i.source==0
            for x in i.to:
                self.edges.append(InheritEdge(layer=layer, cross=cross, source=id, to=x-1+id, property=i.property))
        self.ids.append(new_id)