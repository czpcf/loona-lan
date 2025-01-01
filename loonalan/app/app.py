from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll
from textual.widgets import Label, Footer, Header

from .rule_table import RuleTable
from .sentence import Sentence

from ..core import Pallete

class LoonaApp(App):

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield RuleTable()
        yield Sentence()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = (
            "textual-dark" if self.theme == "textual-light" else "textual-light"
        )

def run():
    '''
    Launch app.
    '''
    Pallete.disable()
    app = LoonaApp()
    app.run()