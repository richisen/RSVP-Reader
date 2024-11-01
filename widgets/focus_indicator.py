# widgets/focus_indicator.py

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line
from kivy.metrics import dp
from kivy.properties import NumericProperty

class FocusIndicator(Widget):
    """Visual indicator showing focus point and baseline for RSVP display."""
    
    line_width = NumericProperty(dp(2))
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._font_size = dp(24)
        self.bind(pos=self.update_graphics, 
                 size=self.update_graphics)
        self.update_graphics()
    
    def update_font_size(self, font_size):
        """Update indicator sizes based on font size."""
        self._font_size = dp(font_size)
        self.update_graphics()
    
    def update_graphics(self, *args):
        """Update the indicator graphics, ensuring proper scaling and positioning."""
        self.canvas.clear()
        with self.canvas:
            # Center marker
            Color(0.8, 0.8, 0.8, 1)  # Light gray
            center_x = self.center_x
            marker_height = self._font_size * 0.25
            spacing = dp(1)
            
            # Top marker line
            Line(points=[center_x, self.center_y + marker_height,
                       center_x, self.center_y + spacing],
                width=self.line_width)
            
            # Bottom marker line
            Line(points=[center_x, self.center_y - spacing,
                       center_x, self.center_y - marker_height],
                width=self.line_width)
            
            # Simple white baseline
            Color(1, 1, 1, 1)  # White
            baseline_y = self.center_y - self._font_size * 0.3
            Line(points=[self.x + dp(10), baseline_y,
                       self.right - dp(10), baseline_y],
                width=dp(1))