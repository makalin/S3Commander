"""
Theme management for S3Commander UI
"""

import curses

class ThemeManager:
    """Manages color themes for the UI"""
    def __init__(self, theme_name: str = "green_on_black"):
        self.theme_name = theme_name
        self.colors = {}

    def initialize_colors(self):
        # Define color pairs for retro themes
        if self.theme_name == "amber":
            curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Default
            curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)   # Highlight
            curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Status
            curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_YELLOW)  # Amber
            curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Selection
        elif self.theme_name == "dos_blue":
            curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)    # Default
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)   # Highlight
            curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLUE)     # Status
            curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)    # DOS blue
            curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Selection
        else:  # green_on_black
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Default
            curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Highlight
            curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Status
            curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLUE)    # DOS blue
            curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_WHITE)   # Selection
        self.colors = {
            "default": curses.color_pair(1),
            "highlight": curses.color_pair(2),
            "status": curses.color_pair(3),
            "dos_blue": curses.color_pair(4),
            "selected": curses.color_pair(5),
        }

    def get_color(self, name: str):
        return self.colors.get(name, curses.color_pair(1)) 