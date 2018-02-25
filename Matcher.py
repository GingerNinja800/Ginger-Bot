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
    #await discordclient.change_presence(game=discord.Game(name="Type >>Help"))


def AccessSheet():
    scope = ["https://spreadsheets.google.com/feeds"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
    client = gspread.authorize(creds)
    knightsheet = client.open("THS Members").get_worksheet(2)
    maasheet = client.open("THS Members").get_worksheet(1)
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
        for loop in range(1, 4):
            for Maa in maadata:
                Maalist = list(Maa.values())
                if Main == Maalist[loop]:
                    Canditates[Maalist[0]] = Maalist[1:]

    Matches = {}
    for Canditate in Canditates:
        Match = set(KnightMains) & set(Canditates[Canditate])
        Matches[Canditate] = len(Match)

    Squire = max(Matches, key=Matches.get)

    return (Squire)


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
        for loop in range(1, 5):
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

    return (KnightTeacher)


def FindMe(sheet,discrim):
    ColA = sheet.col_values(1)
    ColA.remove(ColA[0])
    for cell in ColA:
        cell2 = cell.split("#")
        if discrim in cell2[1]:
            Row = ColA.index(cell)
            Row += 2
    try:
        return Row
    except:
        return

def AddToSheet(name, sheet, discrim, mains):
    present, row = InSheet(sheet,discrim)
    if present:
        if len(mains) == 0:
            return
        else:
            counter = 2
            for main in mains:
                sheet.update_cell(row,counter,main)
                counter += 1
                if counter > 4:
                    break
            return "1"

    else:
        Row = sheet.row_count + 1
        sheet.insert_row("",index=Row)
        sheet.update_cell(Row,1,name)
        if len(mains) == 0:
            return "1"
        else:
            counter = 2
            for main in mains:
                sheet.update_cell(row, counter, main)
                counter += 1
                if counter > 4:
                    break
            return "1"


def InSheet(sheet,discrim):
    TagCol = sheet.col_values(1)
    for Tag in TagCol[1:]:
        row = TagCol.index(Tag) + 1
        if discrim in Tag:
            return True, row
    return False, None



def TransferData(name,discrim):
    knightsheet, maasheet = AccessSheet()
    Row = FindMe(maasheet,discrim)
    if Row == None:
        return
    else:
        RowValues = maasheet.row_values(Row)
        RowValues.insert(1,"")
        maasheet.delete_row(Row)

        present = FindMe(knightsheet,discrim)
        print(present)
        if present == None:
            TotalRowCount = (knightsheet.row_count)+1
            knightsheet.insert_row(RowValues,index = TotalRowCount)
            return "1"
        else:
            for cell in range(3,3+len(RowValues)):
                knightsheet.update_cell(present,cell,RowValues[cell-1])
            return "1"


def Squiring(Finding,squiring,discrim):
        knightsheet, maasheet = AccessSheet()
        Row = FindMe(knightsheet,discrim)
        if Finding == "?":
            if Row == None:
                return
            else:
                return (knightsheet.row_values(Row)[1])
        elif Finding == "!":
            knightsheet.update_cell(Row,2,squiring)
            return

def next_available_row(worksheet,column):
    str_list = list(filter(None, worksheet.col_values(column)))
    return str(len(str_list)+1)

def FindMains(role,discrim):
    knightsheet, maasheet = AccessSheet()
    if role == "Man At Arms":
        Row = FindMe(maasheet,discrim)
        if Row == None:
            return
        else:
            RowValues = maasheet.row_values(Row)
            RowValues = RowValues[1:]
            return RowValues

    elif role == "Knight":
        Row = FindMe(knightsheet,discrim)
        if Row == None:
            return
        else:
            RowValues = knightsheet.row_values(Row)
            RowValues = RowValues[1:]
            return RowValues

@discordclient.event
async def on_message(message):
    if message.author.name != "Ginger Bot":
        username = message.author.name
        discrim = message.author.discriminator
        if message.content.startswith("!FindKnight"):
            try:
                Knight = FindKnight(username)
                await discordclient.send_message(message.channel, Knight)
            except:
                await discordclient.send_message(message.channel, "Sorry there was an error")

        elif message.content.startswith("!FindSquire"):
            try:
                squire = FindSquire(username)
                await discordclient.send_message(message.channel, squire)
            except:
                await discordclient.send_message(message.channel, "Sorry there was an error")
        elif message.content.startswith(">>Help"):
            await discordclient.send_message(message.channel,
                                             "!FindSquire : Suggests the most worthy MaA for your knightliness\n!FindKnight : Suggests the most suitable knight for your squireship\n!AddMe : Adds you to the relevant spreadsheet")

        elif message.content.startswith("!AddMe"):
            username += "#" + message.author.discriminator
            AcceptMains = ["True", "False", "Warden", "Conqueror", "Peacekeeper", "Lawbringer", "Centurion",
                           "Gladiator", "Raider", "Warlord", "Berzerker", "Valkyrie", "Highlander", "Kensei", "Shugoki",
                           "Orochi", "Nobushi", "Shinobi","Shaman","Aramusha"]





            mains = message.content.split(" ")
            mains.remove(mains[0])
            validated = []
            for pos in range(len(mains)):
                if (mains[pos].title() in AcceptMains[2:]):
                    validated.append(mains[pos])

            mains = validated

            knightsheet, maasheet = AccessSheet()

            if discord.utils.get(message.author.roles, name = "Man At Arms") == "Man At Arms":
                none = AddToSheet(username, maasheet, discrim, mains)
            else:
                none = AddToSheet(username, knightsheet, discrim, mains)

            if none == None:
                await discordclient.send_message(message.channel, "You're already in the spreadsheet.")
            else:
                await discordclient.send_message(message.channel, "Success!")

        elif message.content.startswith("!PromoteMe"):
            if str(discord.utils.get(message.author.roles, name = "Recruit")) == "Recruit":
                joindate = str(message.author.joined_at).split(" ")[0]
                todaydate = datetime.date.today()
                JoinDate2 = joindate
                joindate = joindate.split("-")

                joindate = datetime.date(int(joindate[0]), int(joindate[1]), int(joindate[2]))
                print(joindate)
                difference = str(todaydate - joindate).split()[0]
                if int(difference)-7 >= 0:
                    ManAtArmsRole = discord.utils.get(message.server.roles, name="Man At Arms")
                    RecruitRole = discord.utils.get(message.server.roles, name="Recruit")
                    await discordclient.remove_roles(message.author, RecruitRole)
                    await discordclient.add_roles(message.author, ManAtArmsRole)
                    await discordclient.send_message(message.channel,
                                                     "Congratulations, you're now a Man At Arms. Do !AddMe to add yourself to the database to aid in squiring")
                else:
                    await discordclient.send_message(message.channel,
                                                     "You joined " + JoinDate2 + ". You must wait " + 7-int(difference) + " days before you can become a Man At Arms. #SorryNotSorry")

            elif str(discord.utils.get(message.author.roles, name = "Knight")) == "Knight":
                Done = TransferData(username,discrim)
                if Done == "1":
                    await discordclient.send_message(message.channel, "You've been transferred to the Knight sheet. Remember to add whether or not you're available to squire")
                elif Done == None:
                    await discordclient.send_message(message.channel, "Error: You're most likely not in the MaA sheet, so just use !AddMe to add yourself to knight sheet if not already there.")

        elif message.content.startswith("!Squiring") or message.content.startswith("?Squiring"):
            if str(discord.utils.get(message.author.roles, name = "Knight")) == "Knight":
                userinput = message.content.split(" ")
                finding = userinput[0][0]
                if finding == "!":
                    userinput.remove(userinput[0])
                    if userinput[0].title() in ["True","False","N/A"]:
                        squiring = userinput[0].title()
                        Squiring(finding,squiring,discrim)
                        await discordclient.send_message(message.channel, "Done.")
                elif finding == "?":
                    squireless = Squiring(finding,"",discrim)
                    await discordclient.send_message(message.channel, "You're current status is: "+squireless)
         
        elif message.content.startswith("?Mains"):
            role = str(discord.utils.get(message.author.roles,name = "Man At Arms"))
            if role == 'None':
                role = str(discord.utils.get(message.author.roles, name = "Knight"))
                if role == 'None':
                    await discordclient.send_message(message.channel, "This command is only available to Man At Arms and Knights, sorry")


            mains = FindMains(role,discrim)
            if mains != None:
                await discordclient.send_message(message.channel,"Your current mains are: "+" ".join(mains))
       
        elif message.content.startswith("!UpdateMemberList"):
            Roles = ["Recruit","Man At Arms","Squire","Knight","Cavalry","Bannerman","Under-Marshal","Marshal"]
            scope = ["https://spreadsheets.google.com/feeds"]
            creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
            client = gspread.authorize(creds)
            DawnPCSheet = client.open("THS Members").sheet1
            if str(discord.utils.get(message.author.roles,name = "Dawn Knight Commander")) != "Dawn Knight Commander":
                await discordclient.send_message(message.channel, "Leadership only for this command, sorry lads")
            else:
                for person in discordclient.get_all_members():
                    if str(discord.utils.get(person.roles, name= "FH Dawn PC")) == "FH Dawn PC":
                        for rank in Roles:
                            if str(discord.utils.get(person.roles, name= rank)) == "Recruit":
                                Row = next_available_row(DawnPCSheet,1)
                                DawnPCSheet.update_acell("A{}".format(Row),str(person))
                            if str(discord.utils.get(person.roles, name=rank)) == "Man At Arms":
                                Row = next_available_row(DawnPCSheet, 2)
                                DawnPCSheet.update_acell("B{}".format(Row),str(person))
                            if str(discord.utils.get(person.roles, name=rank)) == "Squire":
                                Row = next_available_row(DawnPCSheet, 3)
                                DawnPCSheet.update_acell("C{}".format(Row),str(person))

                            if str(discord.utils.get(person.roles, name=rank)) == "Knight":
                                Row = next_available_row(DawnPCSheet, 4)
                                DawnPCSheet.update_acell("D{}".format(Row), str(person))

                            if str(discord.utils.get(person.roles, name=rank)) == "Cavalry":
                                Row = next_available_row(DawnPCSheet, 6)
                                DawnPCSheet.update_acell("F{}".format(Row), str(person))

                            if str(discord.utils.get(person.roles, name="Cavalry")) == "None" and str(discord.utils.get(person.roles, name=rank)) == "Knight":
                                Row = next_available_row(DawnPCSheet, 5)
                                DawnPCSheet.update_acell("E{}".format(Row), str(person))

                            if str(discord.utils.get(person.roles, name=rank)) == "Bannerman":
                                Row = next_available_row(DawnPCSheet, 7)
                                DawnPCSheet.update_acell("G{}".format(Row), str(person))

                            if str(discord.utils.get(person.roles, name=rank)) == "Under-Marshal":
                                Row = next_available_row(DawnPCSheet, 8)
                                DawnPCSheet.update_acell("H{}".format(Row), str(person))

                            if str(discord.utils.get(person.roles, name=rank)) == "Marshal":
                                Row = next_available_row(DawnPCSheet, 9)
                                DawnPCSheet.update_acell("I{}".format(Row), str(person))

                await discordclient.send_message(message.channel,"All Members added.")

#discordclient.run('MzM2MTI4OTc3MzA1NDY4OTI4.DIR5cA.SVdKgvWIgkqw2zzTtyrL9RBAB54')
discordclient.run("MzE1NDc3NzU5NjA0NTU1Nzg2.DXOSoQ.G2F7LlhxEzyoq06Ft7G73e-aI8c")
