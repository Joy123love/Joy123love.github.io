import tkinter as tk
from tkinter import messagebox
from game_engine import GameEngine

class ThirtySecondsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("30 Seconds Game")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")

        self.engine = GameEngine()
        self.timer_value = 30
        self.timer_running = False
        self.timer_id = None

        # Fonts
        self.title_font = ("Helvetica", 24, "bold")
        self.text_font = ("Helvetica", 14)
        self.card_font = ("Helvetica", 18, "bold")

        # Container for frames
        self.container = tk.Frame(self.root, bg="#f0f0f0")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.setup_menu_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def setup_menu_screen(self):
        self.clear_container()

        title = tk.Label(self.container, text="30 Seconds", font=self.title_font, bg="#f0f0f0", fg="#333")
        title.pack(pady=50)

        start_btn = tk.Button(self.container, text="Start Game", font=self.text_font, bg="#4CAF50", fg="white",
                              command=self.start_turn_screen, padx=20, pady=10, borderwidth=0)
        start_btn.pack(pady=20)

        instruction = tk.Label(self.container, text="2 Teams. 30 Seconds. 5 Words.", font=self.text_font, bg="#f0f0f0", fg="#666")
        instruction.pack(pady=20)

    def start_turn_screen(self):
        self.clear_container()
        
        score_a, score_b = self.engine.get_scores()
        
        info_frame = tk.Frame(self.container, bg="#f0f0f0")
        info_frame.pack(fill="x", pady=10)
        
        tk.Label(info_frame, text=f"Team A: {score_a}", font=self.text_font, bg="#f0f0f0").pack(side="left", padx=20)
        tk.Label(info_frame, text=f"Team B: {score_b}", font=self.text_font, bg="#f0f0f0").pack(side="right", padx=20)

        tk.Label(self.container, text=f"It's {self.engine.current_team}'s Turn!", font=self.title_font, bg="#f0f0f0", fg="#333").pack(pady=40)

        ready_btn = tk.Button(self.container, text="Ready? Go!", font=self.text_font, bg="#2196F3", fg="white",
                              command=self.play_game_screen, padx=20, pady=10, borderwidth=0)
        ready_btn.pack(pady=10)
import tkinter as tk
from tkinter import messagebox
from game_engine import GameEngine

class ThirtySecondsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("30 Seconds Game")
        self.root.geometry("600x700")
        self.root.configure(bg="#f0f0f0")

        self.engine = GameEngine()
        self.timer_value = 30
        self.timer_running = False
        self.timer_id = None
        self.word_vars = [] # Initialize word_vars here

        # Fonts
        self.title_font = ("Helvetica", 24, "bold")
        self.text_font = ("Helvetica", 14)
        self.card_font = ("Helvetica", 18, "bold")

        # Container for frames
        self.container = tk.Frame(self.root, bg="#f0f0f0")
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.setup_menu_screen()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def setup_menu_screen(self):
        self.clear_container()

        title = tk.Label(self.container, text="30 Seconds", font=self.title_font, bg="#f0f0f0", fg="#333")
        title.pack(pady=50)

        start_btn = tk.Button(self.container, text="Start Game", font=self.text_font, bg="#4CAF50", fg="white",
                              command=self.start_turn_screen, padx=20, pady=10, borderwidth=0)
        start_btn.pack(pady=20)

        instruction = tk.Label(self.container, text="2 Teams. 30 Seconds. 5 Words.", font=self.text_font, bg="#f0f0f0", fg="#666")
        instruction.pack(pady=20)

    def start_turn_screen(self):
        self.clear_container()
        
        score_a, score_b = self.engine.get_scores()
        
        info_frame = tk.Frame(self.container, bg="#f0f0f0")
        info_frame.pack(fill="x", pady=10)
        
        tk.Label(info_frame, text=f"Team A: {score_a}", font=self.text_font, bg="#f0f0f0").pack(side="left", padx=20)
        tk.Label(info_frame, text=f"Team B: {score_b}", font=self.text_font, bg="#f0f0f0").pack(side="right", padx=20)

        tk.Label(self.container, text=f"It's {self.engine.current_team}'s Turn!", font=self.title_font, bg="#f0f0f0", fg="#333").pack(pady=40)

        ready_btn = tk.Button(self.container, text="Ready? Go!", font=self.text_font, bg="#2196F3", fg="white",
                              command=self.play_game_screen, padx=20, pady=10, borderwidth=0)
        ready_btn.pack(pady=10)

        end_game_btn = tk.Button(self.container, text="End Game", font=self.text_font, bg="#9E9E9E", fg="white",
                                 command=self.setup_menu_screen, padx=20, pady=10, borderwidth=0)
        end_game_btn.pack(pady=10)

    def play_game_screen(self):
        self.clear_container()
        
        self.timer_value = 30
        self.current_card = self.engine.get_card()

        # Timer Label
        self.timer_label = tk.Label(self.container, text=str(self.timer_value), font=("Helvetica", 48, "bold"), bg="#f0f0f0", fg="#333")
        self.timer_label.pack(pady=20)

        # Card Frame
        card_frame = tk.Frame(self.container, bg="white", bd=2, relief="solid")
        card_frame.pack(fill="both", expand=True, padx=50, pady=20)

        self.word_vars = []
        for word in self.current_card:
            var = tk.IntVar()
            self.word_vars.append(var)
            cb = tk.Checkbutton(card_frame, text=word, variable=var, font=self.card_font, bg="white", fg="#333", selectcolor="white")
            cb.pack(pady=5, anchor="w")

        # Start Timer
        self.start_timer()

        # Cancel Button (Pack first at bottom to ensure visibility)
        cancel_btn = tk.Button(self.container, text="Cancel", font=("Helvetica", 12), bg="#FF5722", fg="white",
                               command=self.cancel_turn, padx=10, pady=5, borderwidth=0)
        cancel_btn.pack(side="bottom", pady=20)

    def cancel_turn(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        self.start_turn_screen()

    def start_timer(self):
        self.timer_running = True
        self.update_timer()

    def update_timer(self):
        if self.timer_running and self.timer_value > 0:
            self.timer_value -= 1
            self.timer_label.config(text=str(self.timer_value))
            if self.timer_value <= 5:
                self.timer_label.config(fg="red")
            self.timer_id = self.root.after(1000, self.update_timer)
        elif self.timer_value == 0:
            self.end_turn_screen()

    def end_turn_screen(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
            
        self.clear_container()

        # Calculate Score
        score = sum(var.get() for var in self.word_vars)
        self.engine.update_score(score)
        self.engine.switch_team()

        tk.Label(self.container, text="Time's Up!", font=self.title_font, bg="#f0f0f0", fg="red").pack(pady=30)
        
        tk.Label(self.container, text=f"You got {score} points!", font=self.title_font, bg="#f0f0f0", fg="#4CAF50").pack(pady=20)

        next_btn = tk.Button(self.container, text="Next Team", font=self.text_font, bg="#2196F3", fg="white",
                             command=self.start_turn_screen, padx=20, pady=10, borderwidth=0)
        next_btn.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = ThirtySecondsApp(root)
    root.mainloop()
