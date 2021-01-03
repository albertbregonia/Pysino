from discord.ext import commands as cmd
import glob as match
import discord
import os
from games.Blackjack import Blackjack
from games.Roulette import Roulette
import util.ErrorHandler as e

pysino = cmd.Bot(command_prefix='*')

#Initialize Users Directory
if not os.path.exists('users'):
    os.mkdir('users')

#Load Cogs
for cog in match.glob('cogs/*.py'):
    pysino.load_extension(f'cogs.{cog[5:-3]}')

#Initialize Games
blackjack = Blackjack()
roulette = Roulette()

@pysino.event
async def on_ready():
    print('\n'*5+'Pysino Fully Initialized'+'\n'*5)
    await pysino.change_presence(activity=discord.Game('with $$$ - Use: *'))

@pysino.command(help='Setup function to register Pysino with the current discord server')
async def setup(bot):
    path = f'users/{bot.guild.name}/'
    if not os.path.exists(path):
        os.mkdir(path)
        games = ['blackjack','roulette']
        for game in games:
            await bot.message.guild.create_text_channel(game)
        await bot.channel.send(f'{bot.author.mention}, setup successful.')
    else:
        await bot.channel.send(f'{bot.author.mention}, setup has already been completed.')

@pysino.command(help='Register a new account within the Pysino Database.')
async def register(bot):
    user = str(bot.author)
    if not os.path.exists(f'users/{bot.guild.name}/{user}.txt'):
        with open(f'users/{user}.txt','w') as file:
            file.write('$50') #base balance to play any games
        await bot.channel.send(f'Thank you for registering {bot.author.mention}! I have given you a $50 starting balance to play.')
    else:
        await bot.channel.send(f'{bot.author.mention}, you are already registered with our system!')

@pysino.command(help='Start a game based on the current channel you are in')
async def play(bot):
    error = e.fullSetup(f'users/{bot.guild.name}/', f'users/{bot.guild.name}/{str(bot.author)}.txt')
    if error == 'full':
        if bot.channel.name == 'blackjack':
                await blackjack.play(pysino, bot)
        elif bot.channel.name == 'roulette':
            await roulette.play(pysino, bot)
    else:
        await bot.channel.send(f'{bot.author.mention}{error}')

@pysino.command(help='See the tutorial for the current game channel you are in.')
async def how2(bot):
    if bot.channel.name == 'blackjack':
        await bot.channel.send(blackjack.tutorial())
    elif bot.channel.name == 'roulette':
        await bot.channel.send(roulette.tutorial())

pysino.run('Nzg2Nzc2MDEyNDU2NzIyNDcy.X9LUQg.tNtJGow-MMfGHTJ41ui6d_dYyoE')