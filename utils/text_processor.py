# utils/text_processor.py

import syllapy
import pyphen
from typing import Tuple, Optional
from constants import (BASE_DURATION_FACTOR, LENGTH_FACTOR, 
                        SYLLABLE_FACTOR, DEFAULT_FOCUS_OFFSET, BASE_WPM, FOCUS_COLOR)

class TextProcessor:
    def __init__(self):
        """Initialize text processor with hyphenation dictionary."""
        self.dic = pyphen.Pyphen(lang='en')
    
    def calculate_focus_character(self, word: str) -> int:
        """
        Determine optimal focus character position using Spritz-like algorithm.
        
        Following Spritz's approach:
        - For short words (1-3 chars), use first character
        - For medium words (4-8 chars), use ~30% position
        - For longer words, use position based on syllable structure
        - Prefer beginning of word for better comprehension
        
        Args:
            word: The word to process
        
        Returns:
            Integer index of the focus character
        """
        word_length = len(word)
        
        # Handle very short words
        if word_length <= 3:
            return 0
            
        try:
            # Get syllable structure
            syllables = self.dic.inserted(word).split('-')
            
            if len(syllables) <= 1:
                # No syllable breaks, use position-based approach
                return min(int(word_length * DEFAULT_FOCUS_OFFSET), word_length - 1)
            else:
                # Use first character of second syllable if it exists
                first_syl_len = len(syllables[0])
                # But don't go too far into the word
                max_pos = min(word_length - 1, int(word_length * 0.4))
                return min(first_syl_len, max_pos)
            
        except Exception:
            # Fallback to simple position-based approach
            return min(int(word_length * DEFAULT_FOCUS_OFFSET), word_length - 1)
    
    def calculate_display_duration(self, word: str, base_wpm: int,
                                 timecode_duration: Optional[float] = None) -> float:
        """
        Calculate how long to display a word.
        
        For timecoded content:
            - Uses the provided duration scaled by WPM ratio
        For regular text:
            - Base duration from WPM
            - Subtle adjustments for word length and complexity
            - Maintains readability while keeping flow smooth
        
        Args:
            word: The word to time
            base_wpm: Target words per minute
            timecode_duration: Optional duration from timecode file
        
        Returns:
            Float duration in seconds
        """
        if timecode_duration is not None:
            # Scale timecoded duration based on WPM
            return timecode_duration * (BASE_WPM / base_wpm)
        
        # Calculate base duration from WPM
        base_duration = 60.0 / base_wpm
        
        # Get word complexity factors
        syllable_count = syllapy.count(word)
        length_factor = min(len(word) / 5.0, 2.0)  # Cap length impact
        syllable_factor = min(syllable_count / 2.0, 2.0)  # Cap syllable impact
        
        # Combine factors with subtle adjustments
        # Base duration makes up 80%, length and syllables each affect up to 10%
        duration = (base_duration * 
                   (BASE_DURATION_FACTOR +
                    (LENGTH_FACTOR * length_factor) +
                    (SYLLABLE_FACTOR * syllable_factor)))
        
        return duration
    
    def format_word_with_focus(self, word: str, focus_pos: int,
                             metrics: Optional['TextMetrics'] = None,
                             texture_size: Optional[Tuple[int, int]] = None) -> str:
        """
        Format word with colored focus character and proper alignment.
        
        Args:
            word: The word to format
            focus_pos: Position of focus character
            metrics: Optional TextMetrics instance for measurement
            texture_size: Optional texture size for scaling
        
        Returns:
            Marked up text string ready for display
        """
        # If we have metrics, use them to properly align the word
        if metrics and texture_size:
            glyph_attribs, ascender, descender = metrics.get_text_extents(
                word, texture_size)
            
            # Use measurements to ensure focus character is centered
            # This part is handled by the widget's positioning
            pass
        
        # Format with colored focus character
        return (
            f"{word[:focus_pos]}"
            f"[color={FOCUS_COLOR}]{word[focus_pos]}"
            f"[/color]{word[focus_pos + 1:]}"
        )