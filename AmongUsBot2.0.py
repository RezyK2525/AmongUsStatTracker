import discord
from discord.ext import commands
import mysql.connector
import discord.ext

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print("Bot is Ready.")

mydb = mysql.connector.connect(
    host="localhost",
    user="RezyK",
    password="Random",
    database="AmongUsTracker")
print(mydb)
cursor=mydb.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS OverallTracker(userid VARCHAR(20) primary key, username VARCHAR(32), Impwins INT, Implosses INT, Crewwins INT, Crewlosses INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS DailyTracker(userid VARCHAR(20) primary key, username VARCHAR(32), Impwins INT, Implosses INT, Crewwins INT, Crewlosses INT)")


def checkUname(uname):
    if len(uname) < 32:
        return True
    return False

@client.command()
async def create(ctx, member: discord.Member, uname="rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr"):
    if uname == "rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr":
        await ctx.send("Make sure you enter a Username!")
        return 0
    validUname = checkUname(uname)
    if not validUname:
        await ctx.send("Invalid Username!")
        return 0
    else:
        try:
            insert_new_user1 = ("INSERT INTO OverallTracker (userid, username, Impwins, Implosses, Crewwins, Crewlosses) VALUES (%s, %s, %s, %s, %s, %s)")
            insert_new_user2 = ("INSERT INTO DailyTracker (userid, username, Impwins, Implosses, Crewwins, Crewlosses) VALUES (%s, %s, %s, %s, %s, %s)")
            cursor.execute(insert_new_user1, (str(member.id), str(uname), 0, 0, 0, 0))
            cursor.execute(insert_new_user2, (str(member.id), str(uname), 0, 0, 0, 0))
            mydb.commit()
            await ctx.send("Member Added!")
        except:
            await ctx.send("Please try again!")


game_list = []
imp_list = []
imp_win = False

@client.command()
async def join(ctx, member: discord.Member):
    cursor.execute("SELECT * FROM OverallTracker WHERE userid = %s", (member.id,))
    tester=cursor.fetchall()
    if tester == []:
        await ctx.send("User not in database. Use .create to create a user!")
        return 0

    if len(game_list) <= 9:
        game_list.append(member.id)
        await ctx.send("Successfully Joined!")
    else:
        await ctx.send("Game is Full!")


@client.command()
async def leave(ctx, member: discord.Member):
    game_list.remove(member.id)
    await ctx.send("Successfully Removed!")

@client.command()
async def clear(ctx):
    for x in range(0, len(game_list)):
        gameuser = game_list[x]
        cursor.execute(
            "SELECT username, Impwins, Implosses, Crewwins, Crewlosses FROM DailyTracker WHERE userid = %s",
            (gameuser,))
        gamestats = cursor.fetchone()
        await ctx.send(
            "```Username: " + str(gamestats[0]) + "\nImposter Wins: " + str(gamestats[1]) + "\nImposter Losses: " + str(
                gamestats[2]) + "\nCrew Wins: " + str(gamestats[3]) + "\nCrew Losses: " + str(gamestats[4]) + "```")
    game_list.clear()
    await ctx.send("Game has been cleared!")
    cursor.execute("UPDATE DailyTracker SET Impwins = 0, Implosses = 0, Crewwins = 0, Crewlosses = 0")
    mydb.commit()

@client.command()
async def update(ctx, imp1: discord.Member, imp2: discord.Member, WL):
    try:
        imp_list = [imp1.id, imp2.id]
        print(imp1.id)
        print(imp2.id)

        for x in range(0, len(game_list)):
            if game_list[x] == imp_list[0] or game_list[x] == imp_list[1]:
                if WL == "W" or WL == "w":
                    cursor.execute("UPDATE `OverallTracker` SET `Impwins` = (Impwins + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    cursor.execute("UPDATE `DailyTracker` SET `Impwins` = (Impwins + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    mydb.commit()
                elif WL == "L" or WL == "l":
                    cursor.execute("UPDATE OverallTracker SET Implosses = (Implosses + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    cursor.execute("UPDATE DailyTracker SET Implosses = (Implosses + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    mydb.commit()
            else:
                if WL == "L" or WL == "l":
                    cursor.execute("UPDATE OverallTracker SET Crewwins = (Crewwins + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    cursor.execute("UPDATE DailyTracker SET Crewwins = (Crewwins + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    mydb.commit()
                elif WL == "W" or WL == "w":
                    cursor.execute("UPDATE OverallTracker SET Crewlosses = (Crewlosses + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    cursor.execute("UPDATE DailyTracker SET Crewlosses = (Crewlosses + 1) WHERE `userid` = %s",
                                   (game_list[x],))
                    mydb.commit()
    except:
        await ctx.send("Please input a valid argument!")


@client.command()
async def stats(ctx, statistics):
    if statistics[0] == "<":
        ussser = ""
        for i in range(3, 21):
            ussser += statistics[i]
        cursor.execute("SELECT * FROM OverallTracker WHERE userid = %s", (ussser,))
        tester = cursor.fetchall()
        if tester == []:
            await ctx.send("User not in database. Use .create to create a user!")
            return 0
        cursor.execute("SELECT username, Impwins, Implosses, Crewwins, Crewlosses FROM OverallTracker WHERE userid = %s", (ussser,))
        UserStats = cursor.fetchone()
        await ctx.send("```Username: " + str(UserStats[0]) + "\nImposter Wins: "+ str(UserStats[1])+ "\nImposter Losses: "+ str(UserStats[2])+ "\nCrew Wins: "+ str(UserStats[3])+"\nCrew Losses: "+str(UserStats[4])+"```")
    elif statistics.lower() == "game":
        if len(game_list) == 0:
            await ctx.send("The game is empty!")
            return 0
        print(statistics)
        for x in range(0, len(game_list)):
            gameuser = game_list[x]
            cursor.execute("SELECT username, Impwins, Implosses, Crewwins, Crewlosses FROM OverallTracker WHERE userid = %s", (gameuser,))
            gamestats = cursor.fetchone()
            await ctx.send("```Username: " + str(gamestats[0]) + "\nImposter Wins: "+ str(gamestats[1])+ "\nImposter Losses: "+ str(gamestats[2])+ "\nCrew Wins: "+ str(gamestats[3])+"\nCrew Losses: "+str(gamestats[4])+"```")
    else:
        await ctx.send("Invalid use of stats command!")
        return 0


@client.command()
async def daily(ctx, statistics):
    if statistics[0] == "<":
        ussser = ""
        for i in range(3, 21):
            ussser += statistics[i]
        cursor.execute("SELECT * FROM DailyTracker WHERE userid = %s", (ussser,))
        tester = cursor.fetchall()
        if tester == []:
            await ctx.send("User not in database. Use .create to create a user!")
            return 0
        cursor.execute("SELECT username, Impwins, Implosses, Crewwins, Crewlosses FROM DailyTracker WHERE userid = %s", (ussser,))
        UserStats = cursor.fetchone()
        await ctx.send("```Daily Statistics:\n\nUsername: " + str(UserStats[0]) + "\nImposter Wins: "+ str(UserStats[1])+ "\nImposter Losses: "+ str(UserStats[2])+ "\nCrew Wins: "+ str(UserStats[3])+"\nCrew Losses: "+str(UserStats[4])+"```")
    elif statistics.lower() == "game":
        if len(game_list) == 0:
            await ctx.send("The game is empty!")
            return 0
        print(statistics)
        for x in range(0, len(game_list)):
            gameuser = game_list[x]
            cursor.execute("SELECT username, Impwins, Implosses, Crewwins, Crewlosses FROM DailyTracker WHERE userid = %s", (gameuser,))
            gamestats = cursor.fetchone()
            await ctx.send("```Daily Statistics:\n\nUsername: " + str(gamestats[0]) + "\nImposter Wins: "+ str(gamestats[1])+ "\nImposter Losses: "+ str(gamestats[2])+ "\nCrew Wins: "+ str(gamestats[3])+"\nCrew Losses: "+str(gamestats[4])+"```")
    else:
        await ctx.send("Invalid use of stats command!")
        return 0



client.run('NzUzMzM5MDc3ODgwOTcxMzg1.X1kvsA.yvgAJ7HSJeaNoHt7rdZHrXZHZhQ')


