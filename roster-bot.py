
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

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix = '.', help_command = None, intents=intents)

dbconfig ={
    "host" : "eu-cdbr-west-03.cleardb.net",
    "user" : "bd8ad38ff63784",
    "passwd" : "f3a8831d",
    "database": "heroku_cd6d7049894a6fc"
}



connection_pool = pooling.MySQLConnectionPool(
    pool_name = 'Pingus',
    pool_size=5,
    pool_reset_session=True,
    **dbconfig
    )
db = connection_pool.get_connection()
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
        color = discord.Color.purple()
    )

    embed.add_field(name = '``Komendy dostępne dla wszystkich``', value = '\u200B', inline = False)
    embed.add_field(name = 'Wypisz', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?w [nazwa oddziału] [nazwa użytkownika (bez tej gwiazdki na początku), ping, oryginalna nazwa użytkownia]', inline = True)
    embed.add_field(name = 'Opis:', value = 'wypisuje wszystkie dane, o podanym użytkowniku\n', inline = True)


    embed.add_field(name = 'Kompania', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?k [nazwa kompanii]', inline = True)
    embed.add_field(name = 'Opis:', value = 'wyświetla wszystkie oddziały z danej kompanii\n', inline = True)



    embed.add_field(name = '``Komendy tylko dla edytorów``', value = '\u200B', inline = False)
    embed.add_field(name = 'Edit', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?ed [oddzial] [kolumna] [nowa wartoscśclassć] [nazwa użytkownika, ping oryginalna nazwa użytkownia]', inline = True)
    embed.add_field(name = 'Opis:', value = 'zwiększa dane\n', inline = True)


    embed.add_field(name = 'Dodaj', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?d [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = "dodaje użytkownika do rostera (użytkownik musi mieć ten war'owski pseudonim)\n", inline = True)


    embed.add_field(name = 'Awans', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?a [nazwa oddzialu] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'zwiększa rangę użytkownika o jeden w górę\n', inline = True)

    embed.add_field(name = 'Plus/Minus', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?p/m [nazwa oddzialu] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'Dodaje plusa lub minusa (napisane w jednym bo składnia identyczna)\n', inline = True)

    embed.add_field(name = 'Aktywność/Zachowanie', value = '\u200B', inline = False)
    embed.add_field(name = 'Składnia', value = '?ak/z [nazwa oddzialu] [plus albo minus] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    embed.add_field(name = 'Opis:', value = 'Zwiększa lub zmniejsza Aktywność/Zachowanie o jeden (napisane razem bo taka sama składnia)\n', inline = True)


    await ctx.send(embed=embed)
#or '4th' or 'Marksman' or 'marksman' or '4th Marksman Company' or '4th company' or '4th marksman company'
#or '12th' or 'Mechanized' or 'mechanized' or 'Mechanized Company' or '12th Mechanized Company'
@client.command(aliases = ['kompania', 'Kompania', 'K'])
async def k(ctx, *baza):
    
    b = " ".join(baza)
    b = b.lower()
    if b == '4' or b == '4th' or b == 'marksman' or b == '4th marksman company' or b =='4th company':
        mycursor.execute("SELECT*FROM 4th")
            color = discord.Color.red()
    elif b == '12' or b == '12th' or b == 'mechanized' or b == '12th mechanized company' or b == '12th company':
        mycursor.execute("SELECT*FROM 12th")
        color = dirscord.Color.blue()
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


        if pingus == 'Korpus Podoficerów':
            kolor = discord.Color.red()
        elif pingus == 'Sztab Wyższy':
            kolor = discord.Color.green()
        elif pingus == 'Korpus Szeregowych':
            kolor = discord.Color.green()
        else:
            kolor = discord.Color.green()
            #await ctx.send(f'```{result[0]} {result[1]} {result[2]}```')
        desc = ''
        if result[12] is not None:
            prin = ctx.message.guild.get_member(int(result[12]))
            desc += f'**Ranga**: {result[2]}\n**Nickname**: {result[3]}\n **ID**: {result[5]}\n \u200B\n**Pozycja**: {result[13]}\n**Status**: {result[4]}\n**Specka**: {result[6]}\n\u200B\n**Plusy**: {result[7]}\n**Minusy**: {result[8]}\n**Aktywność**: {result[9]}\n**Zachowanie**: {result[10]}\n\u200B\n**Data Awansu/Degrada**: {result[11]}\n**Awansujący**: {prin.nick}'
        else:
            desc += f'**Ranga**: {result[2]}\n**Nickname**: {result[3]}\n **ID**: {result[5]}\n \u200B\n**Pozycja**: {result[13]}\n**Status**: {result[4]}\n**Specka**: {result[6]}\n\u200B\n**Plusy**: {result[7]}\n**Minusy**: {result[8]}\n**Aktywność**: {result[9]}\n**Zachowanie**: {result[10]}\n\u200B\n**Data Awansu/Degrada**: {result[11]}\n**Awansujący**: {None}'

            embed = discord.Embed(
            description = desc,
            color = kolor
            )

        embed.set_author(name=member.nick, icon_url=member.avatar_url)
            embed.set_footer(text=AtName, icon_url=icon)
            await ctx.send(embed=embed)
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
        db.commit()

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
        db.commit()
            embed2 = discord.Embed(
                title = f'witamy w ~~koloni~~ szeregach',
                color = discord.Color.green()
            )

            embed2.set_image(url="https://media.discordapp.net/attachments/811324655310602303/825141657393299456/Tapeta.png?width=840&height=473")
            embed2.set_footer(text=AtName, icon_url=icon)
            embed2.set_author(name = member.mention)
            await ctx.send(embed=embed2)

            await wypisywanie(ctx, member, baza)
            await ctx.send('A tutaj twój wygląd w rosterze :point_up:')

    else:
        await ctx.send('Podany użytkownik nie istnieje!')
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
            db.commit()
            await ctx.send(f'Plusik dla pana {member.nick}')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Jak chcesz sobie zaplusować to rusz dupę a nie tykasz nie swoje komendy!')


@client.command(aliases = ['minus', 'Minus', 'M', 'minusik'])
async def m(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    author = ctx.message.author
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
            db.commit()
            await ctx.send(f'No, ciekawe co pan {member.nick} przeskrobał')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Ty chyba jesteś jakiś niepełnosprytny ?!')


@client.command(aliases = ['aktywnosc', 'Aktywnosc', 'aktywność', 'Aktywność'])
async def ak(ctx, tabela, arg, imie):
    member = await findMember(ctx, imie)
    prin = ctx.message.guild.get_member(509353384709586945)
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
                    db.commit()
                    await ctx.send(f'No kto by pomyślał, {prin.mention} przestał się opierdzielać!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {down(x)} where IdStorm = '{member.id}'")
                    db.commit()
                    await ctx.send(f'{prin.mention} przestań się opierdzielać i pić na służbie!')
            else:
                mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
                r = mycursor.fetchall()
                x = r[0][0]
                if pM =='plus' or pM=='p' or pM=='+':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    db.commit()
                    await ctx.send(f'No po prostu wzorowy żołnierz! Zawsze na treningu i nie pije na służbie! {prin.nick} powinieneś brać z niego przykład!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {down(x)} where IdStorm = '{member.id}'")
                    db.commit()
                    await ctx.send(f'{member.nick} nie idź w ślady Kubiego!!!')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Rusz tą dupę a nie kombinujesz!')



@client.command(aliases = ['Zachowanie', 'zachowanie', 'Z', 'Zach', 'zach'])
async def z(ctx, tabela, arg, imie):
    member = await findMember(ctx, imie)
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
                    db.commit()
                    await ctx.send(f'No kto by pomyślał, {prin.mention} przestał się opierdzielać!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    db.commit()
                    await ctx.send(f'{prin.mention} przestań się opierdzielać i pić na służbie!')
            else:
                mycursor.execute(f"SELECT Ranga, Pozycja FROM {tabela} WHERE IdStorm = '{member.id}'")
                r = mycursor.fetchall()
                x = r[0][0]
                if pM =='plus' or pM=='p' or pM=='+':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    db.commit()
                    await ctx.send(f'No po prostu wzorowy żołnierz! Zawsze na treningu i nie pije na służbie! {prin.nick} powinieneś brać z niego przykład!')
                elif pM=='minus' or pM == 'm' or pM == '-':
                    mycursor.execute(f"UPDATE {tabela} set Aktywnosc = {up(x)} where IdStorm = '{member.id}'")
                    db.commit()
                    await ctx.send(f'{member.nick} nie idź w ślady Kubiego!!!')
        else:
            await ctx.send('Podany użytkownik nie istnieje!')
    else:
        await ctx.send('Ja już nie mam siły. Plusy rozumiem, awans rozumiem, AKTYWNOŚĆ też jeszcze zrozumiem, ALE PO CHOLERE TO ZACHOWANIE SOBIE ZWIĘKSZASZ! PRZECIEŻ TO PRAKTYCZNIE NIC NIE ZNACZY!!!')


@client.command(aliases = ['awans', 'Awans', 'up', 'Up', 'aw', 'Aw'])
async def a(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    wiad = ctx.message.created_at
    author = ctx.message.author
    member2 = await findMember(ctx, author.name)
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
            db.commit()
            await ctx.send(f"Gratuluję awa")
            await ctx.send('chwila...')
            await ctx.send(f"O cholera {member.mention} witamy w podoficerach!!!")
        else:
            mycursor.execute(f"UPDATE {tabela} set Ranga = '{up(x)}', DataAwDeg = '{wiad.year}-{wiad.month}-{wiad.day}', Awansujacy = '{author.id}' WHERE IdStorm = '{member.id}'")
            db.commit()
            mycursor.execute(f"select r.N")
            await ctx.send(f"Gratuluję awansu {member.mention} na :partying_face: :partying_face: :partying_face: ")
    elif hasRole == False:
        await ctx.send('A CO TO ZA DODAWANIE SOBIE AWANSU?! NIE DLA PSA!')





#@client.command(aliases = ['oddzial', 'Oddzial', 'oddział', 'Oddział'])
#async def o(ctx, tabela):
#    author = ctx.message.author
#    icon = author.avatar_url

#    tab = ['Rang', 'Nick', 'Stat', 'Num', 'Spec', '+', '-', 'Aktyw', 'Zach', 'Data_Aw/Deg', 'Aw', 'Poz']
#    pracie = '```python\n'
#    pracie += f'{padMiddle(tab[0], 4)} | {padMiddle(tab[1], 4)} | {padMiddle(tab[2], 4)} | {padMiddle(tab[3], 4)} | {padMiddle(tab[4], 4)} | {padMiddle(tab[5], 2)} | {padMiddle(tab[6], 2)} | {padMiddle(tab[7], 4)} | {padMiddle(tab[8], 4)} | {padMiddle(tab[9], 12)} | {padMiddle(tab[10], 2)} | {padMiddle(tab[11], 4)}\n'
#    pracie += '---------------------------------------------------\n'
#    pracie += '```'
#    AtName = (f"{author.name}#{author.discriminator}")

#    mycursor.execute("SELECT*FROM tabele")/
#    r = mycursor.fetchall()
#    tabele = []
#    uz = []
#    for y in r:
#        for z in y:
#            tabele.append(z)
    #print(tabele)
#    if tabela in tabele:
#        mycursor.execute(f"SELECT * FROM {tabela}, Rangi WHERE {tabela}.Ranga = Rangi.Ranga")
#        r = mycursor.fetchall()



#        for x in r:
#            pracie += f"{padStart(int('x[1]'), 19)} | {padStart(x[2], 8)} | {padStart(x[3],6)} | {padStart(int('x[4]'), 20)} | {padStart(x[5], 18)} | {padStart(int('x[6]'),6)} | {padStart(int('x[7]'), 20)} | {padStart(x[8], 18)} | {padStart(x[9],6)} | {padStart(int('x[10]'), 20)} | {padStart(x[11], 20)} | {padStart(x[12], 18)}\n"
#        pracie += '```'



#    await ctx.send(pracie)







client.run('TOKEN')
