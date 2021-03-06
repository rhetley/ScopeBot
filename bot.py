# Perm Int: 3406912

# Import Libraries / Modules
import discord
import random

import os

# Only import Config.py if the bot is being run locally
# 'HOSTED' is a environment variable set on Heroku that equals the bot token
token = ''
if os.environ.get('HOSTED') == None:
    import config
    token = config.token
else:
    token = str(os.environ.get('HOSTED'))
    print('Running on Heroku, token = ' + token)

import data

# create a Discord client instance
client = discord.Client()

# Helper functions

# Retrieves a quote, and will @ the user if supported by the quote
def GetQuote(usr):
    quote = data.scopebook[random.randint(0,len(data.scopebook)-1)]
    quote = quote.replace('$','<@' + str(usr) + '>')
    return quote

# Check if a message contains a keyword
def ContainsKeyword(msg):
    if any(map(msg.content.lower().__contains__,data.keywords)):
        return True
    
    return False

# Discord Events

# When the bot is successfully logged in
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

# When a message is sent to a channel visible to the bot
@client.event
async def on_message(msg):

    # enforces cooldown on sending scope messages
    if not str(msg.channel.id) in data.cooldowns:
        data.cooldowns[str(msg.channel.id)] = 0
    elif data.cooldowns[str(msg.channel.id)] > 0:
        data.cooldowns[str(msg.channel.id)] -= 1

    # ignore messages sent by the bot
    if msg.author == client.user:
        return
    
    # 'hello' ping
    if msg.content.startswith('$hello'):
        await msg.channel.send('Hello!')

    # send a scope reminder (by using a command, random chance, or by containing a keyword)
    if msg.content.startswith('!scope'):
        await msg.channel.send(GetQuote(msg.author.id))
    elif (random.randint(0,100) <= 5 or ContainsKeyword(msg)) and data.cooldowns[str(msg.channel.id)] == 0:
        data.cooldowns[str(msg.channel.id)] = 10
        await msg.channel.send(GetQuote(msg.author.id))

    
# run the bot
print('Bot online')
client.run(token)