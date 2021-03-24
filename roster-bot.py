
import discord
import os
from discord.ext import commands
import random
import sys
import datetime
import asyncio
import sqlite3
import re
import mysql.connector

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '?', help_command = None, intents=intents)


db = mysql.connector.connect(
    host = "eu-cdbr-west-03.cleardb.net",
    user = "bd8ad38ff63784",
    passwd = "f3a8831d",
    database = "heroku_cd6d7049894a6fc"
    )

mycursor = db.cursor()


async def findMember(ctx, query):
    members = []
    member = ctx.message.guild.get_member_named(query)

    memberList = ctx.message.guild.members

    #filtrowanie = [member for member in memberList if member.nick == query]
    def searchMember(member):
        nickname = member.nick
        if member.nick is not None:
            if '✦' not in query:
                nickname = member.nick.replace('✦ ','')
                nickname = nickname.replace(' ✪','')
                nickname = nickname.replace('✪ ','')
            return nickname.lower() == query.lower()
        else:
            return member.nick == query

    an_iterator = filter(searchMember, memberList)
    filtered_members = list(an_iterator)

    if len(ctx.message.mentions) > 0:
        members.append(ctx.message.mentions[0])
    elif member is not None:
        members.append(member)
    elif len(filtered_members) > 0:
         members.append(filtered_members[0])

    if len(members) > 0:
        return members[0]
    else:
        return None


@client.event
async def on_ready():
    print('Bot is ready')
    await client.change_presence(activity=discord.Streaming(name="Na służbie 24/7 z przerwami", url='https://www.youtube.com/watch?v=FUD5mX0G-KQ'))


