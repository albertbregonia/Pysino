import util.Currency as c
# essentailly a semi abstract class to house general game features

class Game:

    def __init__(self):
        pass

    def welcome(self):
        pass

    def tutorial(self):
        pass

    def handleBalance(self, user, winner, bet):
        if winner == 1:
            c.changeBal(user, bet)
        elif winner == 2:
            c.changeBal(user, -1*bet)

    def win(self, pv, dv):
        pass

    async def play(self, pysino, bot):
        pass