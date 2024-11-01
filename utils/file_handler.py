# utils/file_handler.py

from typing import List, Tuple, Optional
from pathlib import Path
import os
from timecoded_transcript import parse_timecoded_text
from ..constants import SUPPORTED_EXTENSIONS

class Word:
    """Represents a word with optional timing information."""
    def __init__(self, text: str, start_time: Optional[float] = None, 
                 end_time: Optional[float] = None):
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time if start_time is not None \
                       and end_time is not None else None

class FileHandler:
    @staticmethod
    def load_file(filepath: str) -> List[Word]:
        """
        Load and parse a text or timecode file.
        
        Args:
            filepath: Path to the file to load
        
        Returns:
            List of Word objects containing text and timing information
        
        Raises:
            ValueError: If file extension is not supported
            FileNotFoundError: If file doesn't exist
            RuntimeError: If file parsing fails
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
            
        if path.suffix not in SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type. Supported types: {', '.join(SUPPORTED_EXTENSIONS)}"
            )
        
        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
            
            if path.suffix == '.timecode':
                return FileHandler._parse_timecode_file(content)
            return FileHandler._parse_text_file(content)
            
        except UnicodeDecodeError:
            raise RuntimeError("File must be UTF-8 encoded text")
        except Exception as e:
            raise RuntimeError(f"Error parsing file: {str(e)}")
    
    @staticmethod
    def _parse_timecode_file(content: str) -> List[Word]:
        """
        Parse a timecoded transcript file.
        
        Args:
            content: Raw file content
            
        Returns:
            List of Word objects with timing information
        """
        try:
            parsed_data = parse_timecoded_text(content)
            return [Word(word, start_time, end_time) 
                    for word, start_time, end_time in parsed_data]
        except Exception as e:
            raise RuntimeError(f"Failed to parse timecode file: {str(e)}")
    
    @staticmethod
    def _parse_text_file(content: str) -> List[Word]:
        """
        Parse a regular text file.
        
        Args:
            content: Raw file content
            
        Returns:
            List of Word objects
        """
        return [Word(word.strip()) for word in content.split() 
                if word.strip()]

    @staticmethod
    def verify_file_access(filepath: str) -> None:
        """
        Verify file exists and is readable.
        
        Args:
            filepath: Path to file to verify
            
        Raises:
            FileNotFoundError: If file doesn't exist
            PermissionError: If file isn't readable
        """
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
        if not path.is_file():
            raise ValueError(f"Not a file: {filepath}")
        if not os.access(filepath, os.R_OK):
            raise PermissionError(f"File not readable: {filepath}")