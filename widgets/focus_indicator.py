# widgets/focus_indicator.py

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from kivy.properties import NumericProperty
from ..constants import (CENTER_MARKER_COLOR, BASELINE_COLOR, 
                        FOCUS_LINE_WIDTH, FOCUS_MARKER_HEIGHT,
                        BASELINE_OFFSET)

class FocusIndicator(Widget):
    """
    Visual indicator showing focus point and baseline for RSVP display.
    
    Features:
    - Vertical lines marking the focus point (above and below text)
    - Horizontal line indicating text baseline
    - All measurements use device-independent pixels
    - Properly scales with window/display changes
    """
    
    line_width = NumericProperty(FOCUS_LINE_WIDTH)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_graphics,
                 size=self.update_graphics)
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Update the indicator graphics, ensuring proper scaling and positioning."""
        self.canvas.clear()
        with self.canvas:
            # Center marker (vertical lines)
            Color(*CENTER_MARKER_COLOR)
            center_x = self.center_x
            
            # Top marker line
            Line(
                points=[
                    center_x, 
                    self.top - FOCUS_MARKER_HEIGHT, 
                    center_x, 
                    self.top
                ],
                width=self.line_width
            )
            
            # Bottom marker line
            Line(
                points=[
                    center_x, 
                    self.y, 
                    center_x, 
                    self.y + FOCUS_MARKER_HEIGHT
                ],
                width=self.line_width
            )
            
            # Baseline indicator with subtle color transition
            # Draw a rectangle with gradient-like effect using multiple lines
            baseline_y = self.y + BASELINE_OFFSET
            line_count = 3
            for i in range(line_count):
                alpha = 1.0 - (i / line_count)
                Color(*BASELINE_COLOR[:3], alpha)
                Line(
                    points=[
                        self.x + dp(20),
                        baseline_y - dp(i),
                        self.right - dp(20),
                        baseline_y - dp(i)
                    ],
                    width=dp(1)
                )