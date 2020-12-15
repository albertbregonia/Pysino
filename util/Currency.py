from discord.ext import commands as cmd
import os

# ==== UTILITY FUNCTIONS ==== #

def changeBal(user, amt):
    bal = getBal(user)+amt # amt should be negative to take away
    userFile = open(f'users/{user}.txt', 'w')
    userFile.write(f'${bal}')
    userFile.close()

def getBal(user):
    userFile = open(f'users/{user}.txt', 'r')
    bal = int(userFile.readline()[1:]) # [1:] to ignore $
    userFile.close()
    return bal

# ==== BOT FUNCTIONS ==== #

class Currency(cmd.Cog):

    def __init__(self, pysino):
        self.pysino = pysino

    @cmd.command(help='Give another player money some of your money')
    async def give(self, bot, get, amt):
        give = str(bot.author)
        amt = int(amt)
        if getBal(give) >= amt and amt > 0:
            changeBal(give, -1*amt)
            changeBal(get, amt)
            await bot.channel.send(f'{bot.author.mention}, you have successfully given `{get}` ${amt}')
        elif amt < 0:
            await bot.channel.send(f'BROKE: {bot.author.mention}, you have unsuccessfully tried to rob this mans `{get}`. What\'s wrong with you bro?')
        else:
            await bot.channel.send(f'{bot.author.mention}, you do not have the funds to support this transaction! Please use: `*bal`')
    
    @cmd.command(help='Display your current balance')
    async def bal(self, bot):
        if os.path.exists(f'users/{str(bot.author)}.txt'):
            await bot.channel.send(f'{bot.author.mention}, your current balance is: **${getBal(str(bot.author))}**')
        else:
            await bot.channel.send(f'{bot.author.mention}, please register with our database before you display your balance! Please use `*register`.')

def setup(pysino):
    pysino.add_cog(Currency(pysino))
