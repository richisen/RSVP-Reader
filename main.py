# main.py

import sys
if sys.version_info[:2] != (3, 10):
    raise RuntimeError("This application requires Python 3.10.x")

# Import and configure kivy_config_helper BEFORE any other Kivy imports
from kivy_config_helper import config_kivy
# Initial setup before any other Kivy imports
window_width, window_height = config_kivy(
    window_width=800,
    window_height=600,
    simulate_device=False  # Must be off in submitted code
)

try:
    from kivy import require
    require('2.3.0')  # Ensure Kivy 2.3.0
except:
    raise RuntimeError("This application requires Kivy 2.3.0")

import os
from pathlib import Path
import bbcode  # Required for Kivy text markup
from kivy.clock import Clock
from kivy.app import App
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.config import Config
from kivy.resources import resource_add_path

from widgets.reader_widget import RSVPReader
from constants import (DEFAULT_FONT, DEFAULT_FONT_SIZE, DEFAULT_WPM, 
                      REQUIRED_PACKAGES)

class RSVPApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._verify_requirements()
        
        # Initialize settings
        self.font_name = DEFAULT_FONT
        self.font_size = DEFAULT_FONT_SIZE
        self.wpm = DEFAULT_WPM
        
        # Store font paths
        self.font_paths = {}

        # Register fonts
        self._register_fonts()
        

        
    def _verify_requirements(self):
        """Verify all required packages are installed."""
        missing = []
        for package, version in REQUIRED_PACKAGES:
            try:
                module = __import__(package)
                if version and not self._check_version(module.__version__, version):
                    missing.append(f"{package}>={version}")
            except ImportError:
                missing.append(package)
        
        if missing:
            raise RuntimeError(
                f"Missing required packages: {', '.join(missing)}. "
                "Please install all requirements."
            )
    
    def _check_version(self, current, required):
        """Compare version strings."""
        current_parts = [int(x) for x in current.split('.')]
        required_parts = [int(x) for x in required.split('.')]
        return current_parts >= required_parts
    
    def _register_fonts(self):
        """Register custom fonts with Kivy."""
        try:
            # Check both local and system-wide font locations
            font_paths = [
                os.path.join(os.path.dirname(__file__), 'fonts'),
                '/usr/local/share/fonts',
                os.path.expanduser('~/.fonts')
            ]
            
            opendyslexic_found = aphont_found = False
            
            for font_path in font_paths:
                resource_add_path(font_path)
                
                # Check for OpenDyslexic
                if not opendyslexic_found:
                    dyslexic_path = os.path.join(font_path, 'OpenDyslexic-Regular.otf')
                    if os.path.exists(dyslexic_path):
                        LabelBase.register('OpenDyslexic', dyslexic_path)
                        self.font_paths['OpenDyslexic'] = dyslexic_path
                        opendyslexic_found = True
                
                # Check for APHont
                if not aphont_found:
                    aphont_path = os.path.join(font_path, 'APHont-Regular.ttf')
                    if os.path.exists(aphont_path):
                        LabelBase.register('APHont', aphont_path)
                        self.font_paths['APHont'] = aphont_path
                        aphont_found = True
            
            if not (opendyslexic_found and aphont_found):
                raise RuntimeError("Required fonts not found. Please ensure OpenDyslexic and APHont fonts are in the fonts directory.")
                
        except Exception as e:
            raise RuntimeError(f"Error registering fonts: {str(e)}")
    
    def get_font_path(self, font_name):
        """Get the full path for a given font name."""
        return self.font_paths.get(font_name)
    
    def build(self):
        reader = RSVPReader()
        reader.app = self
        Clock.schedule_once(lambda dt: self.update_display(), 0)
        return reader
    
    def update_display(self):
        """Update the display when settings change."""
        if hasattr(self, 'root'):
            self.root.word_display.font_name = self.font_name
            self.root.word_display.font_size = dp(self.font_size)

if __name__ == '__main__':
    RSVPApp().run()