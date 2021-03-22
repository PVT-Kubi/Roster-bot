
import discord
import os
from discord.ext import commands
import random
import sys
import datetime
import asyncio
import sqlite3
import re

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '?', help_command = None, intents=intents)





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
async def tab(ctx, baza):

    db = sqlite3.connect('pingus.sqlite', timeout = 10)
    cursor = db.cursor()
    db2 = sqlite3.connect('tesst.db', timeout = 10)
    cursor2 = db2.cursor()
    if baza==('pingus'):
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        result = cursor.fetchall()
        embed = discord.Embed(
            title = 'Oddziały:',
            color = discord.Color.red()
        )
        for x in result:
            for y in x:
                embed.add_field(value = (f'{y}'), name = 'Nazwa oddziału:',  inline = True)
        await ctx.send(embed=embed)
    elif baza==('tesst'):
        cursor2.execute("SELECT name FROM sqlite_master WHERE type='table'")
        result = cursor2.fetchall()
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
    cursor.close()
    cursor2.close()
    db.close()
    db2.close()
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
        db = sqlite3.connect('pingus.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT*FROM {tabela} WHERE Imie = '{member.id}'")
        result = cursor.fetchone()
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
        cursor.close()
        db.close()
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
async def dodaj(ctx, baza, imie, nazwisko, wiek):
    member = await findMember(ctx, imie)
    if member is not None:
        if num(wiek) is not None:
            db = sqlite3.connect('pingus.sqlite', timeout = 10)
            cursor = db.cursor()
            cursor.execute(f"INSERT INTO {baza} VALUES('{member.id}', '{nazwisko}', {wiek})")
            db.commit()
            await ctx.send("Uzytkownik zostal pomyślnie dodany!")
            cursor.close()
            db.close()
        else:
            await ctx.send('Wiek jest liczbą,a nie wyrazem jełopie jebany')
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







client.run('ODIzNjMwMjEwMTkxNzIwNDg4.YFjnaA.sR4wBR_Av1r5hH-zpsK096EVEu8')
