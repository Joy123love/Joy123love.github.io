"""
Swish Kunai - Music Player Game
Main application entry point using PyQt6
"""

import sys
from PyQt6.QtWidgets import QApplication
from music_player_window import MusicPlayerWindow

def main():
    app = QApplication(sys.argv)
    window = MusicPlayerWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
