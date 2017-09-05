import discord
from discord.ext import commands
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint


discordclient = discord.Client()

@discordclient.event
async def on_ready():
    print('Logged in as')
    print(discordclient.user.name)
    print(discordclient.user.id)
    print("-------")
    await discordclient.change_presence(game=discord.Game(name="Type >>Help"))


def FindSquire(username):
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(creds)
    knightsheet = client.open("DawnPC Knights").sheet1
    maasheet = client.open("DawnPC Man At Arms").sheet1

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
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(creds)
    knightsheet = client.open("DawnPC Knights").sheet1
    maasheet = client.open("DawnPC Man At Arms").sheet1

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
                    if Main == Knight[counter]:
                        Canditates[Knight[0]] = Knight[2:]
            

    Matches = {}
    for canditate in Canditates:
        Match = set(maaMains) & set(Canditates[canditate])
        Matches[canditate] = len(Match)
    KnightTeacher = max(Matches, key=Matches.get)

    return(KnightTeacher)

def AddToSheet(name,role):
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(creds)
    knightsheet = client.open("DawnPC Knights").sheet1
    maasheet = client.open("DawnPC Man At Arms").sheet1
    if role == "Man At Arms":
        try:
            cell = maasheet.find(name)
            return "1"
        except:
            TotalRowCount = (maasheet.row_count) + 1
            maasheet.insert_row("", index=TotalRowCount)
            maasheet.update_cell(TotalRowCount, 1, name)
    elif role == "Knight":
        try:
            cell = knightsheet.find(name)
            return
        except:
            TotalRowCount = (knightsheet.row_count)+1
            knightsheet.insert_row("",index=TotalRowCount)
            knightsheet.update_cell(TotalRowCount,1,name)
            return "1"

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
            username += "#"+message.author.discriminator
            ManAtArms = discord.utils.get(message.author.roles,name="Man At Arms")
            ManAtArms = str(ManAtArms)
            Knight = discord.utils.get(message.author.roles,name="Knight")
            Knight = str(Knight)
            if ManAtArms != "None":
                none = AddToSheet(username,ManAtArms)
            elif Knight != "None":
                none = AddToSheet(username,Knight)
            if none == None:
                await discordclient.send_message(message.channel, "YOU'RE ALREADY THERE YA DIP. (Or Ginger is a Dip if you aren't)")
            else:
                await discordclient.send_message(message.channel,"Success!")

discordclient.run('MzM2MTI4OTc3MzA1NDY4OTI4.DIR5cA.SVdKgvWIgkqw2zzTtyrL9RBAB54')
