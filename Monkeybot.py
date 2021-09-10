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
TOKEN = os.getenv('DISCORD_TOKEN') 
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.all() #gives discord bot the ability to get any info from the server
client = discord.Client(intents=intents)
guild = ""
users = {}
serverInfo = {
    "channelXPRates": {},
    "modChannel": {},
}

#loads initial users dictionary is json data from servers.json
with open("servers.json") as f:
    try:
        users = json.load(f)
    except:
        print("No json save files")
@client.event
async def on_ready():
    global guild   #called on start of bot to make sure all users 
    guild = client.get_guild(820349556860256286) #gets WSM discord id (CURRENTLY USING BOT TESTING CHANNEL NOT WSM)
    memberlist = guild.members #gets a list of all WSM users (CURRENTLY USING BOT TESTING CHANNEL NOT WSM)
    for member in memberlist: 
        AddMemberToJson(member)
       

@client.event
async def on_member_join(member):
    await member.send("welcome")
    AddMemberToJson(member)


#====================================================#
#                   User Functions                   #
#====================================================#

def AddMemberToJson(member):
     if str(member.id) not in users.keys(): #goes through all users and checks if their in the json file if not adds them at level 1
            users[str(member.id)] = {
                "level": 1,
                "XP": 0,
                "neededXP": 10,
            }

            
#updates the servers.json file with new data
def UpdateJson(users):
    with open("servers.json","w") as f:
        json.dump(users, f, indent=2)
        print("Updated servers.json")

def SetChannelXP(message):
     if message.author.guild_permissions.kick_members and message.content.split()[1]:
        try:
            xpRate = float(message.content.split()[1])
            serverInfo["channelXPRates"][str(message.channel.id)] = xpRate
            print(serverInfo)
        except:
            print(message.content)

def CallXPCommands(message):
    if message.channel.id in serverInfo["channelXPRates"]:
            XPCommands.AddXP(users, message.author.id, serverInfo["channelXPRates"][str(message.channel.id)])
    else:
        XPCommands.AddXP(users, message.author.id, 1)
        UpdateJson(users)
        for role in message.author.roles:
            if role.name == "tester":
                print("Role checking working")
                break

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
    embed.add_field(name='Joined:', value=message.author.joined_at, inline=False)
    
    roles = []
    for role in message.author.roles:
        roles.append(role.mention)

    embed.add_field(name='roles', value= "".join(roles[1:]), inline=False)


    return embed

#====================================================#
#                   Discord Message Commands         #
#====================================================#

@client.event       
async def on_message(message): #on a new message in discord chat this is called
    if message.author == client.user: #if the message comes from the bot ignore
        return

    elif (message.content == ("$User")): #command to print user info 
        embed = EmbedUserInfoMessage(message)
        await message.channel.send(embed=embed)


    elif(message.content.startswith("$SetChannel")):
        SetChannelXP(message)


    else:   #command to add xp if the user command wasnt called and update the json
        CallXPCommands(message)

@client.event
async def on_reaction_add(reaction,user):
    if user.guild_permissions.kick_members:
        if "PepeWat" in str(reaction):
            print("is mod emoji")
            print(reaction.message)
            await reaction.message.clear_reaction(str(reaction))
            channel = client.get_channel(880541130125611038)
            await channel.send(guild.get_role(849768254427496478).mention)
    await reaction.message.channel.send(str(reaction))
    
    

    

client.run(TOKEN)