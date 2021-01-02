from discord.ext import commands as cmd
import os
import random as r
import operator

# ==== UTILITY FUNCTIONS ==== #

def changeBal(user, amt):
    bal = getBal(user)+amt # amt should be negative to take away
    with open(f'users/{user}.txt', 'w') as userFile:
        userFile.write(f'${bal}')

def getBal(user):
    with open(f'users/{user}.txt', 'r') as userFile:
        return int(userFile.readline()[1:]) # [1:] to ignore $

# ==== BOT FUNCTIONS ==== #

class Currency(cmd.Cog):

    def __init__(self, pysino):
        self.pysino = pysino

    @cmd.command(help='Earn money doing math. Rate is $2 per digit in the answer')
    async def work(self, bot):
        num1, num2 = r.randint(0,256), r.randint(0,256)
        ops = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.truediv} #operators
        op = list(ops.keys())[r.randrange(0,4)] #select random operator
        ans = int(ops[op](num1,num2))
        await bot.channel.send(f'{bot.author.mention}, Solve this equation to earn money ***Integer Answers Only*** : `{num1}{op}{num2} = ?`')
        error = True
        while error:
            response = await self.pysino.wait_for('message', check=lambda message: message.author == bot.author)
            try:
                if int(response.content) == ans:
                    earned = len(str(abs(ans)))*2
                    changeBal(str(bot.author), earned)
                    await bot.channel.send(f'{bot.author.mention}, you have successfully earned **${earned}**.')
                else:
                    await bot.channel.send(f'{bot.author.mention}, unfortunately you were incorrect. Correct answer: {ans}')
                break
            except:
                await bot.channel.send(f'{bot.author.mention}, unfortunately your input was invalid. Please try again.')


    @cmd.command(help='Give another player money')
    async def give(self, bot, get, amt):
        give, amt = str(bot.author), int(amt)
        if getBal(give) >= amt and amt > 0:
            changeBal(give, -1*amt)
            changeBal(get, amt)
            await bot.channel.send(f'{bot.author.mention}, you have successfully given `{get}` ${amt}')
        elif amt < 0:
            await bot.channel.send(f'***BROKE***: {bot.author.mention}, you have unsuccessfully tried to rob this mans `{get}`. What\'s wrong with you bro?')
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
