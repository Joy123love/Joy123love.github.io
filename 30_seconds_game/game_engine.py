import random
from word_db import CARDS

class GameEngine:
    def __init__(self):
        self.cards = CARDS.copy()
        self.team_a_score = 0
        self.team_b_score = 0
        self.current_team = "Team A"
        self.used_cards = []

    def get_card(self):
        if not self.cards:
            self.cards = self.used_cards.copy()
            self.used_cards = []
            random.shuffle(self.cards)
        
        if not self.cards: # Should not happen unless DB is empty
            return ["No", "More", "Cards", "Available", "!"]

        card = random.choice(self.cards)
        self.cards.remove(card)
        self.used_cards.append(card)
        return card

    def switch_team(self):
        self.current_team = "Team B" if self.current_team == "Team A" else "Team A"
        return self.current_team

    def update_score(self, points):
        if self.current_team == "Team A":
            self.team_a_score += points
        else:
            self.team_b_score += points
    
    def get_scores(self):
        return self.team_a_score, self.team_b_score
