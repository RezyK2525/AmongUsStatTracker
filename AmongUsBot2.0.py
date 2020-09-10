import discord
from discord.ext import commands
import mysql.connector
import discord.ext

client = commands.Bot(command_prefix='.')

def checkUname(uname):
    if len(uname) < 32:
        return True
    return False

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
cursor.execute("CREATE TABLE IF NOT EXISTS testtable5(userid VARCHAR(20) primary key, username VARCHAR(32), wins INT, losses INT)")


@client.command()
async def start(ctx, member: discord.Member, uname):

    print(member.id)
    validUname = checkUname(uname)
    if not validUname:
        await ctx.send(
            "That Username is invalid, please resend the command.")
        return 0
    else:
        insert_new_user = ("INSERT INTO testtable5 (userid, username, wins, losses) VALUES (%s, %s, %s, %s)")
        cursor.execute(insert_new_user, (str(member.id), str(uname), 0, 0))
        cursor.execute("SELECT userid, username, wins, losses FROM testtable5")
        row = cursor.fetchall()
        print(*row, sep='\t')
        await ctx.send("Member Added!")

client.run('NzUzMzM5MDc3ODgwOTcxMzg1.X1kvsA.yvgAJ7HSJeaNoHt7rdZHrXZHZhQ')


