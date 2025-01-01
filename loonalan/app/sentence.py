from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup
from textual.widgets import Label, Button, ListView, ListItem, DataTable, Collapsible, Static
from textual.reactive import reactive
from textual.color import Color
from textual.message import Message

from ..core import IDTable, Morpheme, Rule


class MorphemeChoose(Label):
    
    class Clicked(Message):
        def __init__(self, index: int):
            self.index = index
            super().__init__()
    
    def __init__(self, index: int, **kwargs):
        self.index = index
        super().__init__(**kwargs)
    
    def on_click(self):
        self.post_message(self.Clicked(index=self.index))

class SentenceEntry(Static):
    
    def __init__(self, s: list[str], **kwargs):
        super().__init__(**kwargs)
        self.blocks = []
        for (index, x) in enumerate(s):
            t = MorphemeChoose(index=index, renderable=x + ' ')
            self.blocks.append(t)
    
    def compose(self) -> ComposeResult:
        yield HorizontalGroup(*self.blocks)

class RuleChoose(Label):
    
    class Clicked(Message):
        def __init__(self, rule: Rule):
            self.rule = rule
            super().__init__()
    
    def compose(self) -> ComposeResult:
        yield Label(self.rule.format())
    
    def __init__(self, rule: Rule, **kwargs):
        self.rule = rule
        super().__init__(**kwargs)
    
    def on_click(self):
        self.post_message(self.Clicked(rule=self.rule))

class RulesAvailable(HorizontalGroup):
    
    def compose(self) -> ComposeResult:
        yield ListView(id='rules_available')
    
    def update(self, m: Morpheme):
        rules = Rule.find(m=m)
        lv = self.query_one(ListView)
        lv.clear()
        for r in rules:
            lv.append(ListItem(RuleChoose(r)))

class ButtonGenerate(Button):
    
    class Clicked(Message):
        def __init__(self):
            super().__init__()
    
    def on_mount(self):
        pass
    
    def on_click(self):
        self.post_message(self.Clicked())

class Sentence(VerticalGroup):
    
    def compose(self) -> ComposeResult:
        yield HorizontalGroup(
            VerticalGroup(
                HorizontalGroup(
                    ButtonGenerate('Generate', id='generate', variant='success'),
                    Button('Build', id='build', variant='error'),
                ),
                ListView(id='list_view_sentences')
            ),
            RulesAvailable(),
        )
    
    def on_morpheme_choose_clicked(self, message: MorphemeChoose.Clicked):
        ra = self.query_one(RulesAvailable)
        index = message.index
        ra.update(m=self.table.last().sequence[index])
        self.last_index = index
    
    def on_rule_choose_clicked(self, message: RuleChoose.Clicked):
        if self.last_index is None:
            return
        lv = self.query_one(ListView)
        rule = message.rule
        self.table.pushdown(rule=rule, id=self.last_index)
        lv.insert(0, [ListItem(SentenceEntry(s=self.table.last().format().split(' ')))])
        self.last_index = None
        
    def on_button_generate_clicked(self, message: ButtonGenerate.Clicked):
        lv = self.query_one(ListView)
        lv.clear()
        self.table = IDTable(Morpheme('Sentence'))
        lv.append(ListItem(SentenceEntry(s=self.table.last().format().split(' '))))
    
    def on_mount(self):
        pass