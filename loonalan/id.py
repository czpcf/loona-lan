from typing import Tuple, Union
from collections import defaultdict
from copy import deepcopy

from .inherit import Inherit
from .morpheme import Morpheme
from .property import Property
from .rule import Rule
from .vocab import Vocab

class ID():
    def __init__(self, sequence: list[Morpheme]):
        self.sequence = sequence
    
    def format(self, **kwargs) -> str:
        return ' '.join([s.format(**kwargs) for s in self.sequence])
    
    def __getitem__(self, idx: int) -> Morpheme:
        return self.sequence[idx]
    
    def pushdown(self, rule: Rule, id: int) -> Tuple['ID', list[Inherit]]:
        new_s, inherit = rule.pushdown(morpheme=self.sequence[id])
        new_s = deepcopy(self.sequence[:id] + new_s + self.sequence[id+1:])
        return ID(sequence=new_s), inherit

class InheritEdge():
    def __init__(self, source: int, to: int, property: Property):
        self.source = source
        self.to = to
        self.property = property

class IDTable():
    def __init__(self, morpheme: Morpheme):
        self.ids: list[ID] = [ID(sequence=[morpheme])]
        self.edges: list[InheritEdge] = []
        self.fixed = False
        self.property: dict[int, list[Property]] = defaultdict(list[Property])
        self.union: dict[Tuple[int, int], int] = {(0, 0): 0}
        self.tot_parts = 1
        self.edge_out: dict[Tuple[int, Property], list[int]] = defaultdict(list[int])
    
    def format(self, **kwargs):
        return '\n'.join([i.format(**kwargs) for i in self.ids])
    
    def last(self) -> ID:
        return self.ids[-1]
    
    def pushdown(self, rule: Rule, id: int):
        if self.fixed:
            raise RuntimeError(f"table is fixed")
        layer = self.layers - 1
        new_id, inherit = self.ids[-1].pushdown(rule=rule, id=id)

        for x in range(id):
            self.union[(layer+1, x)] = self.union[(layer, x)]
        for x in range(len(rule.to)):
            self.union[(layer+1, id+x)] = self.tot_parts
            self.tot_parts += 1
        for x in range(id + 1, len(self.last().sequence)):
            self.union[(layer+1, x+len(rule.to)-1)] = self.union[(layer, x)]

        for i in inherit:
            for x in i.source:
                for y in i.to:
                    source = self.union[(layer if x==0 else layer+1, id if x==0 else x-1+id)]
                    to = self.union[(layer if y==0 else layer+1, id if y==0 else y-1+id)]
                    self.edges.append(InheritEdge(source=source, to=to, property=i.property))
                    self.edge_out[(source, i.property)].append(to)
        self.ids.append(new_id)
    
    def backward(self):
        for u in self.topo:
            for p in self.property[u]:
                for v in self.edge_out[(u, p)]:
                    if p not in self.property[v]:
                        self.property[v].append(p)
        layer = self.layers - 1
        for i in range(len(self.last().sequence)):
            x = self.union[(layer, i)]
            for p in self.property[x]:
                if p not in self.ids[-1].sequence[i].properties:
                    self.ids[-1].sequence[i].properties.append(p)
    
    @property
    def layers(self):
        return len(self.ids)
    
    def update(self, vocab: Vocab, pos: int):
        if self.fixed is False:
            raise RuntimeError(f"not fixed")
        if pos < 0 or len(self.words) <= pos:
            raise ValueError(f"pos out of range")
        if self.words[pos] is not None:
            raise RuntimeError(f"pos {pos} is possessed")
        # check whether the vocab has type required
        if self.last()[pos] not in vocab.trans:
            raise ValueError(f"expect vocab to have type {self.last()[pos].type}")
        self.words[pos] = vocab
        for (m, property) in vocab.property.items():
            x = self.union[(self.layers-1, pos)]
            for p in property:
                print("GG", p.type)
                if p not in self.property[x]:
                    self.property[x].append(p)
        self.backward()
    
    def build(self):
        self.fixed = True
        id = self.last()
        self.words: list[Union[None, Vocab]] = [None for _ in range(len(id.sequence))]
        layer = self.layers - 1
        for (i, m) in enumerate(id.sequence):
            for p in m.properties:
                self.property[self.union[(layer, i)]].append(p)
        # build topo
        indeg = defaultdict(int)
        out = defaultdict(list[int])
        for i in range(self.tot_parts):
            indeg[i] = 0
        for e in self.edges:
            indeg[e.to] += 1
            out[e.source].append(e.to)
        topo = []
        Q = []
        for i in range(self.tot_parts):
            if indeg[i] == 0:
                Q.append(i)
        while len(Q) != 0:
            u = Q.pop()
            topo.append(u)
            for v in out[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    Q.append(v)
        self.topo = topo
    
    def instantiate(self, **kwargs) -> str:
        id = self.last()
        res = []
        layer = self.layers - 1
        for (i, word) in enumerate(self.words):
            if word is None:
                res.append(id.sequence[i].format(**kwargs))
            elif isinstance(word, Vocab):
                property = self.property[self.union[(layer, i)]]
                res.append(word.conjugate(morpheme=id.sequence[i], property=property))
        return ' '.join(res)