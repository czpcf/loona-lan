from collections import defaultdict
from typing import Callable
import yaml

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
    def __init__(self, vocab: str, property: dict[Morpheme, list[Property]], conjugation: dict[Morpheme, Conjugation], description: dict[Morpheme, str]):
        self.vocab = vocab
        self.property = property
        self.trans = conjugation
        self.description = description
    
    def conjugate(self, morpheme: Morpheme, property: list[Property]) -> str:
        if morpheme not in self.property:
            raise ValueError(f"do not have type {morpheme.type}")
        property = [p for p in property if p not in self.property[morpheme]]
        return self.trans[morpheme].apply(s=self.vocab, property=property)

class VocabTable():
    vocabs: dict[str, Vocab] = {}
    
    @classmethod
    def get(cls, vocab: str) -> Vocab:
        if vocab not in cls.vocabs:
            raise ValueError(f"{vocab} not found")
        return cls.vocabs[vocab]
    
    @classmethod
    def add_vocab(cls, vocab: Vocab):
        if vocab.vocab in cls.vocabs:
            raise ValueError(f"{vocab.vocab} already exists")
        cls.vocabs[vocab.vocab] = vocab
    
    @classmethod
    def load(cls, path: str, conjugation: dict[Morpheme, Callable]):
        config = yaml.safe_load(open(path, "r"))
        vocab = config['vocabulary']
        for v in vocab:
            property: dict[Morpheme, list[Property]] = defaultdict(list[Property])
            description: dict[Morpheme, str] = {}
            for m in vocab[v]:
                for p in vocab[v][m]['property']:
                    property[Morpheme(m)].append(Property(type=p))
                description[Morpheme(m)] = vocab[v][m].get('description', '')
            cls.add_vocab(vocab=Vocab(vocab=v, property=property, conjugation=conjugation, description=description))
    
    @classmethod
    def get_table(cls):
        return ','.join([v for v in cls.vocabs])