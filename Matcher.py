import discord
from discord.ext import commands
import asyncio
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint

scope = ["https://spreadsheets.google.com/feeds"]
creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
client = gspread.authorize(creds)

discordclient = discord.Client()

@discordclient.event
async def on_ready():
    print('Logged in as')
    print(discordclient.user.name)
    print(discordclient.user.id)
    print("-------")
    await discordclient.change_presence(game=discord.Game(name="Type >>Help"))


def FindSquire(username):
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

    counter = 1

    Canditates = {}
    for Main in KnightMains:
        if len(Canditates) == 0:
            for Maa in maadata:
                Maa = list(Maa.values())
                if Main == Maa[counter]:
                    Canditates[Maa[0]] = Maa[1:]
            counter += 1

    Matches = {}
    for Canditate in Canditates:
        Match = set(KnightMains) & set(Canditates[Canditate])
        Matches[Canditate] = len(Match)

    Squire = max(Matches, key=Matches.get)

    return Squire


def FindKnight(username):
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

    counter = 2
    Canditates = {}
    for Main in maaMains:
        if len(Canditates) == 0:
            for Knight in knightdata:
                Knight = list(Knight.values())
                if Knight[1] == "TRUE":
                    if Main == Knight[counter]:
                        Canditates[Knight[0]] = Knight[2:]
            counter += 1

    Matches = {}
    for canditate in Canditates:
        Match = set(maaMains) & set(Canditates[canditate])
        Matches[canditate] = len(Match)
    KnightTeacher = max(Matches, key=Matches.get)

    return KnightTeacher



@discordclient.event
async def on_message(message):
    if message.content.startswith("!FindKnight"):
        username = message.author.name
        Knight = FindKnight(username)
        await discordclient.send_message(message.channel, Knight)

    elif message.content.startswith("!FindSquire"):
        username = message.author.name
        Squire = FindSquire(username)
        await discordclient.send_message(message.channel, Squire)

    elif message.content.startswith(">>Help"):
        await discordclient.send_message(message.channel, "!FindSquire : Suggests the most worthy MaA for your knightliness\n!FindKnight : Suggests the most suitable knight for your squireship")



discordclient.run('MzM2MTI4OTc3MzA1NDY4OTI4.DIR5cA.SVdKgvWIgkqw2zzTtyrL9RBAB54')