@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(
        title = 'Tytuł',
        color = discord.Color.blue()
    )

    embed.set_author(name='Wypisz')
    embed.add_field(name = 'Wypisz', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?wypisz [nazwa oddziału] [nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'wypisuje wszystkie dane, o podanym użytkowniku', inline = True)

    embed.add_field(name = 'Edit', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?edit [numer rajdu] [nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'zwiększa dane', inline = True)

    await ctx.send(embed=embed)

@client.command()
async def Kompania(ctx, *baza):
    if baza==('penis w dupie'):
        mycursor.execute("SELECT*FROM 4th")
        result = mycursor.fetchall()
        embed = discord.Embed(
            title = 'Oddziały:',
            color = discord.Color.red()
        )
        for x in result:
            for y in x:
                embed.add_field(value = (f'{y}'), name = 'Nazwa oddziału:',  inline = True)
        await ctx.send(embed=embed)
    elif baza==('tesst'):
        mycursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        result = mycursor.fetchall()
        embed = discord.Embed(
            title = 'Oddziały:',
            color = discord.Color.red()
        )
        for x in result:
            for y in x:
                embed.add_field(value = (f'{y}'), name = 'Nazwa oddziału:',  inline = True)
        await ctx.send(embed=embed)
    else:
        await ctx.send('Nie znalazłem takiego oddziału (albo o czymś nie wiem)')
@client.command()
async def members(ctx):
    members = ctx.message.guild.members
    filtrowanie = [member for member in members if member.nick == 'dupa']
    print(filtrowanie)
    print(filtrowanie[0])




@client.command()
async def wypisz(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    if member is not None:
        mycursor.execute(f"SELECT*FROM {tabela} WHERE IdStorm = '{member.id}'")
        result = mycursor.fetchone()
        if result is not None:
            author = ctx.message.author
            icon = author.avatar_url
            AtName = (f"{author.name}#{author.discriminator}")
            #await ctx.send(f'```{result[0]} {result[1]} {result[2]}```')
            embed = discord.Embed(
                title = 'Imie:',
                description = result[0],
                color = discord.Color.blue()
            )

            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.add_field(name = 'Nazwisko:', value = member.name, inline = False)
            embed.add_field(name = 'Wiek:', value = result[2], inline = False)
            embed.set_footer(text=AtName, icon_url=icon)

            await ctx.send(embed=embed)
            hasRole = False
            for role in member.roles:
                if role.name != '@everyone':
                    if role.name == 'Tak o':
                        hasRole = True
                        break
            if hasRole:
                sliced = member.nick[3:]
            else:
                sliced = member.nick[2:]
            array = sliced.split("-")
            print(array)

        else:
            await ctx.send("Nie znaleziono uzytkownika w bazie")
    else:
        await ctx.send("Ten użytkownik nie istnieje")

@client.command()
async def find(ctx, query):
    member = await findMember(ctx, query)
    await ctx.send(member)

@client.command()
async def edit(ctx, baza, kolumna, wartosc, imie):
    member = await findMember(ctx, imie)
    if member is not None:
        db = sqlite3.connect('pingus.sqlite', timeout = 10)
        cursor = db.cursor()

        cursor.execute(f"SELECT*FROM {baza} WHERE Imie = '{member.id}'")

        result = cursor.fetchone()
        author = ctx.message.author
        icon = author.avatar_url
        AtName = (f"{author.name}#{author.discriminator}")

        cursor.execute(f"UPDATE {baza} SET {kolumna} = '{wartosc}' WHERE Imie = '{member.id}'")
        db.commit()

        cursor.execute(f"SELECT*FROM {baza} WHERE Imie = '{member.id}'")
        result2 = cursor.fetchone()

        embed = discord.Embed(
            color = discord.Color.green()
        )

        embed.set_author(name=member.name, icon_url=member.avatar_url)
        embed.add_field(name = 'Przed: ' , value = f"``Imię:`` {result[0]}\n``Nazwisko:`` {result[1]}\n``Wiek`` {result[2]}", inline = False)
        embed.add_field(name = 'Po: ' , value = f"``Imie:`` {result2[0]}\n``Nazwisko:`` {result2[1]}\n``Wiek`` {result2[2]}", inline = False)
        embed.set_footer(text=AtName, icon_url=icon)

        await ctx.send(embed=embed)


        await ctx.send("Dane zostały pomyślnie zaktualizowane!")
        cursor.close()
        db.close()
    else:
        await ctx.send("Podany użytkownik nie istnieje")




def num(s):
    try:
        return int(s)
    except ValueError:
        return None

@client.command()
async def dodaj(ctx, baza, imie):
    member = await findMember(ctx, imie)
    if member is not None:
        sliced = member.nick[2:]
        array = sliced.split("-")
        print(array)
        mycursor.execute(f"INSERT INTO {baza}(`IdStorm`, `Ranga`, `Nickname`, `Status`, `Numer`, `Specka`, `Plusy`, `Minusy`, `Aktywnosc`, `Zachowanie`, `DataAwansu/degrada`, `Awansujacy`, `Pozycja`) VALUES('{member.id}', 1, '{array[2]}', 'Aktywny', {array[1]}, 'Piechur', NULL, NULL, '3', '3', NULL, NULL, 1 )")
        mycursor.execute(f"SELECT*FROM {baza} WHERE IdStorm = '{member.id}'")
            await ctx.send("Uzytkownik zostal pomyślnie dodany!")

    else:
        await ctx.send('Podany użytkownik nie istnieje!')

def padStart(string, count):
    if len(string) < count:
        spaces = ""
        for x in range(count-len(string)):
            spaces += " "
        print(spaces + string)
        return (spaces + string)


def padMiddle(string, amount):
    if amount % 2 != 0:
        return "nieparzysta"
    if len(string) <= amount:
        spaces = ""
        for x in range((amount-len(string))//2):
            spaces += " "
        return spaces + string + spaces


@client.command()
async def oddzial(ctx, tabela):
    author = ctx.message.author
    icon = author.avatar_url

    tab = ['Imie', 'Nazwisko', 'Wiek']
    pracie = '```python\n'
    pracie += f'{padMiddle(tab[0], 20)} | {padMiddle(tab[1], 18)} | {padMiddle(tab[2], 6)}\n'
    pracie += '---------------------------------------------------\n'
    AtName = (f"{author.name}#{author.discriminator}")
    wiad = ctx.message.created_at
    db = sqlite3.connect('pingus.sqlite', timeout = 10)
    cursor = db.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabele = []
    uz = []
    for y in cursor.fetchall():
        for z in y:
            tabele.append(z)
    if tabela in tabele:
        cursor.execute(f"SELECT * FROM {tabela}")
        r = cursor.fetchall()


        print(f'{wiad.day}-{wiad.month}-{wiad.year}')
        for x in r:
            pracie += f"{padStart(x[0], 20)} | {padStart(x[1], 18)} | {padStart(str(x[2]),6)}\n"
        pracie += '```'


        embed = discord.Embed(
        description =pracie,
        color = discord.Color.purple())

        embed.set_author(name=tabela, icon_url=icon)
        embed.set_footer(text=AtName, icon_url=icon)
        await ctx.send(embed=embed)







client.run('TOKEN')
