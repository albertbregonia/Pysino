import cogs.Currency as c
import abc
# essentailly a semi abstract class to house general game features

class Game(abc.ABC):

    def __init__(self):
        pass

    def handleBalance(self, user, winner, bet):
        if winner == 1:
            c.changeBal(user, bet)
        elif winner == 2:
            c.changeBal(user, -1*bet)

    @abc.abstractproperty
    def tutorial(self):
        pass

    @abc.abstractproperty
    async def play(self, pysino, bot):
        pass