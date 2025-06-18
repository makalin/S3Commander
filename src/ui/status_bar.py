"""
Status bar for S3Commander UI
"""

class StatusBar:
    def __init__(self, screen, y, x, width, theme_manager):
        self.screen = screen
        self.y = y
        self.x = x
        self.width = width
        self.theme_manager = theme_manager
        self.message = ""

    def set_message(self, message: str):
        self.message = message

    def draw(self):
        msg = self.message[:self.width-1].ljust(self.width-1)
        self.screen.addstr(self.y, self.x, msg, self.theme_manager.get_color("status")) 