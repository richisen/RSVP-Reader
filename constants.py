# constants.py

from kivy.metrics import dp

# Required packages and versions
REQUIRED_PACKAGES = [
    ('kivy', '2.3.0'),
    ('freetype-py', None),
    ('uharfbuzz', None),
    ('syllapy', None),
    ('pyphen', None),
    ('bbcode', None)
]

# Window settings
DEFAULT_WINDOW_WIDTH = 800
DEFAULT_WINDOW_HEIGHT = 600

# Font settings
DEFAULT_FONT = 'OpenDyslexic'
DEFAULT_FONT_SIZE = 24
FONT_SIZES = ['16', '20', '24', '28', '32', '36']
FONT_NAMES = ['OpenDyslexic', 'APHont']

# Display settings
DEFAULT_WPM = 300
WPM_VALUES = ['100', '200', '300', '400', '500']
DEFAULT_FOCUS_OFFSET = 0.3  # Focus character position (30% into word)
BASE_WPM = 300  # Base WPM for timecode scaling

# Timing constants
BASE_DURATION_FACTOR = 0.8  # Base duration multiplier
LENGTH_FACTOR = 0.1  # Word length impact on timing
SYLLABLE_FACTOR = 0.1  # Syllable count impact on timing

# File settings
SUPPORTED_EXTENSIONS = ['.txt', '.timecode']
TEST_FILES = [
    'You_Can_Do_That.txt',
    'The_Ultimate_Display.txt',
    'You_Can_Do_That.timecode',
    'The_Ultimate_Display.timecode'
]

# UI Constants
PADDING = dp(10)
SPACING = dp(10)
BUTTON_HEIGHT = dp(44)
DISPLAY_HEIGHT = dp(100)

# Colors
FOCUS_COLOR = 'ff0000'  # Red for focus character
BASELINE_COLOR = (0.7, 0.7, 0.7, 1)  # Gray for baseline
CENTER_MARKER_COLOR = (0.8, 0.8, 0.8, 1)  # Light gray for center marker

# Focus Indicator
FOCUS_LINE_WIDTH = dp(2)
FOCUS_MARKER_HEIGHT = dp(20)
BASELINE_OFFSET = dp(30)