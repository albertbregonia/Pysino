# essentailly a semi abstract class to house general game features

class Game:

    def __init__(self):
        pass

    def welcome(self):
        pass

    def tutorial(self):
        pass

    def handleBalance(self, user):
        pass # fill in with something that handles balance per user

    async def play(self, pysino, bot):
        pass