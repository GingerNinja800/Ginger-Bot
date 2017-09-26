import discord
from discord.ext import commands
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
import datetime

discordclient = discord.Client()

@discordclient.event
async def on_ready():
    print('Logged in as')
    print(discordclient.user.name)
    print(discordclient.user.id)
    print("-------")
    await discordclient.change_presence(game=discord.Game(name="Type >>Help"))

def AccessSheet():
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(creds)
    knightsheet = client.open("DawnPC Knights").sheet1
    maasheet = client.open("DawnPC Man At Arms").sheet1
    return knightsheet, maasheet

def FindSquire(username):
    knightsheet, maasheet = AccessSheet()
    knightdata = knightsheet.get_all_records()
    maadata = maasheet.get_all_records()

    for knight in knightdata:
        if username in knight["DiscordTag"]:
            KnightPos = knightdata.index(knight)

    KnightMains = []
    for bit in knightdata[KnightPos]:
        if "Main" in bit:
            KnightMains.append(knightdata[KnightPos][bit])
    while '' in KnightMains:
        KnightMains.remove('')

    Canditates = {}
    for Main in KnightMains:
        for loop in range(1,4):
            for Maa in maadata:
                Maalist = list(Maa.values())
                if Main == Maalist[loop]:
                    Canditates[Maalist[0]] = Maalist[1:]


    Matches = {}
    for Canditate in Canditates:
        Match = set(KnightMains) & set(Canditates[Canditate])
        Matches[Canditate] = len(Match)

    Squire = max(Matches, key=Matches.get)

    return(Squire)


def FindKnight(username):
    knightsheet, maasheet = AccessSheet()
    knightdata = knightsheet.get_all_records()
    maadata = maasheet.get_all_records()

    for maa in maadata:
        if username in maa["DiscordTag"]:
            maaPos = maadata.index(maa)

    maaMains = []
    for bit in maadata[maaPos]:
        if "Main" in bit:
            maaMains.append(maadata[maaPos][bit])
    while '' in maaMains:
        maaMains.remove('')

    Canditates = {}
    for Main in maaMains:
        for loop in range(1,5):
            for Knight in knightdata:
                Knight = list(Knight.values())
                if Knight[1] == "TRUE":
                    if Main == Knight[loop]:
                        Canditates[Knight[0]] = Knight[2:]
            

    Matches = {}
    for canditate in Canditates:
        Match = set(maaMains) & set(Canditates[canditate])
        Matches[canditate] = len(Match)
    KnightTeacher = max(Matches, key=Matches.get)

    return(KnightTeacher)

def AddToSheet(name, role, discrim, mains):
    knightsheet, maasheet = AccessSheet()
    if role == "Man At Arms":
        try:
            if len(mains) > 0:
                ColA = maasheet.col_values(1)
                ColA.remove(ColA[0])
                for cell in ColA:
                    cell2 = cell.split("#")
                    if discrim in cell2[1]:
                        Row = ColA.index(cell)
                        Row += 2
                        break
             
                counter = 0
                maasheet.update_cell(Row,1,name)
                for cell in range(2,2+len(mains)):
                    maasheet.update_cell(Row,cell,mains[counter])
                    if counter != len(mains):
                        counter += 1
                return "1"
            else:
                ColA = maasheet.col_values(1)
                ColA.remove(ColA[0])
                for cell in ColA:
                    cell2 = cell.split("#")
                    if discrim in cell2[1]:
                        Row = ColA.index(cell)
                        Row += 2
                        break
                return

        except:
            if len(mains) > 0:
                TotalRowCount = (maasheet.row_count) + 1
                maasheet.insert_row("", index=TotalRowCount)
                maasheet.update_cell(TotalRowCount, 1, name)
                counter = 0
                for cell in range(2,2+len(mains)):
                    maasheet.update_cell(TotalRowCount,cell,mains[counter])
                    counter += 1
                return "1"
            else:
                TotalRowCount = (maasheet.row_count) + 1
                maasheet.insert_row("", index=TotalRowCount)
                maasheet.update_cell(TotalRowCount, 1, name)
                return "1"

    elif role == "Knight":
        try:
            if len(mains) > 0:
                ColA = knightsheet.col_values(1)
                ColA.remove(ColA[0])
                for cell in ColA:
                    cell2 = cell.split("#")
                    if discrim in cell2[1]:
                        Row = ColA.index(cell)
                        Row += 2
                        break
              
                counter = 0
                knightsheet.update_cell(Row,1,name)
                for cell in range(2,2+len(mains)):
                    knightsheet.update_cell(Row,cell,mains[counter])
                    if counter != len(mains):
                        counter += 1
                return "1"
            else:
                ColA = knightsheet.col_values(1)
                ColA.remove(ColA[0])
                for cell in ColA:
                    cell2 = cell.split("#")
                    if discrim in cell2[1]:
                        Row = ColA.index(cell)
                        Row += 2
                        break
                print(row)
                return

        except:
            if len(mains) > 0:
                TotalRowCount = (knightsheet.row_count) + 1
                knightsheet.insert_row("", index=TotalRowCount)
                knightsheet.update_cell(TotalRowCount, 1, name)
                counter = 0
                for cell in range(2,2+len(mains)):
                    knightsheet.update_cell(TotalRowCount,cell,mains[counter])
                    if counter != len(mains):
                        counter += 1
                return "1"
            else:
                TotalRowCount = (knightsheet.row_count) + 1
                knightsheet.insert_row("", index=TotalRowCount)
                knightsheet.update_cell(TotalRowCount, 1, name)
                return "1"
    else:
        return

