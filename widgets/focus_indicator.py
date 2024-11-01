# widgets/focus_indicator.py

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from kivy.properties import NumericProperty
from constants import (CENTER_MARKER_COLOR, BASELINE_COLOR, FOCUS_LINE_WIDTH, 
                      FOCUS_MARKER_HEIGHT, BASELINE_OFFSET)

class FocusIndicator(Widget):
    """Visual indicator showing focus point and baseline for RSVP display."""
    
    line_width = NumericProperty(FOCUS_LINE_WIDTH)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Update the indicator graphics, ensuring proper scaling and positioning."""
        self.canvas.clear()
        with self.canvas:
            # Center marker (vertical lines)
            Color(*CENTER_MARKER_COLOR)
            center_x = self.center_x
            
            # Top marker line - shorter and closer to text
            Line(
                points=[
                    center_x, 
                    self.center_y + dp(25), 
                    center_x, 
                    self.center_y + dp(5)
                ],
                width=self.line_width
            )
            
            # Bottom marker line - shorter and closer to text
            Line(
                points=[
                    center_x, 
                    self.center_y - dp(5), 
                    center_x, 
                    self.center_y - dp(25)
                ],
                width=self.line_width
            )
            
            # Baseline indicator with subtle color transition
            baseline_y = self.center_y - dp(35)  # Closer to text
            line_count = 3
            for i in range(line_count):
                alpha = 1.0 - (i / line_count)
                Color(*BASELINE_COLOR[:3], alpha)
                Line(
                    points=[
                        self.x + dp(40),  # Added padding on sides
                        baseline_y - dp(i),
                        self.right - dp(40),
                        baseline_y - dp(i)
                    ],
                    width=dp(1)
                )