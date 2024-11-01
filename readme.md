# RSVP Reader Implementation

A Rapid Serial Visual Presentation (RSVP) text reader that supports both regular text files and time-coded transcripts.

## Requirements

- Python 3.10.x
- Kivy 2.3.0
- freetype-py
- uharfbuzz
- syllapy
- pyphen
- bbcode

## Features

- Full support for both .txt and .timecode files
- Device-independent pixel scaling
- Proper font measurements using provided metrics
- Focus character highlighting with Spritz-style positioning
- Baseline and center point indication
- Adjustable reading speed with WPM scaling
- Two accessibility-focused fonts supported:
  - OpenDyslexic: Enhanced readability for readers with dyslexia
  - APHont: Optimized for low vision readers

## Installation

1. Ensure Python 3.10.x is installed
2. Install required packages:
```bash
pip install kivy==2.3.0 freetype-py uharfbuzz syllapy pyphen bbcode
```

## Usage

```bash
python main.py
```

## Implementation Notes

- The focus character selection algorithm follows Spritz's approach:
  - Places focus character towards beginning of word
  - Considers syllable structure
  - Optimizes for comprehension
- Word timing is calculated using:
  - Word length
  - Syllable count
  - Timecode information (when available)
- Device-independent rendering using Kivy's dp() function
- Font measurements use freetype-py and uharfbuzz via provided metrics

## Not Implemented/Known Issues

None - all required features are implemented according to specification.

## Build Requirements

- Python 3.10.x
- Kivy 2.3.0
- All additional packages listed in requirements
- Font files must be available in fonts/ directory:
  - OpenDyslexic-Regular.otf
  - APHont-Regular.ttf