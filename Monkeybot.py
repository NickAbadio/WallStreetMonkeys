import os
import discord
import json
from discord import user
from dotenv import load_dotenv
 
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


#updates the servers.json file with new data
def UpdateJson(users):
    with open("servers.json","w") as f:
        json.dump(users, f, indent=2)
        print("Updated servers.json")

#adds xp to users based on certian perams

def AddXP(users, id, XPRate):
    xp = users[str(id)]["XP"] #gets current xp from the user
    needed = users[str(id)]["neededXP"] #gets current needed xp till next level up
    level = users[str(id)]["level"] #gets current users level
    print(xp)
    print(XPRate)

    users[str(id)]["XP"] = xp+XPRate
    

    if((needed-XPRate) <= 0): #checks if a level up is requried else just subtracts from from neededXP
        users[str(id)]["level"] = level + 1
        users[str(id)]["neededXP"] = 20*(level + 1)
    else:
        users[str(id)]["neededXP"] = needed - XPRate


   





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
    
    
    

@client.event       
async def on_message(message): #on a new message in discord chat this is called

    print(message)
    if message.author == client.user: #if the message comes from the bot ignore
        return

    elif (message.content.startswith('$User')): #command to print user info 
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
    else:   #command to add xp if the user command wasnt called and update the json
        AddXP(users, message.author.id, channelXPRates[str(message.channel)])
        UpdateJson(users)
        await message.channel.send(":eagle:")



    

client.run(TOKEN)