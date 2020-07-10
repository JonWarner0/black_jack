class blackjack_game:

    def __init__(self, _players):
        self.players = _players
        self.deck_size = 1
        self.deck = self.make_deck(self.deck_size)
        for p in self.players:
            p.hand = [self.deck.pop(), self.deck.pop()]
            p.score = sum(i for i, _ in p.hand)
        self.pot = 0
        self.dealers_card = None


    def begin_game(self):
        """ Starts the game """
        # Dealer shows one card
        self.ace_check(self.players[0], True)
        self.dealers_card = self.players[0].hand[0]
        print("=> The Dealer has: {}".format(self.dealers_card))
        # start betting
        for i in range(1, 2):
            print("\n-------------------")
            print("| Round {} of Bets |".format(i))
            print("-------------------\n")
            self.round_of_bets()
        # Players can ask for more cards
        self.hit_round()
        result = self.reveal_cards()
        if result:
            return result
        else: # need to go another round until a winner emerges
            print("No winners, going another round.")
            for p in self.players: # Deal new cards
                p.new_round([self.deck.pop(), self.deck.pop()])
                p.score = sum(i for i, _ in p.hand)
            self.begin_game()


    def round_of_bets(self):
        """ Prompt players to place bets and add to pot """
        for p in self.players[1:]:
            while(True):
                try:
                    bet = int(input("{} what is your bet? ".format(p.name)))
                    p.make_bet(bet)
                    self.pot += bet
                    break
                except ValueError:
                    print("! ERROR ! Please enter an integer value.")
            print("------------------")


    # Determine winner or tie which will need another round
    def reveal_cards(self):
        """ Reveal all players cards to determine if a player won """
        winner = None
        tie_score = 0
        # Dealer needs score of at least 17 (Dealer is always at 0)
        self.ace_check(self.players[0], True)
        #self.players[0].score = sum(i for i, _ in self.players[0].hand)
        while self.players[0].score < 17:
            self.players[0].hand.append(self.deck.pop()) #give another
            self.ace_check(self.players[0], True) #check for ace
            self.players[0].score = sum(i for i, _ in self.players[0].hand)
            if self.players[0].score > 21: # check if bust
                self.players[0].over_flag = True
                break
        # Find winner or tie
        for p in self.players:
            if p.over_flag:
                continue
            try:
                if winner.score == p.score:
                    tie_score = p.score
                elif p.score > winner.score and p.score <= 21:
                    winner = p
            except AttributeError: # First iteration will always trigger this
                winner = p         # and I didnt want to do an if
        # Check for win or tie
        try: # If all bust then winner will be None
            if winner.score > tie_score:
                return winner
            else:
                return None
        except AttributeError:
            return None


    def hit_round(self):
        """ Players can request more cards. *NO SPLITTING YET*. """
        for p in self.players[1:]:
            if sum(i for i, _ in p.hand) > 21: # check if initial hand is over
                p.over_flag = True
                continue
            while True:
                print("=> Your cards are {}".format(p.hand))
                hit = input("{}, Hit? (Y/N): ".format(p.name)).upper()
                if hit == 'Y':
                    p.hand.append(self.deck.pop())
                    print("added card: {}".format(p.hand[-1]))
                    self.ace_check(p)
                    p.score = sum(i for i, _ in p.hand) # Update score
                    if p.score > 21:
                        print("__You went over__")
                        p.over_flag = True
                        break
                elif hit == "N":
                    break
            print("------------------")


    def ace_check(self, player, is_Dealer=False):
        """ Special cases for Ace cards to give player best chance of win """
        if is_Dealer:
            for c in player.hand:
                if c[0] == 1:
                    player.hand.append((11, c[1]))
                    player.hand.remove(c)
        for c in player.hand:
            if c[0] == 1:
                if player.score > 10: # would cause loss so break
                    break
                else: # can change to a higher number safely
                    player.hand.append((11, c[1]))
                    player.hand.remove(c)
            if c[0] == 11 and player.score > 21: # keeps player in game
                player.hand.append((1, c[1]))
                player.hand.remove(c)



    # Create the deck
    def make_deck(self, size):
        """ Makes the deck in a set for arbitrary pops. Aces handled above.
            formated so that duplicate card values can exist in set for
            a lazy mans shuffle.
        """
        deck = set()
        for j in range(0, size):
            for i in range(1,10):
                deck.add((i, "spades-{}".format(j)))
                deck.add((i, "clubs-{}".format(j)))
                deck.add((i, "diamonds-{}".format(j)))
                deck.add((i, "hearts-{}".format(j)))
            deck.add((10, "jack-spades-{}".format(j)))
            deck.add((10, "queen-spades-{}".format(j)))
            deck.add((10, "king-spades-{}".format(j)))
            deck.add((10, "jack-clubs-{}".format(j)))
            deck.add((10, "queen-clubs-{}".format(j)))
            deck.add((10, "king-clubs-{}".format(j)))
            deck.add((10, "jack-diamonds-{}".format(j)))
            deck.add((10, "queen-diamonds-{}".format(j)))
            deck.add((10, "king-diamonds-{}".format(j)))
            deck.add((10, "jack-hearts-{}".format(j)))
            deck.add((10, "queen-hearts-{}".format(j)))
            deck.add((10, "king-hearts-{}".format(j)))
        return [i for i in deck] #return list for stack properties