@discordclient.event
async def on_message(message):
    if message.author.name != "Ginger Bot":
        username = message.author.name
        if message.content.startswith("!FindKnight"):
            try:
                Knight = FindKnight(username)
                await discordclient.send_message(message.channel, Knight)
            except:
                await discordclient.send_message(message.channel,"Sorry there was an error")

        elif message.content.startswith("!FindSquire"):
            try:
                squire = FindSquire(username)
                await discordclient.send_message(message.channel, squire)
            except:
                await discordclient.send_message(message.channel, "Sorry there was an error")
        elif message.content.startswith(">>Help"):
            await discordclient.send_message(message.channel, "!FindSquire : Suggests the most worthy MaA for your knightliness\n!FindKnight : Suggests the most suitable knight for your squireship\n!AddMe : Adds you to the relevant spreadsheet")

        elif message.content.startswith("!AddMe"):
           username += "#" + message.author.discriminator
           discrim = message.author.discriminator
           AcceptMains = ["True","False","Warden","Conqueror","Peacekeeper","Lawbringer","Centurion","Gladiator","Raider","Warlord","Berzerker","Valkyrie","Highlander","Kensei","Shugoki","Orochi","Nobushi","Shinobi"]
           ManAtArms = discord.utils.get(message.author.roles, name="Man At Arms")
           ManAtArms = str(ManAtArms)
           Knight = discord.utils.get(message.author.roles, name="Knight")
           Knight = str(Knight)
           mains = message.content.split(" ")
           mains.remove(mains[0])
           validated = []
           for pos in range(len(mains)):
               if (mains[pos].title() in AcceptMains) or (mains[pos] in "N/A"):
                    if mains[pos] in AcceptMains[:1]:
                        if validated[0] not in AcceptMains[:1]:
                            validated.append(mains[pos])
                        
                    elif mains[pos] in AcceptMains[2:]:
                        if len(validated) >= 1:
                            validated.append(mains[pos])
                        else:
                            validated.append("")
                            validated.append(mains[pos])
                    else:
                        validated.append("")
                        
                         
           mains = validated
           
           

           if ManAtArms != "None":
               none = AddToSheet(username, ManAtArms, discrim,mains)
           elif Knight != "None":
               none = AddToSheet(username, Knight, discrim,mains)
           if none == None:
               await discordclient.send_message(message.channel, "You're already in the spreadsheet.")
           else:
               await discordclient.send_message(message.channel, "Success!")
        
        elif message.content.startswith("!PromoteMe"):
           joindate = str(message.author.joined_at).split(" ")[0]
           todaydate = datetime.date.today()
           JoinDate2 = joindate
           joindate = joindate.split("-")
           
           joindate = datetime.date(int(joindate[0]),int(joindate[1]),int(joindate[2]))
            print(joindate)
           difference = str(todaydate - joindate).split()[0]
           if int(difference) >= 7:
               await discordclient.remove_roles(message.author, discord.utils.get(message.server.roles, name="Recruit"))
               await discordclient.add_roles(message.author, discord.utils.get(message.server.roles, name="Man At Arms"))
               await discordclient.send_message(message.channel,"Congratulations, you're now a Man At Arms. Do !AddMe to add yourself to the database to aid in squiring")
           else:
               await discordclient.send_message(message.channel,"You joined "+JoinDate2+". You must wait "+difference+" days before you can become a Man At Arms. #SorryNotSorry")

discordclient.run('MzM2MTI4OTc3MzA1NDY4OTI4.DIR5cA.SVdKgvWIgkqw2zzTtyrL9RBAB54')
