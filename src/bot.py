# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from order_parser import order
import re
from enum import Enum
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
test_channel = 1117516004709367878
client = discord.Client(intents=discord.Intents.all())

emoji_mapping = {
    1:'1️⃣',
    2:'2️⃣',
    3:'3️⃣',
    4:'4️⃣',
    5:'5️⃣',
    6:'6️⃣',
    7:'7️⃣',
    8:'8️⃣',
    9:'9️⃣',
    10:'🔟',
}

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
    i=1
    message = ""
    for item in order["items"]:
        #print(' '.join(item["detail"]))
        details = " ".join(item["detail"])
        print(item["name"], details)
        message += (item["name"] + ": " + details + emoji_mapping[i] + " \n")
        i= i+1
    sent = await ctx.send(message)
    for item in order["items"]:
        await sent.add_reaction(emoji_mapping[i])
        i = i+1


@bot.event
async def send_reaction(ctx, message):
    print("flag")



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
