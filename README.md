# Subtitle Synchronizer Documentation

## Overview
The Subtitle Synchronizer is a Python-based GUI application designed to help users synchronize subtitle files (.srt) with video files. It provides an intuitive interface for adjusting subtitle timings while previewing the video. 100% written by AI (using 4o and Perplexity AI).

## Features
- Load video and subtitle files.
- Synchronize subtitles with video playback.
- Save synchronized subtitles to a new file.
- Resume progress from the last session.
    - WIP
- Keyboard shortcuts for quick navigation and synchronization.
    - This could also be better.

## Requirements
- Python 3.6 or higher.
- Required Python libraries: `tkinter`, `vlc`.
- VLC media player installed on your system.

## How to Run

### Windows
1. Install Python from [python.org](https://www.python.org/).
2. Install VLC media player from [videolan.org](https://www.videolan.org/).
3. Install the `python-vlc` library by running:
   ```
   pip install python-vlc
   ```
4. Save the script as `syncer.py`.
5. Run the script using:
   ```
   python syncer.py
   ```

### macOS
1. Install Python from [python.org](https://www.python.org/).
2. Install VLC media player from [videolan.org](https://www.videolan.org/).
3. Install the `python-vlc` library by running:
   ```
   pip install python-vlc
   ```
4. Save the script as `syncer.py`.
5. Run the script using:
   ```
   python3 syncer.py
   ```

### Linux
1. Install Python from your package manager or [python.org](https://www.python.org/).
2. Install VLC media player from your package manager or [videolan.org](https://www.videolan.org/).
3. Install the `python-vlc` library by running:
   ```
   pip3 install python-vlc
   ```
4. Save the script as `syncer.py`.
5. Run the script using:
   ```
   python3 syncer.py
   ```

## Keyboard Shortcuts
- `Space`: Sync the current subtitle.
- `Left Arrow`: Go back to the previous subtitle.
- `Right Arrow`: Load the next subtitle.
- `[` : Jump back 5 seconds.
- `]` : Jump forward 5 seconds.

## Limitations
- The application currently supports only `.srt` subtitle files.
- Requires VLC media player to be installed and properly configured.
- The GUI may not scale well on very high-resolution displays.
- Limited error handling for corrupted subtitle files.
- It should be noted that the code was written with Windows in mind... testing on other operating systems has not been conducted.

## Future Improvements
- Support for additional subtitle formats.
- Enhanced error handling and user feedback.
- Improved GUI scaling for different screen resolutions.
- Resume/progress system is finicky. WIP.
- Making keyboard shortcuts more robust.