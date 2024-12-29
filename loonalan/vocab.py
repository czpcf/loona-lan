from typing import Callable

from .morpheme import Morpheme
from .property import Property

class Conjugation():
    def __init__(self, conjugation: dict[Property, Callable[[str], str]], arange_order: Callable[[list[Property]], list[Property]]):
        self.trans = conjugation
        self.arange = arange_order
    
    def apply(self, s: str, property: list[Property]):
        property = self.arange(property)
        for p in property:
            if p in self.trans:
                s = self.trans[p](s)
        return s

class Vocab():
    def __init__(self, vocab: str, property: list[Property], conjugation: dict[Morpheme, Conjugation]):
        self.vocab = vocab
        self.property = property
        self.trans = conjugation
    
    def conjugate(self, morpheme: Morpheme, property: list[Property]) -> str:
        property = [p for p in property if p not in self.property]
        return self.trans[morpheme].apply(s=self.vocab, property=property)