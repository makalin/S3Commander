"""
Main UI interface for S3Commander using curses
"""

import curses
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime

from src.core.s3_client import S3Client
from src.ui.themes import ThemeManager
from src.ui.pane import Pane
from src.ui.status_bar import StatusBar
from src.ui.command_bar import CommandBar


class Interface:
    """Main interface class for S3Commander"""
    
    def __init__(self, s3_client: S3Client, theme_manager: ThemeManager):
        self.s3_client = s3_client
        self.theme_manager = theme_manager
        self.logger = logging.getLogger(__name__)
        
        # UI components
        self.screen = None
        self.left_pane = None
        self.right_pane = None
        self.status_bar = None
        self.command_bar = None
        
        # State
        self.active_pane = 0  # 0 = left, 1 = right
        self.current_buckets = ["", ""]  # [left_bucket, right_bucket]
        self.current_prefixes = ["", ""]  # [left_prefix, right_prefix]
        self.selected_objects = [[], []]  # [left_selections, right_selections]
        
    def run(self, screen):
        """Main interface loop"""
        self.screen = screen
        self.setup_curses()
        self.initialize_ui()
        
        try:
            self.main_loop()
        finally:
            self.cleanup()
    
    def setup_curses(self):
        """Setup curses environment"""
        curses.start_color()
        curses.use_default_colors()
        curses.curs_set(0)  # Hide cursor
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        
        # Initialize colors
        self.theme_manager.initialize_colors()
    
    def initialize_ui(self):
        """Initialize UI components"""
        height, width = self.screen.getmaxyx()
        
        # Calculate pane dimensions
        pane_width = (width - 3) // 2  # Leave space for separator
        pane_height = height - 4  # Leave space for status and command bars
        
        # Create panes
        self.left_pane = Pane(
            self.screen,
            0, 0,  # y, x
            pane_height, pane_width,
            self.theme_manager,
            "Left"
        )
        
        self.right_pane = Pane(
            self.screen,
            0, pane_width + 3,  # y, x (with separator)
            pane_height, pane_width,
            self.theme_manager,
            "Right"
        )
        
        # Create status and command bars
        self.status_bar = StatusBar(
            self.screen,
            pane_height, 0,
            width,
            self.theme_manager
        )
        
        self.command_bar = CommandBar(
            self.screen,
            pane_height + 1, 0,
            width,
            self.theme_manager
        )
        
        # Load initial data
        self.load_buckets()
        self.refresh_panes()
    
    def load_buckets(self):
        """Load available buckets"""
        try:
            buckets = self.s3_client.list_buckets()
            self.left_pane.set_buckets(buckets)
            self.right_pane.set_buckets(buckets)
        except Exception as e:
            self.logger.error(f"Failed to load buckets: {e}")
            self.status_bar.set_message(f"Error loading buckets: {e}")
    
    def refresh_panes(self):
        """Refresh both panes"""
        self.refresh_pane(0)  # Left pane
        self.refresh_pane(1)  # Right pane
        self.update_status()
    
    def refresh_pane(self, pane_index: int):
        """Refresh a specific pane"""
        try:
            pane = self.left_pane if pane_index == 0 else self.right_pane
            bucket = self.current_buckets[pane_index]
            prefix = self.current_prefixes[pane_index]
            
            if bucket:
                objects = self.s3_client.list_objects(bucket, prefix)
                pane.set_objects(objects)
            else:
                buckets = self.s3_client.list_buckets()
                pane.set_buckets(buckets)
                
        except Exception as e:
            self.logger.error(f"Failed to refresh pane {pane_index}: {e}")
            self.status_bar.set_message(f"Error refreshing pane: {e}")
    
    def update_status(self):
        """Update status bar with current information"""
        left_info = f"Left: {self.current_buckets[0]}/{self.current_prefixes[0]}"
        right_info = f"Right: {self.current_buckets[1]}/{self.current_prefixes[1]}"
        
        status_text = f"{left_info} | {right_info}"
        self.status_bar.set_message(status_text)
    
    def main_loop(self):
        """Main event loop"""
        while True:
            # Draw everything
            self.draw()
            
            # Get user input
            key = self.screen.getch()
            
            # Handle input
            if not self.handle_input(key):
                break
    
    def handle_input(self, key: int) -> bool:
        """Handle user input"""
        try:
            if key == ord('q') or key == 27:  # q or ESC
                return False
            elif key == ord('\t'):  # Tab
                self.switch_pane()
            elif key == curses.KEY_UP:
                self.move_cursor(-1)
            elif key == curses.KEY_DOWN:
                self.move_cursor(1)
            elif key == ord('\n'):  # Enter
                self.enter_object()
            elif key == ord(' '):  # Space
                self.toggle_selection()
            elif key == ord('F3'):
                self.view_object()
            elif key == ord('F5'):
                self.copy_objects()
            elif key == ord('F6'):
                self.move_objects()
            elif key == ord('F8'):
                self.delete_objects()
            elif key == ord('F7'):
                self.create_folder()
            elif key == ord('F2'):
                self.rename_object()
            elif key == ord('F4'):
                self.edit_object()
            elif key == ord('F9'):
                self.show_menu()
            elif key == ord('F10'):
                self.show_help()
            elif key == ord('\\'):
                self.change_directory()
            elif key == ord('*'):
                self.select_all()
            elif key == ord('+'):
                self.select_pattern()
            elif key == ord('-'):
                self.deselect_all()
            elif key == ord('F1'):
                self.show_help()
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error handling input: {e}")
            self.status_bar.set_message(f"Error: {e}")
            return True
    
    def switch_pane(self):
        """Switch between left and right panes"""
        self.active_pane = 1 - self.active_pane  # Toggle between 0 and 1
        self.update_cursor_visibility()
    
    def move_cursor(self, direction: int):
        """Move cursor in active pane"""
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        pane.move_cursor(direction)
    
    def enter_object(self):
        """Enter/select current object"""
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        current_item = pane.get_current_item()
        
        if not current_item:
            return
        
        if current_item['type'] == 'bucket':
            # Enter bucket
            self.current_buckets[self.active_pane] = current_item['name']
            self.current_prefixes[self.active_pane] = ""
            self.refresh_pane(self.active_pane)
        elif current_item['type'] == 'folder':
            # Enter folder
            self.current_prefixes[self.active_pane] = current_item['key']
            self.refresh_pane(self.active_pane)
        else:
            # View file
            self.view_object()
    
    def toggle_selection(self):
        """Toggle selection of current object"""
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        current_item = pane.get_current_item()
        
        if not current_item:
            return
        
        selections = self.selected_objects[self.active_pane]
        item_key = current_item.get('key', current_item['name'])
        
        if item_key in selections:
            selections.remove(item_key)
        else:
            selections.append(item_key)
        
        pane.update_selections(selections)
    
    def view_object(self):
        """View current object content"""
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        current_item = pane.get_current_item()
        
        if not current_item or current_item['type'] != 'file':
            return
        
        try:
            content = self.s3_client.get_object_content(
                self.current_buckets[self.active_pane],
                current_item['key']
            )
            
            # Show content in a popup (simplified)
            self.show_popup("Object Content", content[:1000] + "..." if len(content) > 1000 else content)
            
        except Exception as e:
            self.status_bar.set_message(f"Error viewing object: {e}")
    
    def copy_objects(self):
        """Copy selected objects to other pane"""
        source_pane = self.active_pane
        dest_pane = 1 - source_pane
        
        selections = self.selected_objects[source_pane]
        if not selections:
            self.status_bar.set_message("No objects selected for copy")
            return
        
        try:
            for item_key in selections:
                source_bucket = self.current_buckets[source_pane]
                dest_bucket = self.current_buckets[dest_pane]
                dest_prefix = self.current_prefixes[dest_pane]
                
                # Determine destination key
                if dest_prefix:
                    dest_key = f"{dest_prefix}/{item_key.split('/')[-1]}"
                else:
                    dest_key = item_key.split('/')[-1]
                
                self.s3_client.copy_object(source_bucket, item_key, dest_bucket, dest_key)
            
            self.status_bar.set_message(f"Copied {len(selections)} object(s)")
            self.refresh_panes()
            
        except Exception as e:
            self.status_bar.set_message(f"Error copying objects: {e}")
    
    def move_objects(self):
        """Move selected objects to other pane"""
        # Similar to copy but delete source after copy
        self.copy_objects()
        # TODO: Implement delete after copy
    
    def delete_objects(self):
        """Delete selected objects"""
        selections = self.selected_objects[self.active_pane]
        if not selections:
            self.status_bar.set_message("No objects selected for deletion")
            return
        
        # Show confirmation
        if not self.show_confirm(f"Delete {len(selections)} object(s)?"):
            return
        
        try:
            bucket = self.current_buckets[self.active_pane]
            for item_key in selections:
                self.s3_client.delete_object(bucket, item_key)
            
            self.status_bar.set_message(f"Deleted {len(selections)} object(s)")
            self.selected_objects[self.active_pane].clear()
            self.refresh_pane(self.active_pane)
            
        except Exception as e:
            self.status_bar.set_message(f"Error deleting objects: {e}")
    
    def create_folder(self):
        """Create a new folder"""
        folder_name = self.command_bar.get_input("Enter folder name: ")
        if not folder_name:
            return
        
        try:
            bucket = self.current_buckets[self.active_pane]
            prefix = self.current_prefixes[self.active_pane]
            
            if prefix:
                folder_key = f"{prefix}/{folder_name}/"
            else:
                folder_key = f"{folder_name}/"
            
            # Create empty object to represent folder
            self.s3_client.s3_client.put_object(
                Bucket=bucket,
                Key=folder_key,
                Body=""
            )
            
            self.status_bar.set_message(f"Created folder: {folder_name}")
            self.refresh_pane(self.active_pane)
            
        except Exception as e:
            self.status_bar.set_message(f"Error creating folder: {e}")
    
    def rename_object(self):
        """Rename current object"""
        current_item = (self.left_pane if self.active_pane == 0 else self.right_pane).get_current_item()
        if not current_item:
            return
        
        new_name = self.command_bar.get_input(f"Rename '{current_item['name']}' to: ")
        if not new_name:
            return
        
        # TODO: Implement rename (copy + delete)
        self.status_bar.set_message("Rename not implemented yet")
    
    def edit_object(self):
        """Edit current object"""
        self.status_bar.set_message("Edit not implemented yet")
    
    def show_menu(self):
        """Show main menu with new options, including batch operations and theme switching"""
        menu_items = [
            "1. Upload file",
            "2. Download file",
            "3. Create bucket",
            "4. Delete bucket",
            "5. Rename object",
            "6. Move object",
            "7. Search objects",
            "8. Batch copy selected",
            "9. Batch move selected",
            "10. Batch delete selected",
            "11. Settings",
            "12. Help",
            "0. Exit"
        ]
        self.show_popup("Menu", "\n".join(menu_items))
        choice = self.command_bar.get_input("Menu option (number): ")
        if choice == "1":
            self.upload_file()
        elif choice == "2":
            self.download_file()
        elif choice == "3":
            self.create_bucket()
        elif choice == "4":
            self.delete_bucket()
        elif choice == "5":
            self.rename_object()
        elif choice == "6":
            self.move_object()
        elif choice == "7":
            self.search_objects()
        elif choice == "8":
            self.batch_copy_selected()
        elif choice == "9":
            self.batch_move_selected()
        elif choice == "10":
            self.batch_delete_selected()
        elif choice == "11":
            self.show_settings()
        elif choice == "12":
            self.show_help()
        elif choice == "0":
            return

    def upload_file(self):
        """Upload a local file to the current bucket/prefix"""
        bucket = self.current_buckets[self.active_pane]
        prefix = self.current_prefixes[self.active_pane]
        local_path = self.command_bar.get_input("Local file to upload: ")
        if not local_path or not bucket:
            self.status_bar.set_message("No file or bucket selected")
            return
        key = self.command_bar.get_input("S3 key (or leave blank for filename): ")
        if not key:
            key = (prefix + "/" if prefix else "") + local_path.split("/")[-1]
        else:
            key = (prefix + "/" if prefix else "") + key
        try:
            self.s3_client.upload_object(local_path, bucket, key)
            self.status_bar.set_message(f"Uploaded {local_path} to {bucket}/{key}")
            self.refresh_pane(self.active_pane)
        except Exception as e:
            self.status_bar.set_message(f"Upload failed: {e}")

    def download_file(self):
        """Download a file from S3 to local filesystem"""
        bucket = self.current_buckets[self.active_pane]
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        current_item = pane.get_current_item()
        if not current_item or current_item['type'] != 'file':
            self.status_bar.set_message("No file selected")
            return
        local_path = self.command_bar.get_input("Local path to save: ")
        try:
            self.s3_client.download_object(bucket, current_item['key'], local_path)
            self.status_bar.set_message(f"Downloaded to {local_path}")
        except Exception as e:
            self.status_bar.set_message(f"Download failed: {e}")

    def create_bucket(self):
        """Create a new S3 bucket"""
        bucket_name = self.command_bar.get_input("New bucket name: ")
        region = self.command_bar.get_input("Region (blank=default): ")
        try:
            self.s3_client.create_bucket(bucket_name, region or None)
            self.status_bar.set_message(f"Created bucket {bucket_name}")
            self.load_buckets()
        except Exception as e:
            self.status_bar.set_message(f"Create bucket failed: {e}")

    def delete_bucket(self):
        """Delete an S3 bucket"""
        bucket_name = self.command_bar.get_input("Bucket to delete: ")
        try:
            self.s3_client.delete_bucket(bucket_name)
            self.status_bar.set_message(f"Deleted bucket {bucket_name}")
            self.load_buckets()
        except Exception as e:
            self.status_bar.set_message(f"Delete bucket failed: {e}")

    def rename_object(self):
        """Rename an object in the current bucket"""
        bucket = self.current_buckets[self.active_pane]
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        current_item = pane.get_current_item()
        if not current_item or current_item['type'] != 'file':
            self.status_bar.set_message("No file selected")
            return
        new_name = self.command_bar.get_input(f"Rename '{current_item['name']}' to: ")
        if not new_name:
            return
        prefix = self.current_prefixes[self.active_pane]
        new_key = (prefix + "/" if prefix else "") + new_name
        try:
            self.s3_client.rename_object(bucket, current_item['key'], new_key)
            self.status_bar.set_message(f"Renamed to {new_key}")
            self.refresh_pane(self.active_pane)
        except Exception as e:
            self.status_bar.set_message(f"Rename failed: {e}")

    def move_object(self):
        """Move an object to another bucket or prefix"""
        bucket = self.current_buckets[self.active_pane]
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        current_item = pane.get_current_item()
        if not current_item or current_item['type'] != 'file':
            self.status_bar.set_message("No file selected")
            return
        dest_bucket = self.command_bar.get_input("Destination bucket: ")
        dest_prefix = self.command_bar.get_input("Destination prefix (blank=none): ")
        dest_key = (dest_prefix + "/" if dest_prefix else "") + current_item['name']
        try:
            self.s3_client.move_object(bucket, current_item['key'], dest_bucket, dest_key)
            self.status_bar.set_message(f"Moved to {dest_bucket}/{dest_key}")
            self.refresh_pane(self.active_pane)
        except Exception as e:
            self.status_bar.set_message(f"Move failed: {e}")

    def search_objects(self):
        """Search for objects by name in the current bucket/prefix"""
        bucket = self.current_buckets[self.active_pane]
        prefix = self.current_prefixes[self.active_pane]
        term = self.command_bar.get_input("Search term: ")
        try:
            results = self.s3_client.search_objects(bucket, term, prefix)
            pane = self.left_pane if self.active_pane == 0 else self.right_pane
            pane.set_objects(results)
            self.status_bar.set_message(f"Found {len(results)} objects")
        except Exception as e:
            self.status_bar.set_message(f"Search failed: {e}")

    def show_help(self):
        """Show help information"""
        help_text = """
S3Commander - Retro S3 File Manager

Navigation:
  Arrow Keys    - Move cursor
  Tab           - Switch panes
  Enter         - Enter folder/bucket or view file
  Space         - Toggle selection
  \\             - Change directory

Operations:
  F3            - View file content
  F5            - Copy selected objects
  F6            - Move selected objects
  F7            - Create folder
  F8            - Delete selected objects
  F2            - Rename object
  F4            - Edit object

Selection:
  *             - Select all
  +             - Select by pattern
  -             - Deselect all

Other:
  F1            - Help
  F9            - Menu
  F10           - Help
  q/ESC         - Exit
        """
        
        self.show_popup("Help", help_text)
    
    def change_directory(self):
        """Change to a specific directory"""
        path = self.command_bar.get_input("Enter path: ")
        if not path:
            return
        
        # TODO: Implement path navigation
        self.status_bar.set_message("Path navigation not implemented yet")
    
    def select_all(self):
        """Select all objects in current pane"""
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        objects = pane.get_all_objects()
        
        selections = []
        for obj in objects:
            selections.append(obj.get('key', obj['name']))
        
        self.selected_objects[self.active_pane] = selections
        pane.update_selections(selections)
    
    def select_pattern(self):
        """Select objects by pattern"""
        pattern = self.command_bar.get_input("Enter pattern: ")
        if not pattern:
            return
        
        # TODO: Implement pattern selection
        self.status_bar.set_message("Pattern selection not implemented yet")
    
    def deselect_all(self):
        """Deselect all objects"""
        self.selected_objects[self.active_pane].clear()
        pane = self.left_pane if self.active_pane == 0 else self.right_pane
        pane.update_selections([])
    
    def show_popup(self, title: str, content: str):
        """Show a popup with content"""
        # Simplified popup - just show in status bar
        self.status_bar.set_message(f"{title}: {content[:50]}...")
    
    def show_confirm(self, message: str) -> bool:
        """Show confirmation dialog"""
        # Simplified confirmation - just return True for now
        return True
    
    def update_cursor_visibility(self):
        """Update cursor visibility based on active pane"""
        self.left_pane.set_active(self.active_pane == 0)
        self.right_pane.set_active(self.active_pane == 1)
    
    def draw(self):
        """Draw the entire interface"""
        self.screen.clear()
        
        # Draw panes
        self.left_pane.draw()
        self.right_pane.draw()
        
        # Draw separator
        height, width = self.screen.getmaxyx()
        for y in range(height - 4):
            self.screen.addstr(y, (width - 3) // 2, " | ")
        
        # Draw status and command bars
        self.status_bar.draw()
        self.command_bar.draw()
        
        self.screen.refresh()
    
    def cleanup(self):
        """Cleanup curses environment"""
        if self.screen:
            curses.nocbreak()
            self.screen.keypad(False)
            curses.echo()
            curses.endwin() 