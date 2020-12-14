from discord.ext import commands as cmd
import glob as match
import discord
import os
from games.Blackjack import Blackjack

pysino = cmd.Bot(command_prefix='*')

#Initialize Users Directory
if not os.path.exists('users'):
    os.mkdir('users')

#Load Cogs
for cog in match.glob('util/*.py'):
    pysino.load_extension(f'util.{cog[5:-3]}')

#Initialize Games
blackjack = Blackjack()

@pysino.event
async def on_ready():
    print('\n'*5+'Pysino Fully Initialized'+'\n'*5)
    await pysino.change_presence(activity=discord.Game('with $$$ - Use: *'))

@pysino.command(help='Register a new account within the Pysino Database.')
async def register(bot):
    if not os.path.exists(f'users/{str(bot.author)}.txt'):
        user = str(bot.author)
        file = open(f'users/{user}.txt','w')
        file.write('$50') # base balance to play any games
        file.close()
        await bot.channel.send(f'Thank you for registering {bot.author.mention}! I have given you a $50 starting balance to play.')
    else:
        await bot.channel.send(f'{bot.author.mention}, you are already registered with our system!')

@pysino.command(help='Start a game based on the current channel you are in')
async def play(bot):
    if os.path.exists(f'users/{str(bot.author)}.txt'):
        if bot.channel.name == 'blackjack':
            await blackjack.play(pysino, bot)
    else:
        await bot.channel.send(f'{bot.author.mention}, please register with our database before you play any games! Please use `*register`.')

pysino.run('<BOT-KEY>')