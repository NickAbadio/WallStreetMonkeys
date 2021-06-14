import os
import discord
import json
from discord import user
from dotenv import load_dotenv
 
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all()
client = discord.Client(intents=intents)
users = {}

#loads initial users dictionary is json data from servers.json
with open("servers.json") as f:
    users = json.load(f)


#updates the servers.json file with new data
def UpdateJson(users):
    with open("servers.json","w") as f:
        json.dump(users, f, indent=2)
        print("Updated servers.json")


def AddXP(users, id):
    xp = users[str(id)]["XP"]
    needed = users[str(id)]["neededXP"]
    level = users[str(id)]["level"]
    users[str(id)]["XP"] = xp+1
    

    if((needed-1) == 0):
        users[str(id)]["level"] = level + 1
        users[str(id)]["neededXP"] = 20*(level + 1)
    else:
        users[str(id)]["neededXP"] = needed - 1


    #print(users)





@client.event
async def on_ready():   
    guild = client.get_guild(849714682804961301)
    memberlist = guild.members
    for member in memberlist:
        print(users.keys())
        if str(member.id) not in users.keys():
            users[str(member.id)] = {
                "level": 1,
                "XP": 0,
                "neededXP": 10,
            }
    
    
    

@client.event       
async def on_message(message):

    print(message)
    if message.author == client.user:
        return

    elif (message.content.startswith('$User')):
        embed = discord.Embed(
        title = message.author,
        description = users[str(message.author.id)]["level"],
        colour = discord.Colour.blue()
        )
        print(message.channel)
        url = message.author.avatar_url
        embed.set_thumbnail(url=url)
        embed.add_field(name='XP', value=users[str(message.author.id)]["XP"], inline=True)
        embed.add_field(name='XP needed', value=users[str(message.author.id)]["neededXP"], inline=True)

        await message.channel.send(embed=embed)
    else:   
        print(message.id)
        AddXP(users, message.author.id)
        UpdateJson(users)
        await message.channel.send(":eagle:")



    

client.run(TOKEN)