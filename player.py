class player:

    def __init__(self, _name):
        self.name = _name
        self.bets = 0
        self.hand = None # cards
        self.score = 0 # cards total value
        self.over_flag = False # player has exceeded 21


    def make_bet(self, bet):
        self.bets += bet


    def new_round(self, cards):
        self.hand = cards
        self.bets = 0
        self.over_flag = False
