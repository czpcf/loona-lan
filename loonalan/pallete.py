import regex as re

class Pallete:
    """ ANSI color codes """
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    END = "\033[0m"
    
    color_map = {
        'black': BLACK,
        'red': RED,
        'green': GREEN,
        'brown': BROWN,
        'blue': BLUE,
        'purple': PURPLE,
        'cyan': CYAN,
        'light_gray': LIGHT_GRAY,
        'dark_gray': DARK_GRAY,
        'light_red': LIGHT_RED,
        'light_green': LIGHT_GREEN,
        'yellow': YELLOW,
        'light_blue': LIGHT_BLUE,
        'light_purple': LIGHT_PURPLE,
        'light_cyan': LIGHT_CYAN,
        'white': LIGHT_WHITE,
        'light_white': LIGHT_WHITE,
        'none': END,
    }
    
    # cancel SGR codes if we don't write to a terminal
    if not __import__("sys").stdout.isatty():
        for _ in dir():
            if isinstance(_, str) and _[0] != "_":
                locals()[_] = ""
    else:
        # set Windows console in VT mode
        if __import__("platform").system() == "Windows":
            kernel32 = __import__("ctypes").windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            del kernel32

    @classmethod
    def color(cls, s: str, color: str) -> str:
        c = cls.color_map.get(color.lower(), cls.END)
        return f"{c}{s}{cls.END}"
    
    @classmethod
    def remove_color(cls, s: str) -> str:
        # Regex to match ANSI escape sequences
        ansi_escape = re.compile(r'\033\[[0-9;]*[a-zA-Z]')
        return ansi_escape.sub('', s)