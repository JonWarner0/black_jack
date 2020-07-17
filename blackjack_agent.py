import blackjack
import random


# Q-Learning agent: currently only considering dealer and player at table
class BlackjackAgent:

    def __init__(self, _game, _player):
        self.game = _game
        self.player = _player
        # Temporary probabilities until learned
        self.bust_probability = {11:0, 12:0.31, 13:0.39, 14:0.56, 15:0.58,
                            16:0.62, 17:0.69, 18:0.77, 19:0.85, 20:0.92, 21:1}
        self.epsilon = 0.75 # exploration rate
        self.alpha = 0.8 # learning rate
        self.gamma = 0.2 # discount factor as risk of going over with more cards
        self.r = lambda  x: x+(21-x)*0.2 if x > 21 else x+(x/21)
        self.Q = {} # States = list of cards, action = hit or not
        # Q should be stored in database and pulled for each episode
        # waiting to do that until learning is stable

    def begin_learning(self):
        """ Driver for learing """
        print("Learning driver not implemented")

    # Don't know how useful this prob is.
    # replace with combinatorics
    def winning_hand_prob(self):
        """ Find the statistical probability of getting a winning hand
            Sum top wining hand probabilities: P(wining_hand)=P(X)=Sigma{19,20,21}
        """
        has_10 = any(10 in i for i in self.player.hand)
        print("Players score: {}".format(self.player.score))
        p_19 = self.calc_probability_winning_hand(19-self.player.score, has_10)
        p_20 = self.calc_probability_winning_hand(20-self.player.score, has_10)
        p_21 = self.calc_probability_winning_hand(21-self.player.score, has_10)
        return p_19+p_20+p_21

    def calc_probability_winning_hand(self, desired, has_10):
            """  key: x = favorable card, m = no. of decks, nv = total cards
                     on table, nx = no. of favorable cards left to be played

                p=(4m-nx)/(52m-nv) where x != 10
                p=(16m-nx)/(52m-nv) where x = 10
            """
            print("Desired card: {}".format(desired))
            m = self.game.deck_size
            nv = len(self.game.players)*((52*m)-len(self.game.deck))
            nx = 4 - sum(i for i, _ in self.player.hand if i == desired)
            if self.game.dealers_card == desired: # Adjust for dealers card
                nx -= 1
            if has_10:
                return ((4*m)-nx)/((52*m)-nv)
            else:
                return ((16*m)-nx)/((52*m)-nv)

    # Maybe using coin flip rather than maxing over both options to optimize learning
    def learning_iteration(self, hand, prev_hit):
        """ Q-learning iteration using version of bellman's equation.
            Tests the next iteration of learning and adds hand and score
            to the database where the results are used in after learning is
            completed.
        """
        next_card = self.game.deck.pop() # TODO Push to deck after?
        with_hit = (1-self.alpha)*self.Q[(hand,prev_hit)]+self.alpha*(
            self.r(score+next_card[0])+self.gamma*
            self.Q[(self.player.hand+[next_card], True)])
        no_hit = (1-self.alpha)*self.Q[(hand,prev_hit)]+self.alpha*(
            self.r(score+next_card[0])+self.gamma*
            self.Q[(self.player.hand+[next_card], False)])
        if with_hit > no_hit:
            self.Q[(hand, True)]
        else:
            self.Q[(hand, False)]
        #self.player.score = self.player.score + next_card[0] #dont know if needed
        #TODO send to blackjack.py for query or link connection here

    def get_action(self, state):
        if flip_coin():
            return random.choice(True,False)
        else:
            return self.Q[state]

    def flip_coin(self):
        return self.epsilon > random.random()
