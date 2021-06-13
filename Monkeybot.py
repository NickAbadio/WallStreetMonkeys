import os
import discord
import json
from dotenv import load_dotenv
 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
users = {}

@client.event
async def on_ready():
    
    

    guild = client.get_guild(849714682804961301)
    memberlist = guild.members
    for member in memberlist:
        if member not in users:
            users[str(member.id)] = {
                "level": 1,
                "XP": 0,
                "neededXP": 10,
            }
    print(users)
    with open('servers.json','w') as f:
        json.dump(users, f, indent=2)


@client.event       
async def on_message(message):
    print(message)
    if message.author == client.user:
        return
    else:
        await message.channel.send(":eagle:")

    
       
client.run(TOKEN)