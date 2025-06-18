"""
Pane for displaying S3 objects or buckets
"""

from typing import List, Dict, Any

class Pane:
    def __init__(self, screen, y, x, height, width, theme_manager, title):
        self.screen = screen
        self.y = y
        self.x = x
        self.height = height
        self.width = width
        self.theme_manager = theme_manager
        self.title = title
        self.items: List[Dict[str, Any]] = []
        self.cursor = 0
        self.selections = set()
        self.active = False

    def set_buckets(self, buckets: List[Dict[str, Any]]):
        self.items = buckets
        self.cursor = 0

    def set_objects(self, objects: List[Dict[str, Any]]):
        self.items = objects
        self.cursor = 0

    def set_active(self, active: bool):
        self.active = active

    def move_cursor(self, direction: int):
        if not self.items:
            return
        self.cursor = max(0, min(self.cursor + direction, len(self.items) - 1))

    def get_current_item(self):
        if not self.items:
            return None
        return self.items[self.cursor]

    def get_all_objects(self):
        return self.items

    def update_selections(self, selections):
        self.selections = set(selections)

    def draw(self):
        # Draw border and title
        for i in range(self.height):
            self.screen.addstr(self.y + i, self.x, " ", self.theme_manager.get_color("default"))
        self.screen.addstr(self.y, self.x + 2, f"[{self.title}]", self.theme_manager.get_color("status"))
        # Draw items
        for idx, item in enumerate(self.items[:self.height-2]):
            attr = self.theme_manager.get_color("default")
            if idx == self.cursor and self.active:
                attr = self.theme_manager.get_color("highlight")
            elif item.get('key', item.get('name')) in self.selections:
                attr = self.theme_manager.get_color("selected")
            display = item.get('name', '')
            self.screen.addstr(self.y + 1 + idx, self.x + 2, display[:self.width-4], attr) 