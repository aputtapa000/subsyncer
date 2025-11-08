# Subtitle Synchronizer Documentation

## Overview
The Subtitle Synchronizer is a Python-based GUI application designed to help users synchronize subtitle files (`.srt`, `.ass`, `.sub`) with video files. It provides an intuitive interface for adjusting subtitle timings while previewing the video. 100% written by AI (using 4o and Perplexity AI).

## Features
- Load video and subtitle files.
- Synchronize subtitles with video playback.
- Save synchronized subtitles to a new file.
- Resume progress from the last session.
    - Now fixed!
- Keyboard shortcuts for quick navigation and synchronization.
    - This could also be better.

## Requirements
- Python 3.6 or higher.
- Required Python libraries: `tkinter`, `vlc`.
- VLC media player installed on your system.

## How to Run

<details>
<summary>Windows</summary>

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

</details>

<details>
<summary>macOS</summary>

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

</details>

<details>
<summary>Linux</summary>

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

</details>

## Keyboard Shortcuts
- `Space`: Sync the current subtitle.
- `Left Arrow`: Go back to the previous subtitle.
- `Right Arrow`: Load the next subtitle.
- `[` : Jump back 5 seconds.
- `]` : Jump forward 5 seconds.

## Testing
The program creates a `*_synced.srt` file (example here is with `.srt` though logic applies to `.ass` and `.sub`) so as to not mess with the original srt file. To test playback, you should select the synced srt file either through your video player or by renaming or making a copy of your video file to match the subtitle file's title.

## Limitations
- The application currently supports only `.srt`, `.ass`, and `.sub` subtitle files.
- The application currently supports `.mkv`,`.mp4`, and `.avi` video file formats. There is no limitation to the length of the video files, however.
- The application cannot handle `.mkv` files with subtitles built-in to the container. Consider using something like [this](https://github.com/Darkfall48/MKV-Sub-Extractor) to extract the subtitles from the file if this is the case.
- Requires VLC media player to be installed and properly configured.
- The GUI may not scale well on very high-resolution displays.
- Limited error handling for corrupted subtitle files.
- It should be noted that the code was written with Windows in mind... testing on other operating systems has not been conducted.

## Future Improvements
- ~~Support for additional subtitle formats.~~ `.ass` and `.sub` added (maybe more to come)!
- Enhanced error handling and user feedback.
- Improved GUI scaling for different screen resolutions.
- ~~Resume/progress system is finicky. WIP.~~ Fixed!
- Making keyboard shortcuts more robust.
- ~~Make it easier to jump around the video file.~~ ADDED!(testing in progress)
   - ~~Clicking 'Next' a thousand times isn't fun... maybe a collapsible scrollable list on the side to see all the subtitles and double clicking takes you to that timestamp.~~
- Bring in support for extracting subs from inside matroska containers and then repackage afterwards.