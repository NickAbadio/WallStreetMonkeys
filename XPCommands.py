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