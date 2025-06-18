#!/usr/bin/env python3
"""
S3Commander - Retro terminal-style file manager for AWS S3 buckets
Inspired by Norton Commander and Midnight Commander
"""

import os
import sys
import json
import curses
import boto3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import logging
from pathlib import Path

# Import local modules
from src.core.s3_client import S3Client
from src.ui.interface import Interface
from src.ui.themes import ThemeManager
from src.utils.config import ConfigManager
from src.utils.logger import setup_logging


class S3Commander:
    """Main S3Commander application class"""
    
    def __init__(self):
        self.config = ConfigManager()
        self.theme_manager = ThemeManager()
        self.s3_client = S3Client()
        self.interface = None
        self.logger = setup_logging()
        
    def initialize(self):
        """Initialize the application"""
        try:
            # Load configuration
            self.config.load_config()
            
            # Initialize S3 client
            self.s3_client.initialize()
            
            # Setup curses interface
            self.interface = Interface(self.s3_client, self.theme_manager)
            
            self.logger.info("S3Commander initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize S3Commander: {e}")
            print(f"Error: {e}")
            sys.exit(1)
    
    def run(self):
        """Run the main application loop"""
        try:
            self.initialize()
            
            # Start the curses interface
            curses.wrapper(self.interface.run)
            
        except KeyboardInterrupt:
            self.logger.info("Application interrupted by user")
            print("\nGoodbye!")
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.interface:
            self.interface.cleanup()
        self.logger.info("S3Commander shutdown complete")


def main():
    """Main entry point"""
    print("S3Commander - Retro S3 File Manager")
    print("Loading...")
    
    app = S3Commander()
    app.run()


if __name__ == "__main__":
    main() 