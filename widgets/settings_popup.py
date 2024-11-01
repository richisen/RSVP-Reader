# widgets/settings_popup.py

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.metrics import dp
from kivy.properties import ObjectProperty

from ..constants import (FONT_NAMES, FONT_SIZES, WPM_VALUES, 
                        PADDING, SPACING, BUTTON_HEIGHT)

class SettingsPopup(Popup):
    """Settings dialog for RSVP reader configuration."""
    
    app = ObjectProperty(None)
    
    def __init__(self, app_instance, **kwargs):
        super().__init__(**kwargs)
        self.app = app_instance
        self.title = 'Settings'
        self.size_hint = (0.8, 0.8)
        self.content = self._create_layout()
    
    def _create_layout(self) -> BoxLayout:
        """Create and return the settings layout."""
        layout = BoxLayout(
            orientation='vertical',
            padding=PADDING,
            spacing=SPACING
        )
        
        # Font selection
        layout.add_widget(self._create_section_label('Font:'))
        self.font_spinner = Spinner(
            text=self.app.font_name,
            values=FONT_NAMES,
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.font_spinner.bind(text=self.on_font_change)
        layout.add_widget(self.font_spinner)
        
        # Font size selection
        layout.add_widget(self._create_section_label('Font Size:'))
        self.size_spinner = Spinner(
            text=str(self.app.font_size),
            values=FONT_SIZES,
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.size_spinner.bind(text=self.on_size_change)
        layout.add_widget(self.size_spinner)
        
        # WPM selection
        layout.add_widget(self._create_section_label('Words Per Minute:'))
        self.wpm_spinner = Spinner(
            text=str(self.app.wpm),
            values=WPM_VALUES,
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        self.wpm_spinner.bind(text=self.on_wpm_change)
        layout.add_widget(self.wpm_spinner)
        
        # Close button
        close_button = Button(
            text='Close',
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            background_normal='',
            background_color=(0.8, 0.8, 0.8, 1)
        )
        close_button.bind(on_press=self.dismiss)
        layout.add_widget(close_button)
        
        return layout
    
    def _create_section_label(self, text: str) -> Label:
        """Create a section label with consistent styling."""
        return Label(
            text=text,
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            text_size=(None, BUTTON_HEIGHT),
            valign='middle'
        )
    
    def on_font_change(self, spinner, text):
        """Handle font selection change."""
        self.app.font_name = text
        self.app.update_display()
    
    def on_size_change(self, spinner, text):
        """Handle font size change."""
        self.app.font_size = int(text)
        self.app.update_display()
    
    def on_wpm_change(self, spinner, text):
        """Handle WPM change."""
        self.app.wpm = int(text)