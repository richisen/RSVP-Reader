# widgets/reader_widget.py

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty
from kivy_text_metrics import TextMetrics

from utils.text_processor import TextProcessor
from utils.file_handler import FileHandler, Word
from widgets.focus_indicator import FocusIndicator
from widgets.settings_popup import SettingsPopup
from constants import (SUPPORTED_EXTENSIONS, PADDING, SPACING, BUTTON_HEIGHT,
                    DISPLAY_HEIGHT)

class RSVPReader(FloatLayout):
    """
    Main RSVP Reader widget that handles text display and playback.
    """
    
    current_word = StringProperty('')
    is_playing = BooleanProperty(False)
    app = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text_processor = TextProcessor()
        self.words = []
        self.current_index = 0
        self.scheduled_event = None
        self.metrics = None
        self.setup_ui()
        self.bind(size=self._on_size)
    
    def _on_size(self, *args):
        """Handle window resize events."""
        self.update_display()
    
    def setup_ui(self):
        """Initialize and layout the UI components."""
        # Main container
        self.main_layout = BoxLayout(
            orientation='vertical',
            padding=PADDING,
            spacing=SPACING,
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        # Controls
        controls = BoxLayout(
            size_hint_y=None,
            height=BUTTON_HEIGHT,
            spacing=SPACING
        )
        
        # Settings button
        self.settings_button = Button(
            text='⚙',
            size_hint_x=None,
            width=BUTTON_HEIGHT,
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        
        # File selection button
        self.file_button = Button(
            text='Select File',
            size_hint_x=None,
            width=dp(100),
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        
        # Play/Pause button
        self.play_button = Button(
            text='Play',
            size_hint_x=None,
            width=dp(100),
            disabled=True,
            background_normal='',
            background_color=(0.9, 0.9, 0.9, 1)
        )
        
        controls.add_widget(self.settings_button)
        controls.add_widget(self.file_button)
        controls.add_widget(self.play_button)
        
        # Display area
        self.display_area = BoxLayout(
            orientation='vertical',
            spacing=dp(2)
        )
        
        # Create a relative layout for precise word positioning
        self.word_container = RelativeLayout(
            size_hint=(1, None),
            height=DISPLAY_HEIGHT
        )
        
        # Word display with improved initial centering
        self.word_display = Label(
            text='Select a file to begin',
            markup=True,
            size_hint=(None, None),
            height=DISPLAY_HEIGHT,
            font_size=dp(24),
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.word_container.add_widget(self.word_display)
        
        # Focus indicator with adjusted position
        self.focus_indicator = FocusIndicator(
            size_hint=(1, None),
            height=DISPLAY_HEIGHT,
            pos_hint={'center_x': 0.5, 'center_y': 0.5}
        )
        
        self.display_area.add_widget(self.word_container)
        self.display_area.add_widget(self.focus_indicator)
        
        # Add everything to main layout
        self.main_layout.add_widget(controls)
        self.main_layout.add_widget(self.display_area)
        
        # Add main layout to root
        self.add_widget(self.main_layout)
        
        # Bind events
        self.settings_button.bind(on_press=self.show_settings)
        self.file_button.bind(on_press=self.show_file_chooser)
        self.play_button.bind(on_press=self.toggle_playback)
    
    def show_settings(self, instance):
        """Display the settings dialog."""
        settings_popup = SettingsPopup(self.app)
        settings_popup.open()
    
    def show_file_chooser(self, instance):
        """Show file selection dialog."""
        content = BoxLayout(orientation='vertical')
        
        file_chooser = FileChooserListView(
            path='.',
            filters=self._get_file_filters()
        )
        
        def select_file(instance, filename, touch=None):
            if filename:
                self.load_file(filename[0])
                popup.dismiss()
        
        file_chooser.bind(on_submit=select_file)
        content.add_widget(file_chooser)
        
        popup = Popup(
            title='Select File',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def _get_file_filters(self):
        """Get file filters based on supported extensions."""
        return ['*' + ext for ext in SUPPORTED_EXTENSIONS]
    
    def load_file(self, filepath):
        """Load and prepare file for display."""
        try:
            FileHandler.verify_file_access(filepath)
            self.words = FileHandler.load_file(filepath)
            self.current_index = 0
            self.play_button.disabled = False
            self.update_display()
        except Exception as e:
            self.show_error_popup(str(e))
    
    def show_error_popup(self, message):
        """Display error message to user."""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()
    
    def toggle_playback(self, instance):
        """Toggle between play and pause states."""
        if not self.is_playing:
            self.start_playback()
        else:
            self.pause_playback()
    
    def start_playback(self):
        """Start or resume playback."""
        self.is_playing = True
        self.play_button.text = 'Pause'
        self.schedule_next_word()
    
    def pause_playback(self):
        """Pause playback."""
        self.is_playing = False
        self.play_button.text = 'Play'
        if self.scheduled_event:
            self.scheduled_event.cancel()
            self.scheduled_event = None
    
    def schedule_next_word(self):
        """Schedule the display of the next word."""
        if self.current_index >= len(self.words):
            self.current_index = 0
            self.pause_playback()
            return
        
        word = self.words[self.current_index]
        self.update_display()
        
        duration = self.text_processor.calculate_display_duration(
            word.text,
            self.app.wpm,
            word.duration if hasattr(word, 'duration') else None
        )
        
        self.scheduled_event = Clock.schedule_once(
            lambda dt: self.advance_word(),
            duration
        )
    
    def advance_word(self):
        """Advance to the next word if still playing."""
        if self.is_playing:
            self.current_index += 1
            self.schedule_next_word()
    
    def update_display(self):
        """Update the display with the current word."""
        if not self.words:
            self.word_display.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
            return
            
        self.word_display.pos_hint = {}
        word = self.words[self.current_index]
        
        try:
            font_path = self.app.get_font_path(self.app.font_name)
            font_size = int(self.app.font_size)
            self.metrics = TextMetrics(font_path, font_size)
            self.focus_indicator.update_font_size(font_size)
        except Exception as e:
            print(f"Error creating TextMetrics: {e}")
            self.metrics = None
        
        focus_pos = self.text_processor.calculate_focus_character(word.text)
        formatted_word = self.text_processor.format_word_with_focus(
            word.text, focus_pos, self.metrics,
            self.word_display.texture_size if self.word_display.texture else None
        )
        
        self.word_display.text = formatted_word
        self.word_display.texture_update()
        
        if self.metrics and self.word_display.texture:
            glyph_attribs, ascender, descender = self.metrics.get_text_extents(
                word.text, self.word_display.texture_size
            )
            
            # Calculate focus width including half of focus character
            focus_width = sum(attrib[6] for attrib in glyph_attribs[:focus_pos])
            if focus_pos < len(glyph_attribs):
                focus_width += glyph_attribs[focus_pos][6] / 2
            
            self.word_display.width = self.word_display.texture_size[0]
            
            # Calculate x position relative to container width for consistent centering
            self.word_display.x = self.word_container.width / 2 - focus_width
            
            # Position vertically
            self.word_display.y = self.word_container.height / 2 - self.word_display.height / 2