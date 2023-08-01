# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from order_parser import for_testing as order
import re
from enum import Enum
import venmo
import json
import asyncio

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
emoji_unmapping = {
    '1️⃣':1,
    '2️⃣':2,
    '3️⃣':3,
    '4️⃣':4,
    '5️⃣':5,
    '6️⃣':6,
    '7️⃣':7,
    '8️⃣':8,
    '9️⃣':9,
    '🔟':10,
}

@bot.event
async def on_ready():
    print("hello world")
    #channel = bot.get_channel(test_channel)
    #await channel.send("Happy 4th of July")

@bot.command()
async def hi(ctx):
    await ctx.send("hello!")

@bot.command()
async def who_got_what(ctx):
    i=1
    message = ""
    for item in order["items"]:#builds a message from all the items names+deetails fromt eh order dict in order_parser.py
        #print(' '.join(item["detail"]))
        details = " ".join(item["detail"])
        print(item["name"], details)
        message += (item["name"] + ": " + details + emoji_mapping[i] + " \n")
        i= i+1
    i=1
    sent = await ctx.send(message)
    global oder_message
    oder_message = sent.id
    for item in order["items"]:#adds a reaction for each item in the oder (currently maxes at 10 items)
        await sent.add_reaction(emoji_mapping[i])
        i = i+1


@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:#prevent bot from triggering event
        return
    if reaction.message.author != bot.user:
        return
    print("flag")
    item_name = order["items"][(emoji_unmapping[reaction.emoji])-1]["name"]#get the item the user ordered

    #get the amount
    my_price = order["items"][(emoji_unmapping[reaction.emoji])-1]["price"]
    subtotal = order["subtotal"]
    my_portion = my_price/subtotal
    my_tip = round(my_portion*order["tip"], 2)
    my_fee = round(my_portion*order["fee"], 2)
    my_total = round( (my_price*.0625) + my_tip + my_fee, 2)#get the price of that item + tax + tip + fee
    print(my_price)
    print(my_tip)
    print(my_fee)
    print(my_total)
    await user.send("you ordered: " + item_name)#tell the user what they ordered
    print(user)

    #get the users venmo name
    f = open('venmo_names.JSON')# Opening JSON file
    # returns JSON object as a dictionary
    names_dict = json.load(f)
    if(str(user) in names_dict):
        if(venmo.request_money(names_dict[str(user)], my_total)):
            await user.send("Venmo payment for "+ item_name + " has been sent")
        else:
            await user.send("the username we have on file for you is invalid please re-run !vname {venmo username} ensure proper casing")
    else:
        await user.send("we don't have your venmo username on file please what is you venmo username (ensure proper casing) and rereact to the food item again")
        ctx = await bot.get_context(reaction.message)
        ctx.command = bot.get_command("vname")
        ctx.author = user
            
        def check(m):
            return m.content.lower()
        try:
            response = await bot.wait_for('message', check=check, timeout=60)  # Waits for 60 seconds for the response
            print(response.content.lower())
        except asyncio.TimeoutError:
            await user.send(f"Sorry, you took too long to respond. Run !check_if_group_order to be prompted again" )
        print("invoking vname")
        await vname(ctx, response.content)
        f = open('venmo_names.JSON')
        names_dict = json.load(f)
        if(str(user) in names_dict):
            if(venmo.request_money(names_dict[str(user)], my_total)):
                await user.send("Venmo payment for "+ item_name + " has been sent")
            else:
                await user.send("the username we have on file for you is invalid please re-run !vname {venmo username} ensure proper casing")
        else:
            print("flag")
            print(names_dict)

@bot.command()
async def vname(ctx, arg):#adds the discord users venmo name keyed to their discord user ID and saves it to the JSON file
    f = open('venmo_names.JSON')# Opening JSON file
    # returns JSON object as a dictionary
    names_dict = json.load(f)
    names_dict[str(ctx.author)] = str(arg)
    print(ctx.author)
    print(" was added with the venmo anme ")
    print(arg)
    print(names_dict)
    with open("venmo_names.json", "w") as f:
        json.dump(names_dict, f)

@bot.command()
async def check_if_group_order(ctx, owner_id = 241376328278999041):#DMs Grubhub owner if this is a group meal
    user = await bot.fetch_user(owner_id)
    await user.send("Is the most recent Grubhub order a group Meal")
    def check(m):
        return m.author.id == owner_id and m.content.lower()
    
    try:
        response = await bot.wait_for('message', check=check, timeout=60)  # Waits for 60 seconds for the response
        await ctx.send(f"{user.name} answered: {response.content.lower()}")
    except asyncio.TimeoutError:
        await user.send(f"Sorry, you took too long to respond. Run !check_if_group_order to be prompted again" )

    if response.content.lower() == "yes":#invoke the who got what
        command = bot.get_command('who_got_what')  # Get the command object for !hi
        channel = bot.get_channel(test_channel)
        ctx.channel = channel
        ctx.command = command  # Set the command in the context
        await bot.invoke(ctx)  # Invoke the !hi command


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
