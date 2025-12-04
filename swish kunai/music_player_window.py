"""
Music Player Window
Displays the music player interface using asset images with clickable elements
"""

from PyQt6.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt6.QtGui import QPixmap, QPainter, QMouseEvent, QIcon
from PyQt6.QtCore import Qt, QRect, QPoint, QSize
from pathlib import Path
import pygame
import json

class ClickableButton(QPushButton):
    """Custom button that uses asset images"""
    def __init__(self, parent, image_path, x, y, width, height):
        super().__init__(parent)
        self.setGeometry(x, y, width, height)
        
        # Load and set icon
        if image_path.exists():
            icon = QIcon(str(image_path))
            self.setIcon(icon)
            self.setIconSize(QSize(width, height))
        
        # Make button transparent
        self.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 30);
                border-radius: 10px;
            }
        """)
        
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        print(f"Button clicked: {self.objectName()}")
        return True

class MusicPlayerWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Swish Kunai")
        self.setFixedSize(500, 700)
        
        # Load background pixmap (will be painted in paintEvent)
        self.background_pixmap = None
        self.load_background()
        
        # Load blue background for game mode
        self.blue_background_pixmap = None
        self.load_blue_background()
        
        # Load thumb pixmap
        self.thumb_pixmap = None
        self.load_thumb()
        
        # Define clickable album art circle area
        self.album_art_center = QPoint(250, 220)
        self.album_art_radius = 120
        
        # Add UI buttons
        self.create_buttons()
        
        # Success page (hidden initially)
        self.success_label = QLabel(self)
        self.success_label.setGeometry(0, 0, 500, 700)
        self.success_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.success_label.setStyleSheet("""
            QLabel {
                background-color: #4A9EFF;
                color: white;
                font-size: 48px;
                font-weight: bold;
            }
        """)
        self.success_label.setText("SUCCESSFUL!")
        self.success_label.hide()
        
        # Quit button for game mode (hidden initially)
        self.quit_btn = QPushButton("Quit", self)
        self.quit_btn.setGeometry(20, 10, 60, 35)  # Top left, shifted up
        self.quit_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: white;
                font-size: 16px;
                font-weight: bold;
                border-radius: 17px;
                border: 2px solid rgba(255, 255, 255, 40);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 40);
            }
        """)
        self.quit_btn.clicked.connect(self.exit_game_mode)
        self.quit_btn.hide()
        
        # Track progress for programmatic slider
        self.thumb_progress = 0.0
        
        # Rotation angle for spinning circle animation
        self.circle_rotation = 0.0
        
        # Setup animation timer for spinning circle (don't start yet)
        from PyQt6.QtCore import QTimer
        self.rotation_timer = QTimer(self)
        self.rotation_timer.timeout.connect(self.update_rotation)
        # Don't auto-start - only start when play is clicked
        
        # Click detection timer for single vs double click
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self.handle_single_click)
        self.click_count = 0
        
        # Track if music is playing (start paused by default)
        self.is_music_playing = False
        
        # Track hover state for album art
        self.is_hovering_circle = False
        self.setMouseTracking(True)  # Enable mouse tracking for hover detection
        
        # Track music folder and songs
        self.music_folder = None
        self.song_list = []
        self.current_song_index = 0
        self.current_song_name = "Unknown"
        
        # Initialize pygame mixer for music playback
        pygame.mixer.init()
        
        # Setup music end event to auto-advance to next song
        from PyQt6.QtCore import QTimer
        self.music_check_timer = QTimer(self)
        self.music_check_timer.timeout.connect(self.check_music_end)
        self.music_check_timer.start(1000)  # Check every second
        
        # Timer for updating song time display
        self.time_update_timer = QTimer(self)
        self.time_update_timer.timeout.connect(self.update_time_display)
        self.time_update_timer.start(100)  # Update every 100ms
        self.current_time = 0.0
        self.total_time = 0.0
        
        # Marquee effect for song name
        self.marquee_offset = 0
        self.marquee_timer = QTimer(self)
        self.marquee_timer.timeout.connect(self.update_marquee)
        self.marquee_timer.start(50)  # Update every 50ms for smooth scrolling
        
        # Thumb dragging state
        self.is_dragging_thumb = False
        self.slider_start_x = 100
        self.slider_end_x = 400
        self.slider_y = 484
        
        # Transition animation for game mode
        self.is_transitioning = False
        self.transition_progress = 0.0
        self.transition_timer = QTimer(self)
        self.transition_timer.timeout.connect(self.update_transition)
        
        # Reverse transition (game mode -> music mode)
        self.is_reverse_transitioning = False
        self.reverse_transition_progress = 0.0
        self.reverse_transition_timer = QTimer(self)
        self.reverse_transition_timer.timeout.connect(self.update_reverse_transition)
        
        # Game state
        self.game_score = 0
        self.game_over = False
        self.is_stopping = False  # Flag for gradual deceleration
        self.current_rotation_speed = 0.0  # Actual rotation speed (for deceleration)
        self.game_time = 0  # Track total game time in seconds
        self.last_speed_increase = 0  # Track when we last increased speed
        self.base_game_speed = 3.0  # Starting speed
        self.is_resting = False  # Flag for rest period
        self.rest_time_remaining = 0  # Countdown for rest period
        self.kunai_base_x = 250  # Center horizontally for base kunai
        self.kunai_base_y = 620  # Bottom of screen for base kunai
        # List to store active kunai: each item is {'x': x, 'y': y, 'velocity_y': vy}
        self.active_kunai = []
        # List to store kunai stuck to circle: each item is {'angle': angle_in_degrees}
        self.stuck_kunai = []
        
        # Stars for game mode background
        self.stars = []
        self.star_pixmap = None
        self.load_star_image()
        self.initialize_stars()
        
        # Load kunai image
        self.kunai_pixmap = None
        self.load_kunai()
        
        # Game update timer
        self.game_timer = QTimer(self)
        self.game_timer.timeout.connect(self.update_game)
        
        # Star animation timer
        self.star_timer = QTimer(self)
        self.star_timer.timeout.connect(self.update_stars)
        
        # Settings file path for persistent storage
        self.settings_file = Path("swish_kunai_settings.json")
        
        # Load saved settings (music folder)
        self.load_settings()
        self.star_timer.start(50)  # Update stars every 50ms
        
        # Create song list overlay (hidden initially)
        self.create_song_list_overlay()
        
        # Add + button for adding songs
        self.add_file_button()
    
    def load_star_image(self):
        """Load the star image for game mode background"""
        star_path = Path("assets") / "star.png"
        
        if star_path.exists():
            self.star_pixmap = QPixmap(str(star_path))
        else:
            print(f"Warning: Star image not found at {star_path}")
            self.star_pixmap = None
    
    def initialize_stars(self):
        """Initialize stars for game mode background"""
        import random
        
        # Create 30 stars in the top region of the screen
        self.stars = []
        for _ in range(30):
            # Random size between 10-25 pixels
            size = random.randint(10, 25)
            
            # Keep trying positions until we find one not overlapping the circle
            # Circle is at (250, 220) with radius 120
            attempts = 0
            while attempts < 50:  # Limit attempts to avoid infinite loop
                x = random.randint(20, 480)
                y = random.randint(20, 350)
                
                # Check distance from circle center
                dx = x - 250
                dy = y - 220
                distance = (dx**2 + dy**2) ** 0.5
                
                # If star is far enough from circle (radius 120 + buffer 40), use this position
                if distance > 160:
                    break
                attempts += 1
            
            star = {
                'x': x,
                'y': y,
                'size': size,  # Star size
                'pixmap': None,  # Will store scaled pixmap
                'opacity': random.uniform(0.3, 1.0),  # Starting opacity
                'fade_speed': random.uniform(0.01, 0.03),  # How fast it fades
                'fade_direction': random.choice([1, -1]),  # 1 = fade in, -1 = fade out
                'min_opacity': random.uniform(0.2, 0.4),  # Minimum brightness
                'max_opacity': random.uniform(0.7, 1.0)   # Maximum brightness
            }
            
            # Create scaled pixmap for this star if base image exists
            if self.star_pixmap:
                star['pixmap'] = self.star_pixmap.scaled(size, size,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation)
            
            self.stars.append(star)
    
    def update_stars(self):
        """Update star fade animations"""
        for star in self.stars:
            # Update opacity
            star['opacity'] += star['fade_speed'] * star['fade_direction']
            
            # Reverse direction if hitting limits
            if star['opacity'] >= star['max_opacity']:
                star['opacity'] = star['max_opacity']
                star['fade_direction'] = -1
            elif star['opacity'] <= star['min_opacity']:
                star['opacity'] = star['min_opacity']
                star['fade_direction'] = 1
        
        # Trigger repaint if in game mode
        if self.quit_btn.isVisible():
            self.update()
    
    def load_settings(self):
        """Load saved settings from JSON file"""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    saved_folder = settings.get('music_folder')
                    
                    if saved_folder and Path(saved_folder).exists():
                        # Load the saved music folder
                        self.music_folder = saved_folder
                        self.load_songs_from_folder()
                        print(f"Loaded saved music folder: {saved_folder}")
                        print(f"Found {len(self.song_list)} songs")
                        
                        # Load last song index
                        last_index = settings.get('last_song_index', 0)
                        if 0 <= last_index < len(self.song_list):
                            self.current_song_index = last_index
                            # Auto-play the last song
                            self.play_current_song()
                        else:
                            self.current_song_index = 0
                    else:
                        print("Saved folder no longer exists")
            else:
                print("No saved settings found - please select a music folder")
        except Exception as e:
            print(f"Error loading settings: {e}")
    
    def save_settings(self):
        """Save settings to JSON file"""
        try:
            settings = {
                'music_folder': self.music_folder,
                'last_song_index': self.current_song_index
            }
            with open(self.settings_file, 'w') as f:
                json.dump(settings, f, indent=2)
            print(f"Settings saved: {self.music_folder}, song index: {self.current_song_index}")
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def load_songs_from_folder(self):
        """Load all audio files from the current music folder"""
        if not self.music_folder:
            return
        
        folder_path = Path(self.music_folder)
        audio_extensions = ('.mp3', '.wav', '.flac', '.m4a', '.ogg')
        
        # Find all audio files
        self.song_list = []
        for file in folder_path.iterdir():
            if file.suffix.lower() in audio_extensions:
                self.song_list.append(file.name)
        
        # Sort alphabetically
        self.song_list.sort(key=lambda x: x.lower())
    
    def create_buttons(self):
        """Create clickable UI buttons using asset images"""
        asset_path = Path("assets")
        
        # Button positions (approximate based on typical music player layout)
        # Play button (center) - store reference for toggling
        self.play_btn = ClickableButton(self, asset_path / "play.png", 225, 550, 50, 50)
        self.play_btn.setObjectName("play")
        self.play_btn.clicked.disconnect()  # Remove default handler
        self.play_btn.clicked.connect(self.toggle_play_pause)
        
        # Store play/pause state and icons
        self.is_playing = False
        self.play_icon = QIcon(str(asset_path / "play.png"))
        self.pause_icon = QIcon(str(asset_path / "pause.png"))
        
        # Previous button
        prev_btn = ClickableButton(self, asset_path / "back.png", 150, 550, 50, 50)
        prev_btn.setObjectName("previous")
        prev_btn.clicked.disconnect()
        prev_btn.clicked.connect(self.play_previous_song)
        
        # Next button
        next_btn = ClickableButton(self, asset_path / "forward.png", 300, 550, 50, 50)
        next_btn.setObjectName("next")
        next_btn.clicked.disconnect()
        next_btn.clicked.connect(self.play_next_song)
        
        # Repeat button (right side, using infinity icon)
        self.repeat_btn = ClickableButton(self, asset_path / "infinity.png", 380, 550, 40, 40)
        self.repeat_btn.setObjectName("repeat")
        self.repeat_btn.clicked.disconnect()  # Remove default handler
        self.repeat_btn.clicked.connect(self.toggle_repeat)
        
        # Track repeat state
        self.is_repeat_on = False
    
    def toggle_play_pause(self):
        """Toggle between play and pause states"""
        # If no songs loaded, open folder dialog
        if not self.song_list:
            self.open_file_dialog()
            return True
        
        self.is_playing = not self.is_playing
        self.is_music_playing = self.is_playing  # Sync both states
        
        if self.is_playing:
            # Switch to pause icon and start rotation
            self.play_btn.setIcon(self.pause_icon)
            self.rotation_timer.start(50)
            pygame.mixer.music.unpause()
            print("Playing...")
        else:
            # Switch to play icon and stop rotation
            self.play_btn.setIcon(self.play_icon)
            self.rotation_timer.stop()
            pygame.mixer.music.pause()
            print("Paused")
        
        return True
    
    def toggle_repeat(self):
        """Toggle repeat mode on/off"""
        self.is_repeat_on = not self.is_repeat_on
        
        if self.is_repeat_on:
            # Keep highlight on
            self.repeat_btn.setStyleSheet("""
                QPushButton {
                    background-color: rgba(255, 255, 255, 30);
                    border-radius: 10px;
                    border: none;
                }
            """)
            print("Repeat ON")
        else:
            # Remove highlight
            self.repeat_btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgba(255, 255, 255, 30);
                    border-radius: 10px;
                }
            """)
            print("Repeat OFF")
        
        return True
    
    def load_background(self):
        """Load the music player background pixmap"""
        bg_path = Path("assets") / "border background.png"
        
        if bg_path.exists():
            self.background_pixmap = QPixmap(str(bg_path))
            self.background_pixmap = self.background_pixmap.scaled(500, 700, 
                Qt.AspectRatioMode.IgnoreAspectRatio, 
                Qt.TransformationMode.SmoothTransformation)
        else:
            print(f"Warning: Background image not found at {bg_path}")
            self.background_pixmap = None
    
    def load_blue_background(self):
        """Load the blue background for game mode"""
        blue_bg_path = Path("assets") / "blue background.png"
        
        if blue_bg_path.exists():
            self.blue_background_pixmap = QPixmap(str(blue_bg_path))
            self.blue_background_pixmap = self.blue_background_pixmap.scaled(500, 700,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
        else:
            print(f"Warning: Blue background image not found at {blue_bg_path}")
            self.blue_background_pixmap = None
    
    def load_thumb(self):
        """Load the thumb pixmap"""
        thumb_path = Path("assets") / "thumb.png"
        
        if thumb_path.exists():
            self.thumb_pixmap = QPixmap(str(thumb_path))
            # Scale to 48x48 (increased size)
            self.thumb_pixmap = self.thumb_pixmap.scaled(48, 48,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
        else:
            print(f"Warning: Thumb image not found at {thumb_path}")
            self.thumb_pixmap = None
    
    def load_kunai(self):
        """Load the kunai pixmap for game mode"""
        kunai_path = Path("assets") / "kunai_knife.png"
        
        if kunai_path.exists():
            self.kunai_pixmap = QPixmap(str(kunai_path))
            # Scale to double size (120 pixels tall)
            self.kunai_pixmap = self.kunai_pixmap.scaled(60, 120,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation)
            
            # Rotate 1 degree to the right to fix bent appearance
            from PyQt6.QtGui import QTransform
            transform = QTransform().rotate(1)
            self.kunai_pixmap = self.kunai_pixmap.transformed(transform,
                Qt.TransformationMode.SmoothTransformation)
        else:
            print(f"Warning: Kunai image not found at {kunai_path}")
            self.kunai_pixmap = None
    
    def add_file_button(self):
        """Add + button to open file dialog for selecting music"""
        from PyQt6.QtWidgets import QFileDialog
        
        # Create + button (moved up by 2*radius and right a bit)
        # Button radius = 17.5, so 2*radius = 35
        # Original y=640, new y = 640 - 70 = 570
        plus_btn = QPushButton("+", self)
        plus_btn.setGeometry(50, 570, 35, 35)
        plus_btn.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                font-size: 28px;
                font-weight: bold;
                border-radius: 17px;
                border: none;
            }
            QPushButton:hover {
                background-color: #333333;
            }
        """)
        plus_btn.clicked.connect(self.open_file_dialog)
    
    def create_song_list_overlay(self):
        """Create the song list overlay window"""
        from PyQt6.QtWidgets import QListWidget
        
        self.song_overlay = QLabel(self)
        self.song_overlay.setGeometry(0, 0, 500, 700)
        self.song_overlay.setStyleSheet("""
            QLabel {
                background-color: rgba(0, 0, 0, 180);
            }
        """)
        self.song_overlay.hide()
        
        # Create list widget for songs
        self.song_list_widget = QListWidget(self)
        self.song_list_widget.setGeometry(50, 100, 400, 500)
        self.song_list_widget.setStyleSheet("""
            QListWidget {
                background-color: transparent;
                color: white;
                font-family: 'Ink Free';
                font-size: 20px;
                border: none;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 30);
            }
            QListWidget::item:hover {
                background-color: rgba(255, 255, 255, 20);
            }
            QListWidget::item:selected {
                background-color: rgba(255, 255, 255, 40);
            }
        """)
        self.song_list_widget.hide()
        self.song_list_widget.itemClicked.connect(self.select_song)
        
        # Add X button to close overlay
        close_btn = QPushButton("✕", self)
        close_btn.setGeometry(430, 30, 40, 40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 20);
                color: white;
                font-size: 24px;
                font-weight: bold;
                border-radius: 20px;
                border: 2px solid rgba(255, 255, 255, 40);
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 40);
            }
        """)
        close_btn.clicked.connect(self.close_song_overlay)
        close_btn.hide()
        self.overlay_close_btn = close_btn
    
    def open_file_dialog(self):
        """Open folder dialog or show song list"""
        from PyQt6.QtWidgets import QFileDialog
        
        if self.music_folder is None:
            # First time: select folder
            folder = QFileDialog.getExistingDirectory(self, "Select Music Folder")
            
            if folder:
                self.music_folder = folder
                print(f"Music folder selected: {folder}")
                
                # Load songs from folder
                self.load_songs_from_folder()
                
                # Save settings for next time
                self.save_settings()
                
                print(f"Found {len(self.song_list)} songs")
                
                # Auto-play first song if songs were found
                if self.song_list:
                    self.current_song_index = 0
                    self.play_current_song()
                
                return True
        else:
            # Subsequent times: show song list overlay
            if self.song_list:
                self.show_song_list()
            else:
                print("No songs found in folder")
        
        return False
    
    def show_song_list(self):
        """Display the song list overlay"""
        self.song_list_widget.clear()
        for song in self.song_list:
            self.song_list_widget.addItem(song)
        
        self.song_overlay.show()
        self.song_list_widget.show()
        self.overlay_close_btn.show()
        self.song_overlay.raise_()
        self.song_list_widget.raise_()
        self.overlay_close_btn.raise_()
    
    def close_song_overlay(self):
        """Close the song list overlay"""
        self.song_overlay.hide()
        self.song_list_widget.hide()
        self.overlay_close_btn.hide()
    
    def select_song(self, item):
        """Handle song selection from list"""
        selected_song = item.text()
        print(f"Selected song: {selected_song}")
        
        # Find the index of the selected song
        self.current_song_index = self.song_list.index(selected_song)
        
        # Close the overlay
        self.close_song_overlay()
        
        # Load and play the selected song
        self.play_current_song()
    
    def play_current_song(self):
        """Load and play the current song"""
        if not self.song_list or self.current_song_index >= len(self.song_list):
            return
        
        import os
        song_path = os.path.join(self.music_folder, self.song_list[self.current_song_index])
        
        try:
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play()
            
            # Update current song name (remove file extension)
            self.current_song_name = os.path.splitext(self.song_list[self.current_song_index])[0]
            
            # Reset slider thumb to start
            self.thumb_progress = 0.0
            
            # Try to estimate song length
            try:
                from mutagen import File
                audio = File(song_path)
                if audio and audio.info:
                    self.song_length = audio.info.length
                else:
                    self.song_length = 180  # Default 3 minutes
            except:
                self.song_length = 180  # Default 3 minutes if mutagen not available
            
            # Update UI to playing state
            self.is_music_playing = True
            self.is_playing = True
            self.play_btn.setIcon(self.pause_icon)
            self.rotation_timer.start(50)
            
            # Trigger repaint to update song name
            self.update()
            
            # Save settings with current song index
            self.save_settings()
            
            print(f"Now playing: {self.song_list[self.current_song_index]}")
        except Exception as e:
            print(f"Error playing song: {e}")
    
    def check_music_end(self):
        """Check if current song has ended and advance to next"""
        if not pygame.mixer.music.get_busy() and self.is_music_playing:
            # Song has ended
            if self.is_repeat_on:
                # Repeat current song
                pygame.mixer.music.play()
                print(f"Repeating: {self.song_list[self.current_song_index]}")
            else:
                # Advance to next song
                self.play_next_song()
    
    def play_next_song(self):
        """Play the next song in the playlist"""
        if not self.song_list:
            return
        
        self.current_song_index = (self.current_song_index + 1) % len(self.song_list)
        self.play_current_song()
    
    def play_previous_song(self):
        """Play the previous song in the playlist"""
        if not self.song_list:
            return
        
        self.current_song_index = (self.current_song_index - 1) % len(self.song_list)
        self.play_current_song()
    
    def update_time_display(self):
        """Update the current playback time and slider position"""
        if pygame.mixer.music.get_busy():
            # Get position in seconds
            self.current_time = pygame.mixer.music.get_pos() / 1000.0
            
            # Update slider thumb position based on song progress
            # BUT only if user is not currently dragging the thumb
            if not self.is_dragging_thumb and hasattr(self, 'song_length') and self.song_length > 0:
                self.thumb_progress = min(self.current_time / self.song_length, 1.0)
            
            self.update()  # Trigger repaint to update time display
    
    def update_marquee(self):
        """Update marquee scrolling offset"""
        # Only scroll if music is playing
        if len(self.current_song_name) > 15 and self.is_music_playing:
            self.marquee_offset += 1
            # Reset when scrolled past the text
            if self.marquee_offset > len(self.current_song_name) * 20:  # Approximate pixel width
                self.marquee_offset = -200  # Start from right
            self.update()  # Trigger repaint
    
    def mousePressEvent(self, event: QMouseEvent):
        """Detect single and double clicks on the album art circle, and thumb dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            click_pos = event.pos()
            
            # In game mode, clicking anywhere launches a kunai
            if self.quit_btn.isVisible():
                # Check if game is over and handle button clicks
                if self.game_over:
                    # Replay button (150, 380, 200x60)
                    if 150 <= click_pos.x() <= 350 and 380 <= click_pos.y() <= 440:
                        # Replay the game
                        self.game_over = False
                        self.game_score = 0
                        self.stuck_kunai.clear()
                        self.active_kunai.clear()
                        self.rotation_direction = 1  # Reset to clockwise
                        self.is_stopping = False  # Reset stopping flag
                        self.current_rotation_speed = 0.0
                        self.game_timer.start(16)  # Restart game timer
                        print("Replaying game...")
                        self.update()
                        return
                    
                    # Close button (150, 460, 200x60)
                    if 150 <= click_pos.x() <= 350 and 460 <= click_pos.y() <= 520:
                        # Exit game mode completely
                        self.exit_game_mode()
                        return
                    
                    return  # Don't process other clicks when game over
                
                # Calculate distance from circle to see if clicking on circle
                dx = click_pos.x() - self.album_art_center.x()
                dy = click_pos.y() - self.album_art_center.y()
                distance = (dx**2 + dy**2) ** 0.5
                
                # If clicking on circle, handle double-click for exit
                if distance <= self.album_art_radius:
                    self.click_count += 1
                    
                    if self.click_count == 1:
                        # Start timer for single click (300ms delay)
                        self.click_timer.start(300)
                    elif self.click_count == 2:
                        # Double click detected - exit game mode
                        self.click_timer.stop()
                        self.click_count = 0
                        self.handle_double_click()
                else:
                    # Clicking outside circle - launch kunai
                    new_kunai = {
                        'x': self.kunai_base_x,
                        'y': self.kunai_base_y,
                        'velocity_y': -20  # Fast launch speed upward
                    }
                    self.active_kunai.append(new_kunai)
                    print(f"Kunai launched! Active kunai: {len(self.active_kunai)}")
                
                return  # Don't process other clicks in game mode
            
            # Music mode - original behavior
            # Check if clicking on thumb for dragging
            progress_x = self.slider_start_x + int(self.thumb_progress * (self.slider_end_x - self.slider_start_x))
            thumb_x = progress_x - 24  # Center of 48px thumb
            thumb_y = 460
            
            # Check if click is on thumb (48x48 area)
            if (thumb_x <= click_pos.x() <= thumb_x + 48 and 
                thumb_y <= click_pos.y() <= thumb_y + 48):
                self.is_dragging_thumb = True
                return
            
            # Calculate distance from album art center
            dx = click_pos.x() - self.album_art_center.x()
            dy = click_pos.y() - self.album_art_center.y()
            distance = (dx**2 + dy**2) ** 0.5
            
            # Check if click is within the circle
            if distance <= self.album_art_radius:
                self.click_count += 1
                
                if self.click_count == 1:
                    # Start timer for single click (300ms delay)
                    self.click_timer.start(300)
                elif self.click_count == 2:
                    # Double click detected
                    self.click_timer.stop()
                    self.click_count = 0
                    self.handle_double_click()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Detect when cursor hovers over album art circle and handle thumb dragging"""
        mouse_pos = event.pos()
        
        # Handle thumb dragging
        if self.is_dragging_thumb:
            # Calculate new progress based on mouse position
            x = mouse_pos.x()
            x = max(self.slider_start_x, min(x, self.slider_end_x))  # Clamp to slider bounds
            new_progress = (x - self.slider_start_x) / (self.slider_end_x - self.slider_start_x)
            self.thumb_progress = new_progress
            
            # Seek in the song if music is loaded
            if self.song_list and pygame.mixer.music.get_busy():
                # Get song length and seek to position
                # Note: pygame doesn't provide easy way to get total length
                # We'll use an approximate method
                try:
                    # Seek to position (in seconds)
                    # This is approximate since we don't have total duration
                    seek_time = new_progress * 180  # Assume max 3 minutes for now
                    pygame.mixer.music.set_pos(seek_time)
                except:
                    pass  # Seeking may not work for all formats
            
            self.update()
            return
        
        # Calculate distance from album art center for hover effect
        dx = mouse_pos.x() - self.album_art_center.x()
        dy = mouse_pos.y() - self.album_art_center.y()
        distance = (dx**2 + dy**2) ** 0.5
        
        # Check if hovering over the circle
        was_hovering = self.is_hovering_circle
        self.is_hovering_circle = distance <= self.album_art_radius
        
        # Trigger repaint if hover state changed
        
        # Don't update if game is over
        if self.game_over:
            return
        
        # Handle rest period
        if self.is_resting:
            # Rest period countdown happens in separate timer
            return
        
        # Update game time (16ms per frame = 0.016s)
        self.game_time += 0.016
        
        # Check for speed increase every 30 seconds
        if int(self.game_time) >= self.last_speed_increase + 30 and self.last_speed_increase < 30:
            self.base_game_speed += 1.0  # Increase by 1 degree per update
            self.last_speed_increase = int(self.game_time)
            print(f"Speed increased! New speed: {self.base_game_speed}°/update")
        
        # Check for rest period at 35 seconds
        if self.game_time >= 35 and not self.is_resting and self.last_speed_increase < 60:
            self.start_rest_period()
            return
        
        # Update all active kunai
        kunai_to_remove = []
        
        for i, kunai in enumerate(self.active_kunai):
            # Update kunai position
            kunai['y'] += kunai['velocity_y']
            kunai['velocity_y'] += 0.3  # Slight gravity effect
            
            # Circle parameters
            circle_center_x = 250
            circle_center_y = 220
            circle_radius = 120
            
            # Calculate distance from kunai tip to circle center
            # Kunai tip is at the top of the sprite (y - height/2)
            kunai_tip_y = kunai['y'] - 60  # Half of 120px height
            dx = kunai['x'] - circle_center_x
            dy = kunai_tip_y - circle_center_y
            distance = (dx**2 + dy**2) ** 0.5
            
            # Check if kunai tip touched the circle circumference
            if distance <= circle_radius and distance >= circle_radius - 30:
                # Hit! Stick the kunai to the circle
                # Calculate the angle where kunai hit in world space
                world_angle = math.degrees(math.atan2(dy, dx))
                
                # Subtract current circle rotation to get angle relative to circle's surface
                # This makes the kunai stick to a specific point on the rotating circle
                circle_surface_angle = world_angle - self.circle_rotation
                
                # Normalize to 0-360 range
                while circle_surface_angle < 0:
                    circle_surface_angle += 360
                while circle_surface_angle >= 360:
                    circle_surface_angle -= 360
                
                # Check for collision with existing stuck kunai
                collision_detected = False
                for stuck in self.stuck_kunai:
                    # Calculate angular difference
                    angle_diff = abs(stuck['angle'] - circle_surface_angle)
                    # Handle wrap-around (e.g., 359° and 1° are only 2° apart)
                    if angle_diff > 180:
                        angle_diff = 360 - angle_diff
                    
                    # If kunai are within 5 degrees of each other, it's a collision
                    if angle_diff < 5:
                        collision_detected = True
                        break
                
                if collision_detected:
                    # Game Over!
                    self.game_over = True
                    self.game_timer.stop()
                    print(f"GAME OVER! Kunai collision detected. Final Score: {self.game_score}")
                    self.update()  # Trigger repaint to show game over screen
                else:
                    # Add to stuck kunai with the surface-relative angle
                    self.stuck_kunai.append({'angle': circle_surface_angle})
                    
                    # Increase score
                    self.game_score += 5
                    print(f"Hit! Score: {self.game_score}, Stuck kunai: {len(self.stuck_kunai)}, angle: {circle_surface_angle:.1f}°")
                
                # Mark for removal from active list either way
                kunai_to_remove.append(i)
            # Remove if kunai goes off screen (top)
            elif kunai['y'] < -150:
                kunai_to_remove.append(i)
        
        # Remove kunai that hit or went off screen (iterate backwards to avoid index issues)
        for i in reversed(kunai_to_remove):
            self.active_kunai.pop(i)
        
        # Trigger repaint if there are active kunai or stuck kunai
        if self.active_kunai or self.stuck_kunai:
            self.update()
    
    def start_rest_period(self):
        """Start the 1-minute rest period"""
        self.is_resting = True
        self.rest_time_remaining = 60
        print("Rest period started! Take a 1-minute break...")
        from PyQt6.QtCore import QTimer
        self.rest_timer = QTimer(self)
        self.rest_timer.timeout.connect(self.update_rest_countdown)
        self.rest_timer.start(1000)
        self.update()
    
    def update_rest_countdown(self):
        """Update the rest period countdown"""
        self.rest_time_remaining -= 1
        if self.rest_time_remaining <= 0:
            self.rest_timer.stop()
            self.is_resting = False
            self.last_speed_increase = 60
            print("Rest period over! Game resuming...")
            self.update()
        else:
            self.update()
    
    def handle_single_click(self):
        """Handle single click - toggle play/pause and rotation (disabled in game mode)"""
        # Ignore single clicks in game mode
        if self.quit_btn.isVisible():
            self.click_count = 0
            return
        
        self.click_count = 0
        
        # If no songs loaded, open folder dialog
        if not self.song_list:
            print("No songs loaded, opening folder dialog...")
            self.open_file_dialog()
            return
        
        self.is_music_playing = not self.is_music_playing
        
        if self.is_music_playing:
            print("Music playing...")
            # Resume music playback
            pygame.mixer.music.unpause()
            # Start rotation animation
            self.rotation_timer.start(50)
            # Also update the play button icon
            self.is_playing = True
            self.play_btn.setIcon(self.pause_icon)
        else:
            print("Music paused")
            # Pause music playback
            pygame.mixer.music.pause()
            # Stop rotation animation
            self.rotation_timer.stop()
            # Also update the play button icon
            self.is_playing = False
            self.play_btn.setIcon(self.play_icon)
    
    def handle_double_click(self):
        """Handle double click - toggle between music mode and game mode"""
        if self.quit_btn.isVisible():
            # Already in game mode, exit back to music mode
            print("Exiting game mode via double-click...")
            self.exit_game_mode()
        else:
            # Enter game mode
            print("Entering game mode...")
            self.show_game_mode()
    
    def show_game_mode(self):
        """Show game mode with smooth transition"""
        print("Starting transition to game mode...")
        self.is_transitioning = True
        self.transition_progress = 0.0
        self.transition_timer.start(16)  # ~60 FPS
        
        # Automatically start rotation when entering game mode with faster speed
        self.rotation_timer.stop()  # Stop current rotation
        self.rotation_timer.start(50)  # Same interval, but will rotate 2 degrees per update
        
        # Reinitialize stars for fresh animation
        self.initialize_stars()
        
        # Start game timer
        self.game_timer.start(16)  # ~60 FPS for smooth game physics
    
    def update_transition(self):
        """Update transition animation"""
        self.transition_progress += 0.02  # Adjust speed (0.02 = ~0.8 seconds)
        
        # Fade out all buttons during transition using graphics effect
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        button_opacity = 1.0 - self.transition_progress
        for child in self.findChildren(QPushButton):
            if child != self.quit_btn and child != self.overlay_close_btn:
                # Create or update opacity effect
                effect = child.graphicsEffect()
                if effect is None or not isinstance(effect, QGraphicsOpacityEffect):
                    effect = QGraphicsOpacityEffect(child)
                    child.setGraphicsEffect(effect)
                effect.setOpacity(button_opacity)
        
        if self.transition_progress >= 1.0:
            self.transition_progress = 1.0
            self.transition_timer.stop()
            self.is_transitioning = False
            
            # Hide all music player buttons after fade completes
            self.play_btn.hide()
            self.repeat_btn.hide()
            # Hide all other buttons by finding them
            for child in self.findChildren(QPushButton):
                if child != self.quit_btn:
                    child.hide()
            
            # Show quit button (no text label needed)
            self.quit_btn.show()
            self.quit_btn.raise_()
        
        self.update()  # Trigger repaint
    
    def exit_game_mode(self):
        """Exit game mode and return to music player with fade-in transition"""
        print("Exiting game mode...")
        self.quit_btn.hide()
        
        # Hide overlay close button if visible
        self.overlay_close_btn.hide()
        
        # Rotation speed will automatically adjust back to normal (1 degree) when not in game mode
        
        # Stop game timer and reset game state
        self.game_timer.stop()
        self.active_kunai.clear()  # Remove all active kunai
        self.stuck_kunai.clear()  # Remove all stuck kunai
        self.game_over = False  # Reset game over state
        self.game_time = 0  # Reset game time
        self.last_speed_increase = 0  # Reset speed tracking
        self.base_game_speed = 3.0  # Reset to starting speed
        self.is_resting = False  # Reset rest state
        
        # Start reverse transition
        self.is_reverse_transitioning = True
        self.reverse_transition_progress = 0.0
        self.reverse_transition_timer.start(16)  # ~60 FPS
    
    def update_reverse_transition(self):
        """Update reverse transition animation (game mode -> music mode)"""
        self.reverse_transition_progress += 0.02  # Same speed as forward transition
        
        # Fade in all buttons during reverse transition
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        button_opacity = self.reverse_transition_progress
        for child in self.findChildren(QPushButton):
            if child != self.quit_btn and child != self.overlay_close_btn:
                # Create or update opacity effect
                effect = child.graphicsEffect()
                if effect is None or not isinstance(effect, QGraphicsOpacityEffect):
                    effect = QGraphicsOpacityEffect(child)
                    child.setGraphicsEffect(effect)
                effect.setOpacity(button_opacity)
                child.show()  # Make sure button is visible
        
        if self.reverse_transition_progress >= 1.0:
            self.reverse_transition_progress = 1.0
            self.reverse_transition_timer.stop()
            self.is_reverse_transitioning = False
            
            # Ensure all buttons are at full opacity
            for child in self.findChildren(QPushButton):
                if child != self.quit_btn and child != self.overlay_close_btn:
                    effect = child.graphicsEffect()
                    if effect and isinstance(effect, QGraphicsOpacityEffect):
                        effect.setOpacity(1.0)
        
        self.update()  # Trigger repaint
    
    def show_success_page(self):
        """Show the success page (game mode entry)"""
        # This method is no longer used for game mode
        pass
    
    def update_rotation(self):
        """Update rotation angle for spinning animation"""
        # Rotation speed depends on mode and game state
        if self.quit_btn.isVisible():
            # Game mode
            if self.is_stopping:
                # Gradual deceleration to stop
                if abs(self.current_rotation_speed) > 0.01:
                    # Reduce speed by 2% each frame (smooth deceleration)
                    self.current_rotation_speed *= 0.98
                    rotation_speed = self.current_rotation_speed
                else:
                    # Stopped completely
                    rotation_speed = 0
                    self.current_rotation_speed = 0
                    # Hide game over overlay once stopped
                    if self.game_over:
                        self.game_over = False
            elif self.game_over or self.is_resting:
                # Game over or resting: slow rotation
                rotation_speed = 0.5
            else:
                # Active gameplay: use current game speed (increases over time)
                rotation_speed = self.base_game_speed
        else:
            # Music mode: normal rotation (always clockwise)
            rotation_speed = 1.0
        
        # Update rotation (can go negative or beyond 360)
        self.circle_rotation += rotation_speed
        
        # No normalization - allow rotation to accumulate in either direction
        # This ensures stuck kunai stay in the correct position
        
        self.update()  # Trigger repaint
    
    def paintEvent(self, event):
        """Draw all UI elements in correct order"""
        from PyQt6.QtGui import QFont, QPainterPath, QPen, QColor, QBrush
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Handle transition animation (music -> game)
        if self.is_transitioning:
            # Blend between purple and blue backgrounds
            if self.background_pixmap and self.blue_background_pixmap:
                # Draw purple background
                painter.setOpacity(1.0 - self.transition_progress)
                painter.drawPixmap(0, 0, self.background_pixmap)
                
                # Draw blue background on top with increasing opacity
                painter.setOpacity(self.transition_progress)
                painter.drawPixmap(0, 0, self.blue_background_pixmap)
                
                # Draw UI elements with fading opacity (inverse of blue background)
                painter.setOpacity(1.0 - self.transition_progress)
                
                # Continue to draw UI elements below with reduced opacity
            else:
                return  # Don't draw UI if backgrounds not loaded
        # Handle reverse transition animation (game -> music)
        elif self.is_reverse_transitioning:
            # Blend between blue and purple backgrounds
            if self.background_pixmap and self.blue_background_pixmap:
                # Draw blue background
                painter.setOpacity(1.0 - self.reverse_transition_progress)
                painter.drawPixmap(0, 0, self.blue_background_pixmap)
                
                # Draw purple background on top with increasing opacity
                painter.setOpacity(self.reverse_transition_progress)
                painter.drawPixmap(0, 0, self.background_pixmap)
                
                # Draw UI elements with increasing opacity
                painter.setOpacity(self.reverse_transition_progress)
                
                # Continue to draw UI elements below with increasing opacity
            else:
                return  # Don't draw UI if backgrounds not loaded
        else:
            painter.setOpacity(1.0)  # Full opacity when not transitioning
        
        # Draw background image first
        if self.quit_btn.isVisible() and self.blue_background_pixmap:
            # Game mode - show blue background
            painter.drawPixmap(0, 0, self.blue_background_pixmap)
            # Continue to draw circle in game mode (don't return yet)
        elif self.background_pixmap:
            # Music player mode - show purple background
            painter.drawPixmap(0, 0, self.background_pixmap)
        else:
            painter.fillRect(self.rect(), QColor(180, 120, 220))
        
        # Don't draw UI elements if success screen is showing (but allow circle in game mode)
        if self.success_label.isVisible() and not self.quit_btn.isVisible():
            return
        
        # Initialize pen
        pen = QPen()
        
        # Draw hover glow effect around circle (before rotation, so it doesn't rotate)
        if self.is_hovering_circle:
            # Draw multiple rings for glow effect
            for i in range(3):
                alpha = 60 - (i * 20)  # Fade out as rings get larger
                pen.setColor(QColor(255, 255, 255, alpha))
                pen.setWidth(8 - (i * 2))
                painter.setPen(pen)
                painter.setBrush(Qt.BrushStyle.NoBrush)
                offset = i * 4
                painter.drawEllipse(130 - offset, 100 - offset, 240 + (offset * 2), 240 + (offset * 2))
        
        # Draw circle for MUSIC MODE (will be redrawn on top in game mode)
        if not self.quit_btn.isVisible():
            # Save painter state before rotation
            painter.save()
            
            # Rotate around the circle center (250, 220)
            painter.translate(250, 220)
            painter.rotate(self.circle_rotation)
            painter.translate(-250, -220)
            
            # Draw circle (filled white with black border)
            painter.setOpacity(1.0)
            painter.setBrush(QBrush(QColor(255, 255, 255)))  # White fill
            pen.setColor(QColor(0, 0, 0))
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawEllipse(130, 100, 240, 240)
            
            # Draw music note
            painter.setOpacity(1.0)
            music_font = QFont("Ink Free", 140, QFont.Weight.Bold)
            painter.setFont(music_font)
            path = QPainterPath()
            path.addText(195, 280, music_font, "♪")
            pen.setColor(QColor(0, 0, 0))
            pen.setWidth(5)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)
            painter.fillPath(path, QBrush(QColor(0, 0, 0)))
            
            # Restore painter state after rotation
            painter.restore()
        
        # If in game mode, stop here (only show circle, no other UI)
        if self.quit_btn.isVisible():
            # Draw twinkling stars in the background
            painter.setOpacity(1.0)
            for star in self.stars:
                if star['pixmap']:
                    # Set star opacity for fade effect
                    painter.setOpacity(star['opacity'])
                    
                    # Draw star image centered at position
                    star_x = int(star['x'] - star['size']/2)
                    star_y = int(star['y'] - star['size']/2)
                    painter.drawPixmap(star_x, star_y, star['pixmap'])
            
            # Reset opacity for other elements
            painter.setOpacity(1.0)
            
            # Draw stuck kunai (they rotate with the circle) - OUTSIDE rotation transform
            if self.kunai_pixmap and self.stuck_kunai:
                import math
                circle_center_x = 250
                circle_center_y = 220
                circle_radius = 120
                
                print(f"Rendering {len(self.stuck_kunai)} stuck kunai at rotation {self.circle_rotation:.1f}°")
                
                for i, stuck in enumerate(self.stuck_kunai):
                    # Calculate current angle including circle rotation
                    current_angle = stuck['angle'] + self.circle_rotation
                    angle_rad = math.radians(current_angle)
                    
                    # Position kunai tip on the circumference
                    kunai_tip_x = circle_center_x + circle_radius * math.cos(angle_rad)
                    kunai_tip_y = circle_center_y + circle_radius * math.sin(angle_rad)
                    
                    # Kunai center should be offset OUTWARD from tip
                    kunai_center_x = kunai_tip_x + 60 * math.cos(angle_rad)
                    kunai_center_y = kunai_tip_y + 60 * math.sin(angle_rad)
                    
                    print(f"  Kunai {i}: angle={stuck['angle']:.1f}° current={current_angle:.1f}° pos=({kunai_center_x:.0f}, {kunai_center_y:.0f})")
                    
                    # Save painter state for individual kunai rotation
                    painter.save()
                    
                    # Translate to kunai position and rotate to point outward
                    painter.translate(kunai_center_x, kunai_center_y)
                    painter.rotate(current_angle - 90)  # -90 to point outward
                    
                    # Draw kunai centered at origin
                    kunai_draw_x = -self.kunai_pixmap.width() / 2
                    kunai_draw_y = -self.kunai_pixmap.height() / 2
                    painter.drawPixmap(int(kunai_draw_x), int(kunai_draw_y), self.kunai_pixmap)
                    
                    # Restore painter state
                    painter.restore()
            
            # Draw score at top center
            score_font = QFont("Ink Free", 32, QFont.Weight.Bold)
            painter.setFont(score_font)
            pen.setColor(QColor(255, 255, 255))  # White text
            pen.setWidth(2)
            painter.setPen(pen)
            painter.setOpacity(1.0)
            score_text = f"SCORE: {self.game_score}"
            painter.drawText(0, 30, 500, 50, Qt.AlignmentFlag.AlignCenter, score_text)
            
            # Draw base kunai at bottom (always visible)
            if self.kunai_pixmap:
                base_kunai_x = int(self.kunai_base_x - self.kunai_pixmap.width() / 2)
                base_kunai_y = int(self.kunai_base_y - self.kunai_pixmap.height() / 2)
                painter.drawPixmap(base_kunai_x, base_kunai_y, self.kunai_pixmap)
            
            # Draw all active (launched) kunai
            if self.kunai_pixmap:
                for kunai in self.active_kunai:
                    kunai_x = int(kunai['x'] - self.kunai_pixmap.width() / 2)
                    kunai_y = int(kunai['y'] - self.kunai_pixmap.height() / 2)
                    painter.drawPixmap(kunai_x, kunai_y, self.kunai_pixmap)
            
            # NOW draw circle and stuck kunai as TOP LAYER
            # Save painter state before rotation
            painter.save()
            
            # Rotate around the circle center (250, 220)
            painter.translate(250, 220)
            painter.rotate(self.circle_rotation)
            painter.translate(-250, -220)
            
            # Draw circle (filled white with black border)
            painter.setOpacity(1.0)
            painter.setBrush(QBrush(QColor(255, 255, 255)))  # White fill
            pen = QPen()
            pen.setColor(QColor(0, 0, 0))
            pen.setWidth(5)
            painter.setPen(pen)
            painter.drawEllipse(130, 100, 240, 240)
            
            # Draw music note
            painter.setOpacity(1.0)
            music_font = QFont("Ink Free", 140, QFont.Weight.Bold)
            painter.setFont(music_font)
            path = QPainterPath()
            path.addText(195, 280, music_font, "♪")
            pen.setColor(QColor(0, 0, 0))
            pen.setWidth(5)
            painter.setPen(pen)
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawPath(path)
            painter.fillPath(path, QBrush(QColor(0, 0, 0)))
            
            # Restore painter state after rotation
            painter.restore()
            
            # Draw stuck kunai as ABSOLUTE TOP LAYER
            if self.kunai_pixmap and self.stuck_kunai:
                import math
                circle_center_x = 250
                circle_center_y = 220
                circle_radius = 120
                
                for i, stuck in enumerate(self.stuck_kunai):
                    # Calculate current angle including circle rotation
                    current_angle = stuck['angle'] + self.circle_rotation
                    angle_rad = math.radians(current_angle)
                    
                    # Position kunai tip on the circumference
                    kunai_tip_x = circle_center_x + circle_radius * math.cos(angle_rad)
                    kunai_tip_y = circle_center_y + circle_radius * math.sin(angle_rad)
                    
                    # Kunai center should be offset OUTWARD from tip
                    kunai_center_x = kunai_tip_x + 60 * math.cos(angle_rad)
                    kunai_center_y = kunai_tip_y + 60 * math.sin(angle_rad)
                    
                    # Save painter state for individual kunai rotation
                    painter.save()
                    
                    # Translate to kunai position and rotate to point outward
                    painter.translate(kunai_center_x, kunai_center_y)
                    painter.rotate(current_angle - 90)  # -90 to point outward
                    
                    # Draw kunai centered at origin
                    kunai_draw_x = -self.kunai_pixmap.width() / 2
                    kunai_draw_y = -self.kunai_pixmap.height() / 2
                    painter.drawPixmap(int(kunai_draw_x), int(kunai_draw_y), self.kunai_pixmap)
                    
                    # Restore painter state
                    painter.restore()
            
            # Draw Game Over overlay if game is over
            if self.game_over:
                # Semi-transparent black overlay
                painter.setOpacity(0.8)
                painter.fillRect(0, 0, 500, 700, QColor(0, 0, 0))
                
                # Game Over text
                painter.setOpacity(1.0)
                game_over_font = QFont("Ink Free", 48, QFont.Weight.Bold)
                painter.setFont(game_over_font)
                pen.setColor(QColor(255, 50, 50))  # Red
                pen.setWidth(3)
                painter.setPen(pen)
                painter.drawText(0, 200, 500, 60, Qt.AlignmentFlag.AlignCenter, "GAME OVER!")
                
                # Final Score
                score_font = QFont("Ink Free", 36, QFont.Weight.Bold)
                painter.setFont(score_font)
                pen.setColor(QColor(255, 255, 255))  # White
                painter.setPen(pen)
                painter.drawText(0, 280, 500, 50, Qt.AlignmentFlag.AlignCenter, f"Final Score: {self.game_score}")
                
                # Replay button
                replay_rect = QRect(150, 380, 200, 60)
                painter.setBrush(QBrush(QColor(50, 200, 50)))  # Green
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(replay_rect, 10, 10)
                
                button_font = QFont("Ink Free", 24, QFont.Weight.Bold)
                painter.setFont(button_font)
                pen.setColor(QColor(255, 255, 255))
                painter.setPen(pen)
                painter.drawText(replay_rect, Qt.AlignmentFlag.AlignCenter, "REPLAY")
                
                # Close button
                close_rect = QRect(150, 460, 200, 60)
                painter.setBrush(QBrush(QColor(200, 50, 50)))  # Red
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(close_rect, 10, 10)
                
                painter.setFont(button_font)
                pen.setColor(QColor(255, 255, 255))
                painter.setPen(pen)
                painter.drawText(close_rect, Qt.AlignmentFlag.AlignCenter, "CLOSE")
            
            # Draw Rest Period overlay if resting
            if self.is_resting:
                painter.setOpacity(0.85)
                painter.fillRect(0, 0, 500, 700, QColor(0, 0, 0))
                painter.setOpacity(1.0)
                rest_font = QFont("Ink Free", 42, QFont.Weight.Bold)
                painter.setFont(rest_font)
                pen.setColor(QColor(100, 200, 255))
                pen.setWidth(2)
                painter.setPen(pen)
                painter.drawText(0, 250, 500, 60, Qt.AlignmentFlag.AlignCenter, "REST PERIOD")
                countdown_font = QFont("Ink Free", 72, QFont.Weight.Bold)
                painter.setFont(countdown_font)
                pen.setColor(QColor(255, 255, 255))
                painter.setPen(pen)
                painter.drawText(0, 320, 500, 100, Qt.AlignmentFlag.AlignCenter, f"{self.rest_time_remaining}")
                instruction_font = QFont("Ink Free", 24)
                painter.setFont(instruction_font)
                painter.drawText(0, 450, 500, 40, Qt.AlignmentFlag.AlignCenter, "Take a break!")
            
            return
        
        # Draw song name with marquee effect between circle and slider
        text_font = QFont("Ink Free", 22, QFont.Weight.Bold)  # Decreased from 28 to 22pt
        painter.setFont(text_font)
        pen.setWidth(1)
        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)
        
        # Create clipping region for marquee effect (increased width)
        painter.save()
        clip_rect = QRect(100, 380, 300, 30)  # Increased from 200 to 300 width, moved left
        painter.setClipRect(clip_rect)
        
        # Draw text with offset for marquee
        if len(self.current_song_name) > 15:
            # Scrolling text
            painter.drawText(100 - self.marquee_offset, 380, 500, 30, 
                           Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, 
                           self.current_song_name)
        else:
            # Centered text for short names
            painter.drawText(100, 380, 300, 30, Qt.AlignmentFlag.AlignCenter, self.current_song_name)
        
        painter.restore()
        
        # Draw time display below left side of slider
        time_font = QFont("Ink Free", 18, QFont.Weight.Bold)  # Increased from 14 to 18pt, made bold
        painter.setFont(time_font)
        pen.setColor(QColor(0, 0, 0))  # Changed to black
        pen.setWidth(2)  # Increased thickness
        painter.setPen(pen)
        # Format time as MM:SS
        minutes = int(self.current_time // 60)
        seconds = int(self.current_time % 60)
        time_text = f"{minutes:02d}:{seconds:02d}"
        painter.drawText(100, 500, 80, 25, Qt.AlignmentFlag.AlignLeft, time_text)  # Increased width from 60 to 80
        
        # Draw progress slider line
        pen.setColor(QColor(100, 100, 100))  # Gray line
        pen.setWidth(6)
        painter.setPen(pen)
        # Slider from x=100 to x=400, y=484
        painter.drawLine(100, 484, 400, 484)
        
        # Draw progress fill (based on thumb_progress)
        pen.setColor(QColor(150, 100, 200))  # Purple progress
        pen.setWidth(6)
        painter.setPen(pen)
        progress_x = 100 + int(self.thumb_progress * 300)
        painter.drawLine(100, 484, progress_x, 484)
        
        # Draw thumb using thumb.png
        if self.thumb_pixmap:
            # Center the thumb image at progress_x (48px image)
            thumb_x = progress_x - 24  # Center 48px image
            thumb_y = 460  # Vertical position (adjusted for larger size)
            painter.drawPixmap(thumb_x, thumb_y, self.thumb_pixmap)
        else:
            # Fallback to programmatic circle if image not loaded
            painter.setBrush(QBrush(QColor(200, 150, 230)))  # Purple thumb
            pen.setColor(QColor(0, 0, 0))
            pen.setWidth(2)
            painter.setPen(pen)
            painter.drawEllipse(progress_x - 24, 460, 48, 48)
        
        # Reset opacity at the end
        painter.setOpacity(1.0)
