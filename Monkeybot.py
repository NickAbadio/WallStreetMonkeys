import os
import discord
import json
import XPCommands
from discord import user
from dotenv import load_dotenv

#====================================================#
#             Initial loading of the bot             #
#====================================================#

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #gets
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.all() #gives discord bot the ability to get any info from the server
client = discord.Client(intents=intents)
users = {}
channelXPRates = {
    "general": 1,
    "gamers" : 5,
}

#loads initial users dictionary is json data from servers.json
with open("servers.json") as f:
    users = json.load(f)


@client.event
async def on_ready():   #called on start of bot to make sure all users 
    guild = client.get_guild(849714682804961301) #gets WSM discord id (CURRENTLY USING BOT TESTING CHANNEL NOT WSM)
    memberlist = guild.members #gets a list of all WSM users (CURRENTLY USING BOT TESTING CHANNEL NOT WSM)
    for member in memberlist: 
        if str(member.id) not in users.keys(): #goes through all users and checks if their in the json file if not adds them at level 1
            users[str(member.id)] = {
                "level": 1,
                "XP": 0,
                "neededXP": 10,
            }






#====================================================#
#                   User Functions                   #
#====================================================#

#updates the servers.json file with new data
def UpdateJson(users):
    with open("servers.json","w") as f:
        json.dump(users, f, indent=2)
        print("Updated servers.json")


def EmbedUserInfoMessage(message):
    embed = discord.Embed(
        title = message.author, 
        description = users[str(message.author.id)]["level"],
        colour = discord.Colour.blue()
        )
    url = message.author.avatar_url
    embed.set_thumbnail(url=url)
    embed.add_field(name='XP', value=users[str(message.author.id)]["XP"], inline=True)
    embed.add_field(name='XP needed', value=users[str(message.author.id)]["neededXP"], inline=True)

    return embed

        




#====================================================#
#                   Discord Message Commands         #
#====================================================#


@client.event       
async def on_message(message): #on a new message in discord chat this is called

    print(message)
    if message.author == client.user: #if the message comes from the bot ignore
        return

    elif (message.content.startswith('$User')): #command to print user info 
        embed = EmbedUserInfoMessage(message)

        await message.channel.send(embed=embed)


    else:   #command to add xp if the user command wasnt called and update the json
        XPCommands.AddXP(users, message.author.id, channelXPRates[str(message.channel)])
        UpdateJson(users)
        await message.channel.send(":eagle:")



    

client.run(TOKEN)