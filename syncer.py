# Import necessary libraries
import tkinter as tk
from tkinter import ttk
from datetime import timedelta
import os
import sys
import vlc

# Main class for subtitle synchronization
class SubtitleSyncer:
    def __init__(self, master, video_path=None, srt_path=None):
        # If no paths are provided, prompt the user to select files
        if not video_path or not srt_path:
            video_path, srt_path = self.prompt_file_selection()

        # Validate video and subtitle file paths
        if not os.path.isfile(video_path):
            print(f"Error: Video file '{video_path}' not found.")
            sys.exit(1)
        if not os.path.isfile(srt_path):
            print(f"Error: Subtitle file '{srt_path}' not found.")
            sys.exit(1)

        # Initialize variables and parse subtitle file
        self.master = master
        self.video_path = video_path
        self.srt_path = srt_path
        self.subs = self.parse_srt()
        self.current_sub = 0
        self.is_paused = False

        # Check for existing synced file
        self.synced_path = os.path.splitext(self.srt_path)[0] + '_synced.srt'
        self.resume_point = 0
        if os.path.exists(self.synced_path):
            self.prompt_resume()

        # Set up the GUI
        self.setup_gui()

        # Load the first subtitle
        self.load_next_subtitle()

    def prompt_file_selection(self):
        from tkinter import filedialog

        # Prompt user to select video file
        video_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4;*.avi;*.mkv"), ("All Files", "*.*")]
        )
        if not video_path:
            print("Error: No video file selected.")
            sys.exit(1)

        # Prompt user to select subtitle file
        srt_path = filedialog.askopenfilename(
            title="Select Subtitle File",
            filetypes=[("Subtitle Files", "*.srt"), ("All Files", "*.*")]
        )
        if not srt_path:
            print("Error: No subtitle file selected.")
            sys.exit(1)

        return video_path, srt_path

    # Parse the subtitle file into a structured format
    def parse_srt(self):
        subs = []
        try:
            with open(self.srt_path, 'r', encoding='utf-8') as f:
                lines = f.read().split('\n\n')
                for block in lines:
                    parts = block.strip().split('\n')
                    if len(parts) >= 3:
                        timecode = parts[1].split(' --> ')
                        subs.append({
                            'start': self.time_to_ms(timecode[0]),
                            'end': self.time_to_ms(timecode[1]),
                            'text': '\n'.join(parts[2:])
                        })
        except Exception as e:
            print(f"Error reading subtitle file: {e}")
            sys.exit(1)
        return subs

    # Convert time string to milliseconds
    def time_to_ms(self, time_str):
        try:
            h, m, s = time_str.split(':')
            s, ms = s.split(',')
            return int(timedelta(
                hours=int(h),
                minutes=int(m),
                seconds=int(s),
                milliseconds=int(ms)
            ).total_seconds() * 1000)
        except ValueError:
            print(f"Error parsing time string: {time_str}")
            sys.exit(1)

    # Convert milliseconds to time string
    def ms_to_time(self, ms):
        return str(timedelta(milliseconds=ms))[:-3].replace('.', ',')

    # Update the GUI to display video frames
    def update_video_frame(self):
        # Periodically update the current playback time in the control panel
        current_time = self.vlc_player.get_time()
        if (current_time >= 0):
            self.time_label.config(text=f"Current Time: {self.ms_to_time(current_time)}")

        # Schedule the next update
        self.master.after(500, self.update_video_frame)

    # Set up the graphical user interface
    def setup_gui(self):
        # Configure the main window layout
        self.master.geometry("800x600")  # Set a default window size
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=3)  # Give more space to the video frame
        self.master.columnconfigure(1, weight=1)  # Allocate space for the control panel

        # Create video frame
        self.video_frame = ttk.Frame(self.master)
        self.video_frame.grid(row=0, column=0, sticky="nsew")  # Use grid layout

        # Add a label to display video frames
        self.video_label = tk.Label(self.video_frame)
        self.video_label.pack(fill=tk.BOTH, expand=True)

        # Create control panel
        self.control_frame = ttk.Frame(self.master)
        self.control_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Display subtitle text
        self.sub_text = tk.StringVar()
        self.sub_label = ttk.Label(
            self.control_frame, 
            textvariable=self.sub_text,
            wraplength=300,
            font=('Arial', 14),
            padding=10
        )
        self.sub_label.pack(pady=20)

        # Add sync button
        self.sync_btn = ttk.Button(
            self.control_frame,
            text="Sync Now (Space)",
            command=self.sync_current
        )
        self.sync_btn.pack(pady=10)

        # Add navigation controls
        self.nav_frame = ttk.Frame(self.control_frame)
        self.nav_frame.pack(pady=15)

        self.back_btn = ttk.Button(
            self.nav_frame,
            text="← Back",
            command=self.go_back
        )
        self.back_btn.pack(side=tk.LEFT, padx=5)

        self.forward_btn = ttk.Button(
            self.nav_frame,
            text="→ Next",
            command=self.load_next_subtitle
        )
        self.forward_btn.pack(side=tk.LEFT, padx=5)

        # Add jump controls
        self.jump_frame = ttk.Frame(self.control_frame)
        self.jump_frame.pack(pady=10)

        self.jump_back_btn = ttk.Button(
            self.jump_frame,
            text="⟲ -5s",
            command=lambda: self.jump_time(-5000)
        )
        self.jump_back_btn.pack(side=tk.LEFT, padx=5)

        self.jump_forward_btn = ttk.Button(
            self.jump_frame,
            text="⟳ +5s",
            command=lambda: self.jump_time(5000)
        )
        self.jump_forward_btn.pack(side=tk.LEFT, padx=5)

        # Add playback controls
        self.playback_frame = ttk.Frame(self.control_frame)
        self.playback_frame.pack(pady=10)

        self.play_btn = ttk.Button(
            self.playback_frame,
            text="Play",
            command=self.play_video
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)

        self.pause_btn = ttk.Button(
            self.playback_frame,
            text="Pause",
            command=self.pause_video
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)

        # Add current play time display
        self.time_label = ttk.Label(
            self.control_frame,
            text="Current Time: 00:00:00",
            font=('Arial', 12)
        )
        self.time_label.pack(pady=10)

        # Add status bar
        self.status = tk.StringVar()
        ttk.Label(
            self.control_frame,
            textvariable=self.status,
            font=('Arial', 10)
        ).pack(pady=10)

        # Ensure VLC player is set up before GUI updates
        self.setup_vlc_player()
        self.update_video_frame()

    def setup_vlc_player(self):
        try:
            self.vlc_instance = vlc.Instance()
            self.vlc_player = self.vlc_instance.media_player_new()
            self.vlc_media = self.vlc_instance.media_new(self.video_path)
            self.vlc_player.set_media(self.vlc_media)
            self.vlc_player.set_hwnd(self.video_label.winfo_id())
            self.vlc_player.play()
        except Exception as e:
            print(f"Error initializing VLC player: {e}")
            sys.exit(1)

    def play_video(self):
        self.is_paused = False
        self.vlc_player.play()

    def pause_video(self):
        self.is_paused = True
        self.vlc_player.pause()

    def jump_time(self, ms):
        current_time = self.vlc_player.get_time()
        new_time = max(0, current_time + ms)
        self.vlc_player.set_time(new_time)

    def cleanup(self):
        # Stop VLC player and release resources
        self.vlc_player.stop()
        self.vlc_player.release()
        self.vlc_instance.release()

        # Delete the temporary audio file
        if hasattr(self, 'audio_temp_path') and os.path.exists(self.audio_temp_path):
            try:
                os.remove(self.audio_temp_path)
            except Exception as e:
                print(f"Error deleting temporary audio file: {e}")

    # Load the next subtitle for synchronization
    def load_next_subtitle(self):
        if self.current_sub < len(self.subs):
            sub = self.subs[self.current_sub]
            self.sub_text.set(sub['text'])
            self.vlc_player.set_time(sub['start'])  # Updated to use VLC
            self.update_status()

    # Synchronize the current subtitle with the video
    def sync_current(self):
        if self.current_sub >= len(self.subs):
            return

        current_time = self.vlc_player.get_time()
        self.subs[self.current_sub]['start'] = current_time

        if self.current_sub > 0:
            self.subs[self.current_sub - 1]['end'] = current_time

        self.current_sub += 1
        if self.current_sub < len(self.subs):
            sub = self.subs[self.current_sub]
            self.sub_text.set(sub['text'])  # Prime the next subtitle without jumping
        else:
            self.sub_text.set("All subtitles synchronized!")

        self.update_status()

    # Go back to the previous subtitle
    def go_back(self):
        if self.current_sub > 0:
            self.current_sub -= 1
            self.vlc_player.set_time(self.subs[self.current_sub]['start'])  # Updated to use VLC
            self.sub_text.set(self.subs[self.current_sub]['text'])
            self.update_status()

    # Update the status bar with the current subtitle index
    def update_status(self):
        total = len(self.subs)
        self.status.set(f"Subtitle {self.current_sub + 1} of {total}")

    # Save the synchronized subtitles to a new file
    def save_srt(self):
        # Save the synchronized subtitles to a new file
        with open(self.synced_path, 'w', encoding='utf-8') as f:
            for i, sub in enumerate(self.subs):
                f.write(f"{i+1}\n")
                f.write(f"{self.ms_to_time(sub['start'])} --> {self.ms_to_time(sub['end'])}\n")
                f.write(f"{sub['text']}\n\n")

        # Save the current progress
        with open(self.synced_path + '.progress', 'w', encoding='utf-8') as f:
            f.write(str(self.current_sub))

    def prompt_resume(self):
        # Ask the user if they want to resume from the last save point
        resume = tk.messagebox.askyesno("Resume", "A synced file was found. Do you want to resume where you left off?")
        if resume:
            self.load_resume_point()

    def load_resume_point(self):
        # Load the last synced subtitle and play time from the synced file
        try:
            with open(self.synced_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for i, line in enumerate(lines):
                    if '-->' in line:
                        self.resume_point = i // 4  # Each subtitle block has 4 lines
                        break
            self.current_sub = self.resume_point
            if self.current_sub < len(self.subs):
                self.vlc_player.set_time(self.subs[self.current_sub]['start'])
                self.load_next_subtitle()
        except Exception as e:
            print(f"Error loading resume point: {e}")

# Main entry point for the script
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Subtitle Synchronizer")

    # Initialize the GUI application without requiring command-line arguments
    app = SubtitleSyncer(root)

    # Bind keyboard shortcuts
    root.bind('<space>', lambda e: app.sync_current())
    root.bind('<Left>', lambda e: app.go_back())
    root.bind('<Right>', lambda e: app.load_next_subtitle())
    root.bind('[', lambda e: app.jump_time(-5000))
    root.bind(']', lambda e: app.jump_time(5000))

    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", lambda: (app.save_srt(), app.cleanup(), root.destroy()))

    # Start the GUI event loop
    root.mainloop()
