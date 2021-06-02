import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    
    guild = client.get_guild(849714682804961301)
    memberlist = guild.members
    for member in memberlist:
        print(member)

@client.event       
async def on_message(message):
    print(message)
    if message.author == client.user:
        return
    await message.channel.send("test")
    
       
client.run(TOKEN)