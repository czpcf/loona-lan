from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, VerticalGroup
from textual.widgets import Label, Footer, Header, ListView, ListItem, DataTable, Collapsible
from textual.reactive import reactive
from textual.color import Color

from ..core import Rule, Pallete

class RuleTable(VerticalGroup):
    
    def __init__(self):
        super().__init__()
    
    def compose(self):
        with Collapsible(title="rules", collapsed=True):
            yield DataTable()
    
    def on_mount(self):
        datatable = self.query_one(DataTable)
        datatable.add_columns('source', 'to', 'description')
        self.rules = Rule.get_rules()
        for r in self.rules:
            res = r.format().split('->')
            datatable.add_row(res[0].strip(), res[1].strip())