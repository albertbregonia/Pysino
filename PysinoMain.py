from discord.ext import commands as cmd
import discord
import os
import games.blackjack as blackjack

print('\n'*5)
pysino = cmd.Bot(command_prefix='>')

if not os.path.exists('users'):
    os.mkdir('users')

@pysino.event
async def on_ready():
    await pysino.change_presence(activity=discord.Game('with $$$ - Use: >'))

@pysino.command(help='Register a new account within the Pysino.')
async def register(bot):
    user = str(bot.author)
    file = open(f'{user}.dat','w')
    file.write('$50') # base balance to play any games
    file.close()

@pysino.command(help='Start a game based on the current channel you are in')
async def start(bot):
    if bot.channel.name == 'blackjack':
        await blackjack.start(pysino, bot)


pysino.run('<BOT-KEY>')