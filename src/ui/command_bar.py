"""
Command bar for S3Commander UI
"""

class CommandBar:
    def __init__(self, screen, y, x, width, theme_manager):
        self.screen = screen
        self.y = y
        self.x = x
        self.width = width
        self.theme_manager = theme_manager
        self.prompt = ""

    def get_input(self, prompt: str) -> str:
        self.prompt = prompt
        self.draw()
        curses.echo()
        input_str = self.screen.getstr(self.y, self.x + len(prompt) + 1, self.width - len(prompt) - 2).decode('utf-8')
        curses.noecho()
        self.prompt = ""
        return input_str

    def draw(self):
        bar = (self.prompt + " ").ljust(self.width-1)
        self.screen.addstr(self.y, self.x, bar, self.theme_manager.get_color("default")) 