
import discord
import os
from discord.ext import commands
import random
import sys
import datetime
import asyncio
import sqlite3
import re
from mysql.connector import pooling
import MySQLdb
from MySQLdb.cursors import SSCursor


intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.', help_command = None, intents=intents)


def connection():
    connection = MySQLdb.connect(
    host = "eu-cdbr-west-03.cleardb.net",
    user = 'bd8ad38ff63784',
    passwd = 'f3a8831d',
    db = 'heroku_cd6d7049894a6fc',
    )
    return connection


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
        color = discord.Color.purple()
    )

    embed.add_field(name = '``Komendy dostępne dla wszystkich``', value = '\u200B', inline = False)
    embed.add_field(name = 'Wypisz', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '.w [nazwa oddziału] [nazwa użytkownika (bez tej gwiazdki na początku), ping, oryginalna nazwa użytkownia]', inline = True)
    embed.add_field(name = 'Opis:', value = 'wypisuje wszystkie dane, o podanym użytkowniku\n', inline = True)


    embed.add_field(name = 'Kompania', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '.k [nazwa kompanii]', inline = True)
    embed.add_field(name = 'Opis:', value = 'wyświetla wszystkie oddziały z danej kompanii\n', inline = True)



    embed.add_field(name = '``Komendy tylko dla edytorów``', value = '\u200B', inline = False)
    embed.add_field(name = 'Edit', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '.e [oddzial] [kolumna] [nowa wartoscśclassć] [nazwa użytkownika, ping oryginalna nazwa użytkownia]', inline = True)
    embed.add_field(name = 'Opis:', value = 'zwiększa dane\n', inline = True)


    embed.add_field(name = 'Dodaj', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '.d [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = "dodaje użytkownika do rostera (użytkownik musi mieć ten war'owski pseudonim)\n", inline = True)


    embed.add_field(name = 'Awans', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '.a [nazwa oddzialu] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'zwiększa rangę użytkownika o jeden w górę\n', inline = True)

    embed.add_field(name = 'Plus/Minus', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '.p/m [nazwa oddzialu] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'Dodaje plusa lub minusa (napisane w jednym bo składnia identyczna)\n', inline = True)

    embed.add_field(name = 'Aktywność/Zachowanie', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '.ak/z [nazwa oddzialu] [plus albo minus] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'Zwiększa lub zmniejsza Aktywność/Zachowanie o jeden (napisane razem bo taka sama składnia)\n', inline = True)


    await ctx.send(embed=embed)
#or '4th' or 'Marksman' or 'marksman' or '4th Marksman Company' or '4th company' or '4th marksman company'
#or '12th' or 'Mechanized' or 'mechanized' or 'Mechanized Company' or '12th Mechanized Company'
@client.command(aliases = ['kompania', 'Kompania', 'K'])
async def k(ctx, *baza):
    conn = connection()
    mycursor = SSCursor(conn)
    b = " ".join(baza)
    b = b.lower()
    if b == '4' or b == '4th' or b == 'marksman' or b == '4th marksman company' or b =='4th company':
        mycursor.execute("SELECT*FROM 4th")
        color = discord.Color.red()
    elif b == '12' or b == '12th' or b == 'mechanized' or b == '12th mechanized company' or b == '12th company':
        mycursor.execute("SELECT*FROM 12th")
        color = discord.Color.blue()
    else:
        return await ctx.send('Taki taka kompania nie istnieje (albo o czymś nie wiem)')
    result = mycursor.fetchall()
    embed = discord.Embed(
        title = 'Oddziały:',
        color = color
    )


    for x in result:
        for y in x:
            embed.add_field(value = (f'{y}'), name = 'Nazwa oddziału:',  inline = True)
    await ctx.send(embed=embed)


@client.command()
async def members(ctx):
    members = ctx.message.guild.members
    filtrowanie = [member for member in members if member.nick == 'dupa']
    print(filtrowanie)
    print(filtrowanie[0])

async def wypisywanie(ctx, mb, tab):
    member = mb
    tabela = tab
    conn = connection()
    mycursor = SSCursor(conn)
    if tab == 'liderzy' or tab == 'Liderzy' or tab == 'Lider' or tab == 'lider':
        mycursor.execute(f"select IdStorm, Czego FROM liderzy WHERE IdStorm = '{member.id}'")
        result = mycursor.fetchone()
        if result is not None:
            author = ctx.message.author
            icon = author.avatar_url
            AtName = (f"{author.name}#{author.discriminator}")
            members = ctx.message.guild.members
            prin = ctx.message.guild.get_member(int(result[0]))


            embed = discord.Embed(
                color = discord.Color.blue()
            )
            embed.add_field(name = 'ID Lidera', value = prin.nick, inline = False)
            embed.add_field(name = 'Lider czego?', value = result[1], inline = False)
            embed.set_author(name=member.nick, icon_url=member.avatar_url)
            embed.set_footer(text=AtName, icon_url=icon)
            await ctx.send(embed=embed)
            conn.close()
        else:
            await ctx.send('Podany uzytkownik nie istnieje (no chyba, że jestem ślepy ale śmiem w to wątpi, gdyż do czytania danych nie używam wzroku tylko kodu...)')
    else:


        mycursor.execute(f"select a.IdStorm, r.RangaId, r.RangaNazw, a.Nickname, a.Stat, a.Numer, a.Specka, a.Plusy, a.Minusy, a.Aktywnosc, a.Zachowanie,a.DataAwDeg, a.Awansujacy, p.Pozycja FROM {tabela} a, Rangi r, Pozycja p WHERE r.Ranga = a.Ranga and a.Pozycja = p.IDPozycja and IdStorm = '{member.id}'")
        result = mycursor.fetchone()
        if result is not None:

            author = ctx.message.author
            icon = author.avatar_url
            AtName = (f"{author.name}#{author.discriminator}")
            members = ctx.message.guild.members
            if result[12] in members:
               print('chuj')
            pingus = result[13]
            hasArc = False
            for role in member.roles:
                if role.name != '@everyone':
                    if role.name == '┃ARC┃':
                        hasArck = True
                        break
            if hasArc:
                sliced = member.nick[3:]
            else:
                sliced = member.nick[2:]
            array = sliced.split("-")

            if pingus == 'Korpus Podoficerow':
                kolor = discord.Color.red()
            elif pingus == 'Sztab Wyzszy':
                kolor = 0xf1c40f
            elif pingus == 'Korpus Szeregowych':
                kolor = discord.Color.green()
            else:
                kolor = discord.Color.green()
            #await ctx.send(f'```{result[0]} {result[1]} {result[2]}```')
            desc = ''
            if result[12] is not None:
                prin = ctx.message.guild.get_member(int(result[12]))
                desc += f'**Ranga**: {result[2]}\n**Nickname**: {result[3]}\n **ID**: {array[2]}\n \u200B\n**Pozycja**: {result[13]}\n**Status**: {result[4]}\n**Specka**: {result[6]}\n\u200B\n**Plusy**: {result[7]}\n**Minusy**: {result[8]}\n**Aktywność**: {result[9]}\n**Zachowanie**: {result[10]}\n\u200B\n**Data Awansu/Degrada**: {result[11]}\n**Awansujący**: {prin.nick}'
            else:
                desc += f'**Ranga**: {result[2]}\n**Nickname**: {result[3]}\n **ID**: {result[5]}\n \u200B\n**Pozycja**: {result[13]}\n**Status**: {result[4]}\n**Specka**: {result[6]}\n\u200B\n**Plusy**: {result[7]}\n**Minusy**: {result[8]}\n**Aktywność**: {result[9]}\n**Zachowanie**: {result[10]}\n\u200B\n**Data Awansu/Degrada**: {result[11]}\n**Awansujący**: {result[12]}'

            embed = discord.Embed(
                description = desc,
                color = kolor
            )

            embed.set_author(name=member.nick, icon_url=member.avatar_url)
            embed.set_footer(text=AtName, icon_url=icon)
            await ctx.send(embed=embed)
            conn.close()
        else:
            await ctx.send("Nie znaleziono uzytkownika w bazie")

@client.command(aliases = ['wypisz', 'Wypisz', 'wypisywanie', 'Wypisywanie', 'W'])
async def w(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    if member is not None:
        await wypisywanie(ctx, member, tabela)
        hasRole = False
        for role in member.roles:
            if role.name != '@everyone':
                if role.name == 'Edytor rostera':
                    hasRole = True
                    break
        if hasRole:
            sliced = member.nick[3:]
        else:
            sliced = member.nick[2:]
        array = sliced.split("-")




    else:
        await ctx.send("Ten użytkownik nie istnieje")

@client.command()
async def find(ctx, query):
    member = await findMember(ctx, query)
    await ctx.send(member)

@client.command(aliases = ['edit', 'Edit', 'edytuj', 'Edytuj','E'])
async def e(ctx, baza, kolumna, wartosc, imie):
    member = await findMember(ctx, imie)
    conn = connection()
    mycursor = SSCursor(conn)
    hasRole = False
    author = ctx.message.author
    if member is not None:
        for role in author.roles:
            if role.name != '@everyone':
                if role.name == 'Edytor rostera':
                    hasRole = True
                    break
        if hasRole == True:
            mycursor.execute(f"SELECT {kolumna} FROM {baza} WHERE IdStorm = '{member.id}' ")

            result = mycursor.fetchone()
            author = ctx.message.author
            icon = author.avatar_url
            AtName = (f"{author.name}#{author.discriminator}")

            mycursor.execute(f"UPDATE {baza} set {kolumna} = '{wartosc}' WHERE IdStorm = '{member.id}'")
            conn.commit()

            mycursor.execute(f"SELECT {kolumna} FROM {baza} WHERE IdStorm = '{member.id}' ")
            result2 = mycursor.fetchone()

            embed = discord.Embed(
                color = discord.Color.green()
            )

            embed.set_author(name=member.name, icon_url=member.avatar_url)
            embed.add_field(name = 'Przed: ' , value = f"``{kolumna}:`` {result[0]}", inline = False)
            embed.add_field(name = 'Po: ' , value = f"``{kolumna}:`` {result2[0]}", inline = False)
            embed.set_footer(text=AtName, icon_url=icon)

            await ctx.send(embed=embed)


            await ctx.send("Dane zostały pomyślnie zaktualizowane!")

        else:
            await ctx.send('Jak chcesz edytować nick na GMD-2137-JP2 to gadaj z przełożonymi...')
        conn.close()
    else:
        await ctx.send("Podany użytkownik nie istnieje")








def num(s):
    try:
        return int(s)
    except ValueError:
        return None



@client.command(aliases = ['dodaj', 'Dodaj', 'add', 'Add', 'D'])
async def d(ctx, baza, imie):
    member = await findMember(ctx, imie)
    conn= connection()
    mycursor = SSCursor(conn)
    hasRole = False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor rostera':
                hasRole = True
                break

    if hasRole == True:
        desc = ''
        if member is not None:
            author = ctx.message.author
            icon = author.avatar_url
            AtName = (f"{author.name}#{author.discriminator}")
            sliced = member.nick[0:]
            array = sliced.split("-")
            print(array)
            mycursor.execute(f"INSERT INTO {baza}(`IdStorm`, `Ranga`, `Nickname`, `Stat`, `Numer`, `Specka`, `Plusy`, `Minusy`, `Aktywnosc`, `Zachowanie`, `DataAwDeg`, `Awansujacy`, `Pozycja`) VALUES('{member.id}', 1, '{array[2]}', 'Aktywny', {array[1]}, 'Piechur', NULL, NULL, '3', '3', NULL, NULL, 1 )")
            conn.commit()
            embed2 = discord.Embed(
                title = f'witamy w ~~koloni~~ szeregach',
                color = discord.Color.green()
            )

            embed2.set_image(url="https://cdn.discordapp.com/attachments/760953812713472060/825819921287217202/proxy-image.jpg")
            embed2.set_footer(text=AtName, icon_url=icon)
            embed2.set_author(name = f'{array[0]}-{array[1]}-{array[2]}')
            await ctx.send(embed=embed2)

            await wypisywanie(ctx, member, baza)
            await ctx.send('A tutaj twój wygląd w rosterze :point_up:')

        else:
            await ctx.send('Podany użytkownik nie istnieje!')
        conn.close()
    else:
        await ctx.send('Coś mi się wydaje, że jedyne co możesz sobie dodać to chromosom...')

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

def up(arg):

    arg += 1
    return arg

def down(arg):
    if arg > 1:
        arg -= 1
    return arg


@client.command(aliases = ['plus', 'Plus', 'P', 'plusik'])
async def p(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    conn = connection()
    mycursor = SSCursor(conn)
    hasRole = False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor rostera':
                hasRole = True
                break
    if hasRole == True:
        if member is not None:
            mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
            r = mycursor.fetchall()
            x = r[0][0]
            mycursor.execute(f"UPDATE {tabela} set Plusy = {up(x)} where IdStorm = '{member.id}'")
            conn.commit()
            await ctx.send(f'Plusik dla pana {member.nick}')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Jak chcesz sobie zaplusować to rusz dupę a nie tykasz nie swoje komendy!')
    conn.close()


@client.command(aliases = ['minus', 'Minus', 'M', 'minusik'])
async def m(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    author = ctx.message.author
    conn = connection()
    mycursor = SSCursor(conn)
    hasRole = False
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor rostera':
                hasRole = True
                break
    if hasRole == True:
        if member is not None:
            mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
            r = mycursor.fetchall()
            x = r[0][0]
            mycursor.execute(f"UPDATE {tabela} set Minusy = {up(x)} where IdStorm = '{member.id}'")
            conn.commit()
            await ctx.send(f'No, ciekawe co pan {member.nick} przeskrobał')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Ty chyba jesteś jakiś niepełnosprytny ?!')
    conn.close()


@client.command(aliases = ['aktywnosc', 'Aktywnosc', 'aktywność', 'Aktywność'])
async def ak(ctx, tabela, arg, imie):
    member = await findMember(ctx, imie)
    prin = ctx.message.guild.get_member(509353384709586945)
    conn = connection()
    mycursor = SSCursor(conn)
    author = ctx.message.author
    pM = arg.lower()
    hasRole = False
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor rostera':
                hasRole = True
                break
    if hasRole == True:
        if member is not None:
            if member.id == prin.id:
                mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
                r = mycursor.fetchall()
                x = r[0][0]
                if pM =='plus' or pM=='p' or pM=='+':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'No kto by pomyślał, {prin.mention} przestał się opierdzielać!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {down(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'{prin.mention} przestań się opierdzielać i pić na służbie!')
            else:
                mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
                r = mycursor.fetchall()
                x = r[0][0]
                if pM =='plus' or pM=='p' or pM=='+':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'No po prostu wzorowy żołnierz! Zawsze na treningu i nie pije na służbie! {prin.nick} powinieneś brać z niego przykład!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {down(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'{member.nick} nie idź w ślady Kubiego!!!')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Rusz tą dupę a nie kombinujesz!')
    conn.close()



@client.command(aliases = ['Zachowanie', 'zachowanie', 'Z', 'Zach', 'zach'])
async def z(ctx, tabela, arg, imie):
    member = await findMember(ctx, imie)
    conn = connection()
    mycursor = SSCursor(conn)
    author = ctx.message.author
    prin = ctx.message.guild.get_member(509353384709586945)
    pM = arg.lower()
    hasRole = False
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor rostera':
                hasRole = True
                break
    if hasRole == True:
        if member is not None:
            if member.id == prin.id:
                mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
                r = mycursor.fetchall()
                x = r[0][0]
                if pM =='plus' or pM=='p' or pM=='+':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'No kto by pomyślał, {prin.mention} przestał się opierdzielać!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'{prin.mention} przestań się opierdzielać i pić na służbie!')
            else:
                mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
                r = mycursor.fetchall()
                x = r[0][0]
                if pM =='plus' or pM=='p' or pM=='+':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'No po prostu wzorowy żołnierz! Zawsze na treningu i nie pije na służbie! {prin.nick} powinieneś brać z niego przykład!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    conn.commit()
                    await ctx.send(f'{member.nick} nie idź w ślady Kubiego!!!')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Ja już nie mam siły. Plusy rozumiem, awans rozumiem, AKTYWNOŚĆ też jeszcze zrozumiem, ALE PO CHOLERE TO ZACHOWANIE SOBIE ZWIĘKSZASZ! PRZECIEŻ TO PRAKTYCZNIE NIC NIE ZNACZY!!!')
    conn.close()

@client.command(aliases = ['awans', 'Awans', 'up', 'Up', 'aw', 'Aw'])
async def a(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    wiad = ctx.message.created_at
    author = ctx.message.author
    member2 = await findMember(ctx, author.name)
    conn = connection()
    mycursor = SSCursor(conn)
    hasRole = False
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor rostera':
                hasRole = True
                break
    if hasRole == True:
        wiad = ctx.message.created_at
        mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
        result = mycursor.fetchall()
        x = result[0][0]
        z = result[0][1]
        sliced = member2.nick[2:]
        #ar = sliced.split("-")
        print(author.nick)
        print(member.id)
        if x > 2 and z < 2:
            mycursor.execute(f"UPDATE {tabela} set Ranga = {up(x)}, Pozycja = {up(z)}, DataAwDeg = '{wiad.year}-{wiad.month}-{wiad.day}', Awansujacy = '{author.id}' WHERE IdStorm = '{member.id}'")
            conn.commit()
            await ctx.send(f"Gratuluję awa")
            await ctx.send('chwila...')
            await ctx.send(f"O cholera {member.mention} witamy w podoficerach!!!")
        else:
            mycursor.execute(f"UPDATE {tabela} set Ranga = '{up(x)}', DataAwDeg = '{wiad.year}-{wiad.month}-{wiad.day}', Awansujacy = '{author.id}' WHERE IdStorm = '{member.id}'")
            conn.commit()
            await ctx.send(f"Gratuluję awansu {member.mention} na :partying_face: :partying_face: :partying_face: ")
    elif hasRole == False:
        await ctx.send('A CO TO ZA DODAWANIE SOBIE AWANSU?! NIE DLA PSA!')
    conn.close()

@client.command(aliases = ['u', 'U', 'Usuń', 'usuń', 'Miej_litość_usuń ', 'delete', 'Delete', 'De'])
async def de(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    if member is not None:
        conn = connection()
        mycursor = SSCursor(conn)
        mycursor.execute(f"select*from tabele")
        r = mycursor.fetchall()
        tab = []
        for x in r:
            for y in x:
                tab.append(y.lower())
        if tabela.lower() in tab:
            mycursor.execute(f"DELETE FROM {tabela} WHERE IdStorm = '{member.id}'")
            conn.commit()
            await ctx.send(f"{member.nick} dostał lepę z {tabela}u")
        else:
            await ctx.send(f"Niestety nie udało mi się znaleźć oddziału o nazwie: '{tabela}'")
        conn.close()
    else:
        await ctx.send('Nie udało mi się znaleźć takiego użytkownika (pamiętaj, że na razie obsługuję tylko pingi)')









@client.command(aliases = ['oddzial', 'Oddzial', 'oddział', 'Oddział', 'O'])
async def o(ctx, tabela, pp):
    #author = ctx.message.author
    #icon = author.avatar_url
    conn= connection()
    mycursor = SSCursor(conn)
    #tab = ['Rang', 'Nick', 'Stat', 'Num', 'Spec', '+', '-', 'Aktyw', 'Zach', 'Data_Aw/Deg', 'Aw', 'Poz']
    pracie = '```python\n'
    #pracie += f'{padMiddle(tab[0], 4)} | {padMiddle(tab[1], 4)} | {padMiddle(tab[2], 4)} | {padMiddle(tab[3], 4)} | {padMiddle(tab[4], 4)} | {padMiddle(tab[5], 2)} | {padMiddle(tab[6], 2)} | {padMiddle(tab[7], 4)} | {padMiddle(tab[8], 4)} | {padMiddle(tab[9], 12)} | {padMiddle(tab[10], 2)} | {padMiddle(tab[11], 4)}\n'
    #pracie += '---------------------------------------------------\n'
    #AtName = (f"{author.name}#{author.discriminator}")
    mycursor.execute("SELECT*FROM tabele")
    r = mycursor.fetchall()
    tabele = []
    uz = []
    for y in r:
        for z in y:
            tabele.append(z.lower())
    print(tabele)
    if tabela.lower() in tabele:
        if tabela.lower() == 'liderzy' or tabela.lower() == 'l':
            mycursor.execute(f"select IdStorm, Czego FROM liderzy ")
            re = mycursor.fetchall()

            for x in re:
                print(x[0])
                prin = ctx.message.guild.get_member(int(x[0]))
                pracie +=f"{padMiddle(prin.nick, 30)} | {padMiddle(x[1], 38)}\n"
            pracie += "```"
            await ctx.send(pracie)

        elif pp.lower() == 'podstawowe' or pp.lower() =='p':
            mycursor.execute(f"select  r.RangaId, r.RangaNazw, a.Nickname, a.Specka, a.Numer, a.Stat, p.Pozycja FROM {tabela} a, Rangi r, Pozycja p WHERE r.Ranga = a.Ranga and a.Pozycja = p.IDPozycja")
            re = mycursor.fetchall()
            print(re)

            pracie += f"{padMiddle(f'RangaNazw',20)} | {padMiddle(f'Nickname',12)} | {padMiddle(f'Specka',10)} | {padMiddle(f'Numer',6)} | {padMiddle(f'Pozycja',18)}\n"
            pracie += f"-----------------------------------------------------------------------------\n"
            for x in re:
                 print(x[0])
                 p = x[5]

                 pracie += f" {padStart(f'{x[1]}',18)} | {padStart(f'{x[2]}', 12)} | {padStart(f'{x[3]}',10)} | {padStart(f'{x[4]}', 5)} | {padStart(f'{x[6]}', 19)}\n"

            pracie += '```'
            await ctx.send(f'Podstawowe dane {tabela}u:\n{pracie}')
            mycursor.close()
            conn.close()
        elif pp.lower() == 'aktywnosc' or pp.lower() =="ak":
            mycursor.execute(f"select  a.Nickname, a.Stat, a.Plusy, a.Minusy, a.Aktywnosc, a.Zachowanie FROM {tabela} a")
            re = mycursor.fetchall()
            print(re)

            pracie += f"{padMiddle(f'Nickname',12)} | {padMiddle(f'Stat',8)} | {padMiddle('Plusy', 6)} | {padMiddle('Minusy', 8)} | {padMiddle(f'Aktywnosc',10)} | {padMiddle(f'Zachowanie',12)}|\n"
            pracie += f"-----------------------------------------------------------------------------\n"
            for x in re:
                 print(x[0])


                 pracie += f" {padStart(f'{x[0]}', 11)} | {padStart(f'{x[1]}',8)} | {padStart(f'{x[2]}', 9)} | {padStart(f'{x[3]}',11)} | {padStart(f'{x[4]}', 5)} | {padStart(f'{x[5]}', 7)}\n"

            pracie += '```'
            await ctx.send(f'Dane dotyczące aktywności {tabela}u:\n{pracie}')
            mycursor.close()
            conn.close()
        elif pp.lower() == 'awanse' or pp.lower() =="aw" :
            mycursor.execute(f"select  a.Nickname, a.DataAwDeg, a.Awansujacy FROM {tabela} a")
            re = mycursor.fetchall()
            print(re)

            pracie += f"{padMiddle(f'Nickname',14)} | {padMiddle(f'DataAwDeg',12)} | {padMiddle(f'Awansujacy',22)} |\n"
            pracie += f"-------------------------------------------------------\n"
            for x in re:
                print(x[0])
                if x[2] is not None:
                    prin = ctx.message.guild.get_member(int(x[2]))
                    sliced = prin.nick[2:]
                    print(sliced)
                    pracie += f" {padStart(f'{x[0]}', 13)} | {padStart(f'{x[1]}',11)} | {padStart(f'{sliced}', 22)} |\n"
                else:
                    pracie += f" {padStart(f'{x[0]}', 13)} | {padStart(f'{x[1]}',11)} | {padStart(f'None', 22)} |\n"
            pracie += '```'
            await ctx.send(f'Dane na temat awansów {tabela}u:\n{pracie}')
            mycursor.close()
            conn.close()
        else:
            await ctx.send('Podaj poprawne dane!!!')
    else:
        await ctx.send('Nie znalazłem takiego oddziału')






client.run('ODIzNjMwMjEwMTkxNzIwNDg4.YFjnaA.sR4wBR_Av1r5hH-zpsK096EVEu8')
