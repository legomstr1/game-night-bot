# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from order_parser import order
import re
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
test_channel = 1117516004709367878
client = discord.Client(intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("hello world")
#    channel = bot.get_channel(test_channel)
#    await channel.send("hello world")

@bot.command()
async def hi(ctx):
    await ctx.send("hello!")

@bot.command()
async def who_got_what(ctx):
    for item in order["items"]:
        meal = item["name"], item["detail"]
        print(item["name"], item["detail"])
        await ctx.send(meal)


@client.event
async def on_reaction_add(reaction, user):
    print("flag")
    await reaction.send("flag")
    

'''
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
'''

bot.run(TOKEN)
