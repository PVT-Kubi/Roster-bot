import discord
import os
from discord.ext import commands
import random
import sys
import datetime
import asyncio
import sqlite3
import re
import time
from mysql.connector import pooling
import MySQLdb
from MySQLdb.cursors import SSCursor
from discord.utils import get
from discord import FFmpegPCMAudio
import youtube_dl
from youtube_dl import YoutubeDL
# import cv2
from waiting import wait
# from discord_slash import SlashCommand
# from discord_slash.utils.manage_commands import create_option
from NHentai.nhentai import NHentai
# from NHentai.nhentai_async import NHentaiAsync




intents = discord.Intents.all()
intents.members = True
client = commands.Bot(command_prefix = '.', help_command = None, intents=intents)
#slash = SlashCommand(client, sync_commands=True)
# config = dotenv_values('.env')
config =os.environ

#guild_ids = 811324655310602300

# if not discord.opus.is_loaded():
#     # the 'opus' library here is opus.dll on windows
#     # or libopus.so on linux in the current directory
#     # you should replace this with the location the
#     # opus library is located in and with the proper filename.
#     # note that on windows this DLL is automatically provided for you
#     discord.opus.load_opus('opus')

# players = {}
queue = []
z = 0
dict = {}
looping = False


def connection():
    connection = MySQLdb.connect(
        host = config['HOST'],
        user = config['USER'],
        passwd = config['PASSW'],
        db = config['DB'],
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
    kubi = client.get_user(509353384709586945)
    levi = client.get_user(776053863483965470)
    cherr= client.get_user(521992400755884052)


    await client.change_presence(activity=discord.Streaming(name="Pozdro Cherro jesteś kocur <3", url='https://www.youtube.com/watch?v=uVgZHQ93H1o'))

    # embed = discord.Embed(
    #     color = 10092441,
    #     title = "Siemano kapitany!",
    #     description = f" Pewnie większość z was mnie zna, a jak nie to chociaż o mnie słyszała, gdyż z tego co mi wiadomo byłem pare razy wspominany, ale dla tych co mnie jeszcze nie kojarzą, jestem szeregowy Bubi i będę odpowiedzialny za papierkową robotę tego oddziału! Jeśli chodzi o pochodzenie to przenieśli mnie z innej jednostki (bo usłyszeli, że do teraz używacie tabelek w excelu). O i jeszcze jedno, nie jestem klonem, jednak nie jeste też naturalnie powstałą rasą. Zostałem sztucznie stworzony w ramach operacji R O A S T. Za projekt ciała odpowiada {levi.mention} jednak twórcą umysłu na moje cholerne nieszczęście jest {kubi.mention} (z tego powodu łatwo mogę się wywalić). Nom o mnie to chyba tyle...\n **Liczę na owocną współpracę!**"
    # )
    #
    # embed.set_image(url = "https://media.discordapp.net/attachments/833425519802449951/836872743541669928/Wilk_Natasza.jpg?width=473&height=473")
    # await client.get_channel(843512570057195521).send(embed=embed)
    #
    # await client.get_channel(843512570057195521).send(f'https://media.discordapp.net/attachments/760953812713472060/838789087740690473/mergedimage.png?width=473&height=473')

@client.event
async def on_member_remove(member):
    channel = client.get_channel(825344498178981888)
    channel2 = client.get_channel(843512570057195521)
    print(member.id)
    hasRole = False
    Oddzial = ''
    for role in member.roles:
        if role.name != '@everyone':
            if role.name == '104th Battalion':
                hasRole = True
                break
    if hasRole:
        for role in member.roles:
            if role.name != '@everyone':
                if 'Platoon' in role.name:
                    Oddzial = role.name.replace('Platoon','')
                    break
        print(Oddzial)
        conn = connection()
        mycursor = SSCursor(conn)

        mycursor.execute(f"select * FROM {Oddzial.lower()} WHERE IdStorm = '{member.id}'")
        result = mycursor.fetchone()
        if result:
            mycursor.execute(f"DELETE FROM {Oddzial.lower()} WHERE IdStorm = '{member.id}'")
            conn.commit()
            await client.send_message(message.channel2, f"Nasz kamrat {member.nick} opuścił nasz oddział...")




@client.group(invoke_without_command=True)
async def help(ctx):
    tresc = "```Komendy dostępne dla wszystkich```\n\n**Wypisz**\n``Składnia``: .w [nazwa oddziału] [ping użytkownik]\n``Opis``: wypisuje wszystkie dane, o podanym użytkowniku\n\n**Kompania**\n``Składnia``: .k [nazwa kompanii]\n``Opis``: wyświetla wszystkie oddziały z danej kompanii\n\n**Oddzial**\n``Składnia``: .o [nazwa oddziału] podstawowe(lub p)/awanse(lub aw)/aktywnosc(lub ak)\n``Opis``: Wypisuje podany w argumentach rodzaj danych na temat danego oddziału\n\n**Lista**"
    tresc += "\n``Składnia``: .l\n``Opis``: wypisuje listę użytkowników na kanale, na którym znajduje się piszący komendę\n\n**Lista Kanału**\n``Składnia``: .lk [pełna nazwa kanału (bez emotek kresek czy spacji)]\n``Opis``: wyświetla listę użytkowników z podanego kanału (nie radzę używać bo pełne nazwy kanałów głosowych w łor są trochę dlugie :p\n\n```Komendy dostępne tylko dla edytorów```\n\n**Edit**\n``Składnia``: "
    tresc += ".e [oddzial] [kolumna] [nowa wartoscść] [ping użytkownia]\n``Opis``: Zmienia wartosc kolumny na podaną przez użytkownika\n\n**Dodaj**\n``Składnia``: .d [nazwa oddziału] [ping użytkownia]\n``Opis``: dodaje użytkownika do podanego oddziału (używać tylko dla nowych użytkowników!!!)\n\n**Copy paste**\n``Składnia``: .pa [nazwa starego oddziału] [nazwa nowego oddziału] [ping użytkownia]\n``Opis``: kopiuje użytkownika i wkleja jego dane do nowego oddziału (jednak nie usuwa go ze starego, ze względu na bezpieczeństwo)\n\n **Delete**\n``Składnia``: .de [nazwa oddziału [nazwa użytkownika]\n``Opis``: Usuwa użytkownika z podanego oddziału\n\n**Plus/Minus**\n``Składnia``: .p/m [nazwa oddziału] [ping użytkownika]\n``Opis``: Dodaje jednego plusa/minusa\n\n**Awans**\n``Składnia``: .a [nazwa oddziału] [ping użytkownika]\n``Opis``: zwiększa rangę użytkownika o jeden\n\n**Zachowanie/Aktywnosc**\n``Składnia``: .ak/z [nazwa oddziału] +/- [ping użytkownika]\n``Opis``: zwiększa/zmniejsza aktywnosc/zachowanie użytkownika o jeden"
    voice_client = discord.utils.get(client.voice_clients, guild = ctx.guild)
    print(voice_client)

    embed = discord.Embed(
        color = discord.Color.purple(),
        description = tresc
    )

    # embed.add_field(name = '``Komendy dostępne dla wszystkich``', value = '\u200B', inline = False)
    # embed.add_field(name = 'Wypisz', value = '\u200B', inline = False)
    # embed.add_field(name = 'Składnia', value = '.w [nazwa oddziału] [nazwa użytkownika (bez tej gwiazdki na początku), ping, oryginalna nazwa użytkownia]', inline = True)
    # embed.add_field(name = 'Opis:', value = 'wypisuje wszystkie dane, o podanym użytkowniku\n', inline = True)
    #
    #
    # embed.add_field(name = 'Kompania', value = '\u200B', inline = False)
    # embed.add_field(name = 'Składnia', value = '.k [nazwa kompanii]', inline = True)
    # embed.add_field(name = 'Opis:', value = 'wyświetla wszystkie oddziały z danej kompanii\n', inline = True)
    #
    #
    #
    # embed.add_field(name = '``Komendy tylko dla edytorów``', value = '\u200B', inline = False)
    # embed.add_field(name = 'Edit', value = '\u200B', inline = False)
    # embed.add_field(name = 'Składnia', value = '.e [oddzial] [kolumna] [nowa wartoscśclassć] [nazwa użytkownika, ping oryginalna nazwa użytkownia]', inline = True)
    # embed.add_field(name = 'Opis:', value = 'zwiększa dane\n', inline = True)
    #
    #
    # embed.add_field(name = 'Dodaj', value = '\u200B', inline = False)
    # embed.add_field(name = 'Składnia', value = '.d [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    # embed.add_field(name = 'Opis:', value = "dodaje użytkownika do rostera (użytkownik musi mieć ten war'owski pseudonim)\n", inline = True)
    #
    #
    # embed.add_field(name = 'Awans', value = '\u200B', inline = False)
    # embed.add_field(name = 'Składnia', value = '.a [nazwa oddzialu] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    # embed.add_field(name = 'Opis:', value = 'zwiększa rangę użytkownika o jeden w górę\n', inline = True)
    #
    # embed.add_field(name = 'Plus/Minus', value = '\u200B', inline = False)
    # embed.add_field(name = 'Składnia', value = '.p/m [nazwa oddzialu] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    # embed.add_field(name = 'Opis:', value = 'Dodaje plusa lub minusa (napisane w jednym bo składnia identyczna)\n', inline = True)
    #
    # embed.add_field(name = 'Aktywność/Zachowanie', value = '\u200B', inline = False)
    # embed.add_field(name = 'Składnia', value = '.ak/z [nazwa oddzialu] [plus albo minus] [nazwa użytkownika (bez tej gwiazdki), ping lub oryginalna nazwa użytkownika]', inline = True)
    # embed.add_field(name = 'Opis:', value = 'Zwiększa lub zmniejsza Aktywność/Zachowanie o jeden (napisane razem bo taka sama składnia)\n', inline = True)
    #

    await ctx.send(embed=embed)



# @client.command()
# async def play(ctx, url):
#     voice = get(client.voice_clients, guild=ctx.guild)
#     YDL_OPTIONS = {
#         'format': 'bestaudio',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'mp3',
#             'preferredquality': '192',
#         }],
#         'outtmpl': 'song.%(ext)s',
#     }
#
#     with YoutubeDL(Music.YDL_OPTIONS) as ydl:
#         ydl.download("URL", download=True)
#
#     if not voice.is_playing():
#         voice.play(FFmpegPCMAudio("song.mp3"))
#         voice.is_playing()
#         await ctx.send(f"Now playing {url}")
#     else:
#         await ctx.send("Already playing song")
#         return


#------------------------------------Moduł muzyczny-------------------------------------------------------------

#opcja druga któa też nie działas
# global songs
# global obj
# print(obj[g.id][1])
# song_there = os.path.isfile("song.m4a")
# wait(lambda: is_something_ready(obj[g.id][1]) == True)
# for x in songs[g.id]:
#     try:
#         if song_there:
#             os.remove("song.m4a")
#     except PermissionError:
#         await ctx.send("Zaczekaj, aż skończę, albo użyj stop")
#         return
#
#
#     ydl_opts = {
#         'format': 'm4a'
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([x])
#     for file in os.listdir("./"):
#         if file.endswith(".m4a"):
#             os.rename(file, "song.m4a")
#     obj[g.id][1].play(discord.FFmpegOpusAudio("song.m4a"))
#
# def is_something_ready(something):
#     if not something.is_playing(): #<- nawet tu miałem takie coś
#         return True
#     return False

#tu event bu uratował bo nie musi co sekundę sprawdzać
# def looping(ctx, g, vc, i, loop):
#     global songs
#     global obj
#     if len(songs[g.id]) > 0:
#         i+=1
#         asyncio.run_coroutine_threadsafe(playing(ctx, g, vc, i), loop)
#     else:
#         return
#
#
#
#
#
# async def playing(ctx, g, vc, i):
#     global songs
#     global obj
#     countdown = 0
#
#     print(songs[g.id])
#     song_there = os.path.isfile("song.webm")
#     # wait(lambda: is_something_ready(obj[g.id][1]), timeout_seconds=120, waiting_for="utwór się kończy")
#     try:
#         if song_there:
#             os.remove("song.webm")
#     except PermissionError:
#         # await ctx.send("Zaczekaj, aż skończę, albo użyj stop")
#         return
#
#
#     ydl_opts = {
#         'format': '249/250/251',
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([songs[g.id][i]])
#     for file in os.listdir("./"):
#         if file.endswith(".webm"):
#             os.rename(file, "song.webm")
#     source = await discord.FFmpegOpusAudio.from_probe("song.webm")
#     vc.play(source, after = looping(ctx, g, vc, i, vc.loop))






#---------------------------------------------Proszę tego nie czytać, wstąpił we mnie diabeł-------------------------------------------------------------------------------------
@client.command()
async def po(ctx):
    guild = ctx.message.guild
    if guild.id != 819694752240107590:
        nhentai = NHentai()
        doujins: PopularPage = nhentai.get_popular_now()
        ForCulturedMan = doujins.doujins[random.randrange(0, doujins.total_doujins)]
        try:
            embed = discord.Embed(
                title = ForCulturedMan.title.english,
                url = ForCulturedMan.url,
                color = discord.Color.purple()

            )
        except:
            embed = discord.Embed(
                url = ForCulturedMan.url,
                color = discord.Color.purple()

            )
        print(ForCulturedMan.title)
        try:
            embed.add_field(name = "Język", value = ForCulturedMan.lang, inline = False)

            embed.add_field(name = "Tagi", value = str(ForCulturedMan.data_tags).replace("'", "").replace("[", "").replace("]", ""), inline = False)


        except Exception:
            embed.set_image(url=ForCulturedMan.cover.src)
            await ctx.send(embed=embed)
    else:
        await ctx.send("Chciałbyś :smirk:")


@client.command()
async def szukamPromoFree(ctx, *, p):
    nhentai = NHentai()
    print(p)
    guild = ctx.message.guild
    if guild.id != 819694752240107590:
        try:
            search_obj: SearchPage = nhentai.search(query=f'{p}', sort='popular', page=1)
            print(search_obj)
            ps = search_obj.doujins[0]
            embed = discord.Embed(
                title = ps.title,
                url = ps.url,
                color = discord.Color.purple()

            )

            embed.set_image(url=ps.cover)
            await ctx.send(embed=embed)
        except:
            # try:
            search_obj: SearchPage = nhentai.search(query=f'{p}', sort='popular', page=1)
            sb2: SearchPage = nhentai.search(query=f'{search_obj.title}', sort='popular', page=1)
            ps = sb2.doujins[0]
            embed = discord.Embed(
                title = ps.title+".",
                url = ps.url,
                color = discord.Color.purple()

            )

            embed.add_field(name = "Artysta/ci", value = str(search_obj.artists).replace("'", "").replace("[", "").replace("]", "")+".", inline = False)
            embed.add_field(name = "Języki", value = str(search_obj.languages).replace("'", "").replace("[", "").replace("]", "")+".", inline = False)
            embed.add_field(name = "Tags", value = str(search_obj.tags).replace("'", "").replace("[", "").replace("]", "")+".", inline = False)
            embed.set_image(url=search_obj.images[0])
            embed.set_footer(text = f"Total pages: {search_obj.total_pages}")
            await ctx.send(embed=embed)
            # except:
            #     await ctx.send("Nie znaleziono żadnego wyniku pasującego do wyszukiwania")
    else:
        await ctx.send("Człowieku, poszukaj lepiej kiedy masz trening. Zrobisz chociaż coś pożytecznego")
@client.command()
async def ReadSomeBook(ctx, *, p):
    nhentai = NHentai()
    guild = ctx.message.guild
    if guild.id != 819694752240107590:
        try:
            search_obj: SearchPage = nhentai.search(query=f'{p}', sort='popular', page=1)
            ps = search_obj.doujins[0]
            sb2: SearchPage = nhentai.get_doujin(id=ps.id)
            print(sb2)
            for i in sb2.images:
                await ctx.send(i)
        except:
            try:
                search_obj: SearchPage = nhentai.get_doujin(id=p)
                for i in search_obj.images:
                    await ctx.send(i)
            except:
                await ctx.send("Nie znaleziono żadnego wyniku pasującego do wyszukiwania")
    else:
        await ctx.send("Doceniam to, że czytasz, jednak radziłbym sięgnąć po bardziej rozwijające dzieła...")

#---------------------------------------------Już można czytać, dziękuje za wyrozumiałość-------------------------------------------------------------------------------------
@client.command()
async def radio(ctx, a):
    author = ctx.message.author
    guild = ctx.message.guild
    radia = {
    'nowyswiat' :  'https://n13a-eu.rcs.revma.com/ypqt40u0x1zuv?rj-ttl=5&rj-tok=AAABe5gXcdwA-OfbaBMtuSF13w',
    'rmf' : 'https://rs202-krk.rmfstream.pl/RMFFM48?aw_0_req.gdpr=false&aw_0_req.userConsentV2=CPLwq6lPLwq6lFKACAPLBoCgAAAAAEPAAB5YAAAQTAJMNS8gC7EscGRaNKoUQIwrCQ6AUAFFAMLRMYAMDgp2VgEOoAWACA1ARgRAgxBRgwCAAQCAJCIgJACwQCIAiAAAAgBUgIQAETAILACwMAgAFANCxAigCECQgyOCo5TAgIkWignsrAEou9hTCEMssAKBR_RUYCJQggWBkJCwcxwBICXAAAAA.YAAAD4AAAAAA&aw_0_1st.playerid=RMF_Player_JS_P&aw_0_1st.rmf_disable_preroll=true',
    'eska' : 'https://uk3-play.adtonos.com/8102/eska-sosnowiec',
    'antyradio' : 'https://n-16-12.dcs.redcdn.pl/sc/o2/Eurozet/live/antyradio.livx?audio=5?t=1630345258565',
    'radiozet' : 'https://n-16-11.dcs.redcdn.pl/sc/o2/Eurozet/live/audio.livx?audio=5?t=1630345320815',
    'chillizet' : 'https://n-22-9.dcs.redcdn.pl/sc/o2/Eurozet/live/chillizet.livx?audio=5?t=1630345364253',
    'maryja' : 'https://radiomaryja.fastcast4u.com/proxy/radiomaryja?mp=/1',
    'anime' : 'https://radioanime.radioca.st/stream/1/'
    }



    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
    else:
        await ctx.send("Nie ma cię na żadnym kanale głosowym")
        return
    try:
        await channel.connect()
    except:
        print("Bot jest już na kanale")
    voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild = guild)
    print(voice_client)
    voice_client.play(FFmpegPCMAudio(radia[a.lower()]))

async def actualPlay(guild, source):
    global dict
    global looping
    FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
    YDL_OPTIONS = {'format':'bestaudio'}
    voice_client = dict[guild.id][2]
    if not voice_client.is_playing():
        voice_client.play(source)
    while voice_client.is_playing():
        await asyncio.sleep(3)
    if looping:
        await doingStuff(FFMPEG_OPTIONS, YDL_OPTIONS, guild)

async def doingStuff(FFMPEG_OPTIONS, YDL_OPTIONS, guild):
        global dict
        global looping
        FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
        YDL_OPTIONS = {'format':'bestaudio'}
        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            vc = dict[guild.id][2]
            x =dict[guild.id][0][0]
            info = ydl.extract_info(x, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            while looping == True:
                await actualPlay(guild, source)


@client.command()
async def loop(ctx):
    global dict
    global looping
    guild = ctx.message.guild
    guilded = False

    for y in dict:
        if y == guild.id:
            guilded = True
    if not guilded:
        await ctx.send("Bot nie gra żadnego utworu")
    else:
        if not looping:
            looping = True
            await ctx.send("Włączono zapętlanie utworu")
            FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
            YDL_OPTIONS = {'format':'bestaudio'}
            await doingStuff(FFMPEG_OPTIONS, YDL_OPTIONS, guild)
            # with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            #     vc = dict[guild.id][2]
            #     x =dict[guild.id][0][0]
            #     info = ydl.extract_info(x, download=False)
            #     url2 = info['formats'][0]['url']
            #     source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            #     while looping == True:
            #         await actualPlay(guild, source)
        else:
            looping = False
            await ctx.send("Włączono zapętlanie utworu")


@client.command()
async def skip(ctx):
    global dict
    global looping
    guild = ctx.message.guild
    guilded = False
    hasRole =  False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if '104th Battalion' in role.name:
                hasRole = True
                break
            elif role.name == 'DJ':
                hasRole = True
                break
    if hasRole:
        for y in dict:
            if y == guild.id:
                guilded = True
        if not guilded:
            await ctx.send("Bot nie gra żadnego utworu")
        else:
            try:
                dict[guild.id][1] += 1
                x = dict[guild.id][0][dict[guild.id][1]]
            except:
                await ctx.send("Nie ma czego loopować")
                return
            if looping:
                looping = False
            vc = dict[guild.id][2]
            if vc.is_playing():
                vc.stop()
            dict[guild.id][1] += 1
            FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
            YDL_OPTIONS = {'format':'bestaudio'}
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                 info = ydl.extract_info(x, download=False)
                 url2 = info['formats'][0]['url']
                 source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
                 looping = True
                 await actualPlay(guild, source)
    else:
        await ctx.send("Sory, ale służę w jednostce 104 i tylko oni mają dostęp do modułu muzycznego.")


async def playing(voice_client, FFMPEG_OPTIONS, YDL_OPTIONS, guild, x):
    global dict
    # loop = asyncio.get_event_loop()
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
         info = ydl.extract_info(x, download=False)
         url2 = info['formats'][0]['url']
         source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
         # voice_client.play(source)
         await actualPlay(guild, source)
         # looping(error, voice_client, FFMPEG_OPTIONS, YDL_OPTIONS, loop, guild, x)
         try:
             dict[guild.id][1] += 1
             x = dict[guild.id][0][dict[guild.id][1]]
             print("Nice")
         except Exception as e:
             print("Cock")
             print(e)
             del dict[guild.id]
             return
         await playing(voice_client, FFMPEG_OPTIONS, YDL_OPTIONS, guild, x)






# def looping(voice_client, FFMPEG_OPTIONS, YDL_OPTIONS, loop, guild, x):
#     global dict
#
#     try:
#         dict[guild.id][1] += 1
#         x = dict[guild.id][0][dict[guild.id][1]]
#         print("Nice")
#     except:
#         print("Cock")
#         del dict[guild.id]
#         return
#     x = dict[guild.id][dict[guild.id][1]]
#     try:
#         foot = asyncio.run_coroutine_threadsafe(playing(voice_client, FFMPEG_OPTIONS, YDL_OPTIONS, guild, x), client.loop)
#         foot.result()
#     except Exception as e:
#         print(e)


@client.command()
async def play(ctx, x : str):
    global dict
    author = ctx.message.author
    guild = ctx.message.guild
    guilded = False
    hasRole =  False
    server = ctx.message.server
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if '104th Battalion' in role.name:
                hasRole = True
                break
            elif 'DJ' in role.name:
                hasRole = True
                break
    if hasRole:
        for y in dict:
            if y == guild.id:
                guilded = True
        if guilded == False:
            FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options':'-vn'}
            YDL_OPTIONS = {'format':'bestaudio'}

            if ctx.author.voice and ctx.author.voice.channel:
                channel = ctx.author.voice.channel
            else:
                await ctx.send("Nie ma cię na żadnym kanale głosowym")
                return
            #channel =  client.get_channel(825294815007604788)
            try:
                await channel.connect()
            except:
                print("Bot jest już na kanale")
            voice_client: discord.VoiceClient = client.voice_client_in(server)
            print(voice_client)
            dict = {guild.id : [[x], 0, voice_client]}
            print(dict[guild.id][0][0])
            await playing(dict[guild.id][2], FFMPEG_OPTIONS, YDL_OPTIONS, guild, dict[guild.id][0][0])
        else:
            print(dict[guild.id][0])
            dict[guild.id][0].append(x)
            print(dict[guild.id][0])
    else:
        await ctx.send("Sory, ale służę w jednostce 104 i tylko oni mają dostęp do modułu muzycznego.")


# @client.command()
# async def play(ctx, url : str):
#     global obj
#     global songs
#
#
#     obj = {}
#     songs = {}
#     i = 0
#
#     hasRole =  False
#     hasGuild = False
#     canPlay = False
#     author = ctx.message.author
#     guild = ctx.message.guild
#     # channel = client.get_channel(811324655310602304)
#     # guild = client.get_guild(811324655310602300)
#     for role in author.roles:
#         if role.name != '@everyone':
#             if role.name == '104th Battalion':
#                 hasRole = True
#                 break
#             if role.name == 'Przeciętny Pasożyt':
#                 hasRole = True
#                 break
#     if hasRole:
#         for x in obj:
#             if x == guild.id:
#                 hasGuild = True
#         if hasGuild == False:
#             if ctx.author.voice and ctx.author.voice.channel:
#                 channel = ctx.author.voice.channel
#             else:
#                 await ctx.send("Nie ma cię na żadnym kanale głosowym")
#                 return
#             try:
#                 await channel.connect()
#             except:
#                 print("Bot jest już na kanale")
#             voice_client = discord.utils.get(client.voice_clients, guild = guild)
#             obj = {
#                 guild.id: [channel, voice_client]
#             }
#             songs  = {
#                 guild.id: []
#             }
#             songs[guild.id].append(url)
#             print("Nie ma gilidi")
#             await playing(ctx, guild, voice_client, i)
#
#
#         elif hasGuild == True:
#             songs[guild.id].append(url)
#             #await playing(ctx, guild, voice_client, i)
#
#
#
#
#
#             # channel = obj[guild.id][0]
#             # voice_client = obj[guild.id][1]
#             # while canPlay == False:
#             #     if not voice_client.is_playing():
#             #         time.sleep()
#             #         await playing(ctx, url, guild, channel, voice_client)
#
#     else:
#         await ctx.send("Sory, ale służę w jednostce 104 i tylko oni mają dostęp do modułu muzycznego.")
# #
#
@client.command()
async def leave(ctx):
    hasRole =  False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if '104th Battalion' in role.name:
                hasRole = True
                break
            elif role.name == 'DJ':
                hasRole = True
                break
    if hasRole:
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
        else:
            await ctx.send("You are not connected to a voice channel")
            return
        voice_client = discord.utils.get(client.voice_clients, guild = ctx.guild)
        if voice_client:
            if voice_client.is_connected():
                await voice_client.disconnect()
            else:
                await ctx.send("Nie jestem połączony z kanałem głosowym")
    else:
        await ctx.send("Sory, ale służę w jednostce 104 i tylko oni mają dostęp do modułu muzycznego.")

@client.command()
async def pause(ctx):
    hasRole =  False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if '104th Battalion' in role.name:
                hasRole = True
                break
            elif role.name == 'Przeciętny Pasożyt':
                hasRole = True
                break
    if hasRole:
        voice_client = discord.utils.get(client.voice_clients, guild = ctx.guild)
        if voice_client.is_playing():
            voice_client.pause()
        else:
            await ctx.send("Nic nie gram")
    else:
        await ctx.send("Sory, ale służę w jednostce 104 i tylko oni mają dostęp do modułu muzycznego.")

@client.command()
async def resume(ctx):
    hasRole =  False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if '104th Battalion' in role.name:
                hasRole = True
                break
            elif role.name == 'Przeciętny Pasożyt':
                hasRole = True
                break
    if hasRole:
        voice_client = discord.utils.get(client.voice_clients, guild = ctx.guild)
        if voice_client.is_paused():
            voice_client.resume()
        else:
            await ctx.send("Nie zatrzymałeś utworu, więc jak mam go kontynuować?")
    else:
        await ctx.send("Sory, ale służę w jednostce 104 i tylko oni mają dostęp do modułu muzycznego.")



@client.command()
async def stop(ctx):
    hasRole =  False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if '104th Battalion' in role.name:
                hasRole = True
                break
            elif role.name == 'Przeciętny Pasożyt':
                hasRole = True
                break

    if hasRole:
        voice_client = discord.utils.get(client.voice_clients, guild = ctx.guild)
        voice_client.stop()
    else:
        await ctx.send("Sory, ale służę w jednostce 104 i tylko oni mają dostęp do modułu muzycznego.")

#-------------------------------------------------------------------------------------------------------------------------------------------


@client.command(aliases = ['Pa', 'paste', 'Paste'])
async def pa(ctx, oddzial, newOd, imie):
    member = await findMember(ctx, imie)
    hasRole =  False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor Rostera':
                hasRole = True
                break
    if hasRole:
        if member is not None:
            conn = connection()
            mycursor = SSCursor(conn)

            mycursor.execute(f"select * FROM {oddzial} WHERE IdStorm = '{member.id}'")
            result = mycursor.fetchone()

            if result[11] is None or result[11] == 'None':
                mycursor.execute(f"INSERT INTO {newOd}(`IdStorm`, `Ranga`, `Nickname`, `Stat`, `Numer`, `Specka`, `Plusy`, `Minusy`, `Aktywnosc`, `Zachowanie`, `DataAwDeg`, `Awansujacy`, `Pozycja`) values({result[0]}, {result[1]}, '{result[2]}', '{result[3]}', {result[4]}, '{result[5]}', '{result[6]}', '{result[7]}', '{result[8]}', '{result[9]}', '{result[10]}', NULL, '{result[12]}') ")
            else:
                mycursor.execute(f"INSERT INTO {newOd}(`IdStorm`, `Ranga`, `Nickname`, `Stat`, `Numer`, `Specka`, `Plusy`, `Minusy`, `Aktywnosc`, `Zachowanie`, `DataAwDeg`, `Awansujacy`, `Pozycja`) values({result[0]}, {result[1]}, '{result[2]}', '{result[3]}', {result[4]}, '{result[5]}', '{result[6]}', '{result[7]}', '{result[8]}', '{result[9]}', '{result[10]}', '{result[11]}', '{result[12]}') ")
            conn.commit()
            await ctx.send(f'Pomyslnie udało się skopiować i przenieść użytkownia {member.nick} do {newOd}u. Można już go bezpiecznie usunąć ze starego oddziału!')
            mycursor.close()
            conn.close()
        else:
            await ctx.send('Nie udało mi się znaleźć podanego użytkownia')
    else:
        await ctx.send('Na twoje nieszczęście Bilokacja to tylko bajeczka, a nie faktyczne zjawisko.')

    #for x in ctx.message.mentions:
        #member = ctx.message.guild.get_member_named(x)





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
    elif b == '7' or b == '7th' or b == 'armored' or b == '7th armored company' or b == '7th company':
        mycursor.execute("SELECT*FROM 7th")
        color = discord.Color.orange()
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
    mycursor.close()
    conn.close()


#@client.command()
#async def members(ctx):
#    members = ctx.message.guild.members
#    filtrowanie = [member for member in members if member.nick == 'dupa']
#    print(filtrowanie)
#    print(filtrowanie[0])

async def wypisywanie(ctx, mb, tab):
    member = mb
    tabela = tab

    url = member.avatar
    conn = connection()
    mycursor = SSCursor(conn)
    if tab == 'liderzy' or tab == 'Liderzy' or tab == 'Lider' or tab == 'lider':
        mycursor.execute(f"select IdStorm, Czego FROM liderzy WHERE IdStorm = '{member.id}'")
        result = mycursor.fetchone()
        if result is not None:
            author = ctx.message.author
            icon = author.avatar
            AtName = (f"{author.name}#{author.discriminator}")
            members = ctx.message.guild.members
            prin = ctx.message.guild.get_member(int(result[0]))


            embed = discord.Embed(
                color = discord.Color.blue()
            )
            embed.add_field(name = 'ID Lidera', value = prin.nick, inline = False)
            embed.add_field(name = 'Lider czego?', value = result[1], inline = False)
            embed.set_author(name=member.nick, icon_url = url)
            embed.set_footer(text=AtName, icon_url=icon)
            await ctx.send(embed=embed)
        else:
            await ctx.send('Podany uzytkownik nie istnieje (no chyba, że jestem ślepy ale śmiem w to wątpi, gdyż do czytania danych nie używam wzroku tylko kodu...)')

    else:


        mycursor.execute(f"select a.IdStorm, r.RangaId, r.RangaNazw, a.Nickname, a.Stat, a.Numer, a.Specka, a.Plusy, a.Minusy, a.Aktywnosc, a.Zachowanie,a.DataAwDeg, a.Awansujacy, p.Pozycja FROM {tabela} a, Rangi r, Pozycja p WHERE r.Ranga = a.Ranga and a.Pozycja = p.IDPozycja and IdStorm = '{member.id}'")
        result = mycursor.fetchone()
        if result is not None:
            author = ctx.message.author
            icon = author.avatar
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
                desc += f'**Ranga**: {result[2]}\n**Nickname**: {result[3]}\n **ID**: {result[5]}\n \u200B\n**Pozycja**: {result[13]}\n**Status**: {result[4]}\n**Specka**: {result[6]}\n\u200B\n**Plusy**: {result[7]}\n**Minusy**: {result[8]}\n**Aktywność**: {result[9]}\n**Zachowanie**: {result[10]}\n\u200B\n**Data Awansu/Degrada**: {result[11]}\n**Awansujący**: {prin.nick}'
            else:
                desc += f'**Ranga**: {result[2]}\n**Nickname**: {result[3]}\n **ID**: {result[5]}\n \u200B\n**Pozycja**: {result[13]}\n**Status**: {result[4]}\n**Specka**: {result[6]}\n\u200B\n**Plusy**: {result[7]}\n**Minusy**: {result[8]}\n**Aktywność**: {result[9]}\n**Zachowanie**: {result[10]}\n\u200B\n**Data Awansu/Degrada**: {result[11]}\n**Awansujący**: '

            embed = discord.Embed(
                description = desc,
                color = kolor
            )

            embed.set_author(name=member.nick, icon_url= member.avatar)
            embed.set_footer(text=AtName, icon_url=icon)
            await ctx.send(embed=embed)
        else:
            await ctx.send("Nie znaleziono uzytkownika w bazie")
    mycursor.close()
    conn.close()

# @slash.slash(name = "wypisywanie", description = "wypisuje wszystkie dane podanego użytkownia", options = [create_option(name = "od", description = "oddzial", option_type = 3, required=True), create_option(name = "ping", description = "ping", option_type = 6, required=True)],  guild_ids = guild_ids)
# async def w(ctx, od: str, ping):
#     print(ping.id)
#     member = ctx.guild.get_member(ping.id)
#     author = ctx.guild.get_member(ctx.author_id)
#     guild = client.get_guild(guild_ids)
#
#     print(guild)
#
#     print(ctx.author_id)
#
#     await wypisywanie(ctx, member, od, author)
# #
# #    else:
    #    await ctx.send("Ten użytkownik nie istnieje")




@client.command(aliases = ['wypisz', 'Wypisz', 'wypisywanie', 'Wypisywanie', 'W'])
async def w(ctx, tabela, imie):
    #if ctx.message.mentions[0] == 823630210191720488:
    #    await ctx.send("Miło, że sprawidzłeś/aś co ze mną, ale stety lub nie da się mnie dodać do rostera...\n*Znowu_w_życiu_mi_nie_wyszło.mp4*")
    #else:
    member = await findMember(ctx, imie)
    if member is not None:
        await wypisywanie(ctx, member, tabela)

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
                if role.name == 'Edytor Rostera':
                    hasRole = True
                    break
        if hasRole == True:
            mycursor.execute(f"SELECT {kolumna} FROM {baza} WHERE IdStorm = '{member.id}' ")

            result = mycursor.fetchone()
            author = ctx.message.author
            icon = author.avatar
            AtName = (f"{author.name}#{author.discriminator}")

            mycursor.execute(f"UPDATE {baza} set {kolumna} = '{wartosc}' WHERE IdStorm = '{member.id}'")
            conn.commit()

            mycursor.execute(f"SELECT {kolumna} FROM {baza} WHERE IdStorm = '{member.id}' ")
            result2 = mycursor.fetchone()

            embed = discord.Embed(
                color = discord.Color.green()
            )

            embed.set_author(name=member.name, icon_url=member.avatar)
            embed.add_field(name = 'Przed: ' , value = f"``{kolumna}:`` {result[0]}", inline = False)
            embed.add_field(name = 'Po: ' , value = f"``{kolumna}:`` {result2[0]}", inline = False)
            embed.set_footer(text=AtName, icon_url=icon)

            await ctx.send(embed=embed)


            await ctx.send("Dane zostały pomyślnie zaktualizowane!")

        else:
            await ctx.send('Jak chcesz edytować nick na GMD-2137-JP2 to gadaj z przełożonymi...')
    else:
        await ctx.send("Podany użytkownik nie istnieje")
    mycursor.close()
    conn.close()


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
            if role.name == 'Edytor Rostera':
                hasRole = True
                break

    if hasRole == True:
        desc = ''
        if member is not None:
            author = ctx.message.author
            icon = author.avatar
            AtName = (f"{author.name}#{author.discriminator}")
            sliced = member.nick[0:]
            array = sliced.split("-")
            print(array)
            mycursor.execute(f"INSERT INTO {baza}(`IdStorm`, `Ranga`, `Nickname`, `Stat`, `Numer`, `Specka`, `Plusy`, `Minusy`, `Aktywnosc`, `Zachowanie`, `DataAwDeg`, `Awansujacy`, `Pozycja`) VALUES('{member.id}', 1, '{array[2]}', 'Aktywny', {array[1]}, 'Piechur', NULL, NULL, '4', '4', NULL, NULL, 1 )")
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
    else:
        await ctx.send('Coś mi się wydaje, że jedyne co możesz sobie dodać to chromosom...')
    mycursor.close()
    conn.close()

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
            if role.name == 'Edytor Rostera':
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
    mycursor.close()
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
            if role.name == 'Edytor Rostera':
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
    mycursor.close()
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
            if role.name == 'Edytor Rostera':
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
    mycursor.close()
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
            if role.name == 'Edytor Rostera':
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
    mycursor.close()
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
            if role.name == 'Edytor Rostera':
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
        if x == 2 and z < 2:
            mycursor.execute(f"UPDATE {tabela} set Ranga = {up(x)}, Pozycja = {up(z)}, DataAwDeg = '{wiad.year}-{wiad.month}-{wiad.day}', Awansujacy = '{author.id}' WHERE IdStorm = '{member.id}'")
            conn.commit()
            await ctx.send(f"Gratuluję awa")
            await ctx.send('chwila...')
            await ctx.send(f"O cholera {member.mention} witamy w podoficerach!!!")
        else:
            mycursor.execute(f"UPDATE {tabela} set Ranga = '{up(x)}', DataAwDeg = '{wiad.year}-{wiad.month}-{wiad.day}', Awansujacy = '{author.id}' WHERE IdStorm = '{member.id}'")
            conn.commit()
            await ctx.send(f"Gratuluję awansu {member.mention} :partying_face: :partying_face: :partying_face: ")
    elif hasRole == False:
        await ctx.send('A CO TO ZA DODAWANIE SOBIE AWANSU?! NIE DLA PSA!')
    mycursor.close()
    conn.close()

@client.command(aliases = ['u', 'U', 'Usuń', 'usuń', 'Zmiluj_sie_usuń ', 'delete', 'Delete', 'De'])
async def de(ctx, tabela, imie):
    member = await findMember(ctx, imie)
    hasRole = False
    author = ctx.message.author
    for role in author.roles:
        if role.name != '@everyone':
            if role.name == 'Edytor Rostera':
                hasRole = True
                break
    if hasRole:
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
            mycursor.close()
            conn.close()
        else:
            await ctx.send('Nie udało mi się znaleźć takiego użytkownika (pamiętaj, że na razie obsługuję tylko pingi)')
    else:
        await ctx.send('Nie wiem kto ci zalazł za skórę, ale takie rzeczy załatwia się za grażami.')



@client.command(aliases = ['Lista', 'lista', 'L'])
async def l(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        channel = ctx.author.voice.channel
        memeber = channel.members
        tekst = f'```**Lista Obecności**```\n'
        print(len(memeber))
        if len(memeber) != 0:
            author = ctx.message.author
            icon = author.avatar
            AtName = (f"{author.name}#{author.discriminator}")

            await ctx.send("Już podaję:")
            for x in memeber:
                tekst += f"{x.nick}\n"

            embed = discord.Embed(
                color = discord.Color.orange(),
                description = tekst
            )

            embed.set_footer(text=AtName, icon_url=icon)
            await ctx.send(embed=embed)

        else:
            await ctx.send("Ludzie tu nikogo nie ma")
    else:
        await ctx.send("Z tego co widzę nie ma cię na głosowym?")

@client.command(aliases = ['LK', 'Lk', 'LisaKanalu'])
async def lk(ctx, *,arg):
    if arg.lower() == "7" or arg.lower() == "7th":
        ThisId = 834103651882106971
    elif arg.lower() == "12" or arg.lower() == "12th":
        ThisId = 825294836033781760
    elif arg.lower() == "4" or arg.lower() == "4th":
        ThisId = 825294826965958696
    elif arg.lower() == "104" or arg.lower() == "104th":
        ThisId = 825294815007604788
    else:
        for c in ctx.guild.channels:
            if c.name.lower()[2:] == arg.lower():
                ThisId = c.id

    voiceChannel = discord.utils.get(ctx.message.guild.channels, id = ThisId, type=discord.ChannelType.voice)
    tekst = f'```**Lista Obecności**```\n'
    memeber = voiceChannel.members
    print(len(memeber))
    if len(memeber) != 0:
        author = ctx.message.author
        icon = author.avatar
        AtName = (f"{author.name}#{author.discriminator}")

        await ctx.send("Już podaję:")
        for x in memeber:
            tekst += f"{x.nick}\n"

        embed = discord.Embed(
            color = discord.Color.orange(),
            description = tekst
        )


        embed.set_footer(text=AtName, icon_url=icon)
        await ctx.send(embed=embed)

    else:
        await ctx.send("Ludzie tu nikogo nie ma")



@client.command(aliases = ['oddzial', 'Oddzial', 'oddział', 'Oddział', 'O'])
async def o(ctx, tabela, pp):
    author = ctx.message.author
    icon = author.avatar
    conn= connection()
    mycursor = SSCursor(conn)
    counter = 0
    arrayOfStrings = []
    #tab = ['Rang', 'Nick', 'Stat', 'Num', 'Spec', '+', '-', 'Aktyw', 'Zach', 'Data_Aw/Deg', 'Aw', 'Poz']
    arrayOfStrings.append('```python\n')
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
            arrayOfStrings[counter] += f"{padMiddle('ID Lidera', 30)} | {padMiddle('Blok dowodzenia', 38)}|\n"
            arrayOfStrings[counter] += f"----------------------------------------------------------------------\n"
            for x in re:
                print(x[0])

                prin = ctx.message.guild.get_member(int(x[0]))
                sliced = prin.nick[2:]
                array = sliced.split("-")
                arrayOfStrings[counter] +=f"{padStart(f'{array[0]}-{array[1]}-{array[2]}', 29)} | {padStart(f'{x[1]}', 37)}|\n"
            arrayOfStrings[counter] += "```"
            await ctx.send(arrayOfStrings[counter])

        elif pp.lower() == 'podstawowe' or pp.lower() =='p':
            mycursor.execute(f"select  r.RangaId, r.RangaNazw, a.Nickname, a.Specka, a.Numer, a.Stat, p.Pozycja FROM {tabela} a, Rangi r, Pozycja p WHERE r.Ranga = a.Ranga and a.Pozycja = p.IDPozycja")
            re = mycursor.fetchall()
            print(re)

            arrayOfStrings[counter] += f"{padMiddle(f'RangaNazw',20)} | {padMiddle(f'Nickname',12)} | {padMiddle(f'Specka',10)} | {padMiddle(f'Numer',6)} | {padMiddle(f'Pozycja',18)}\n"
            arrayOfStrings[counter] += f"-----------------------------------------------------------------------------\n"
            for x in re:
                if(len(arrayOfStrings[counter]) < 1900):
                     print(x[0])
                     p = x[5]

                     arrayOfStrings[counter] += f" {padStart(f'{x[1]}',18)} | {padStart(f'{x[2]}', 12)} | {padStart(f'{x[3]}',10)} | {padStart(f'{x[4]}', 5)} | {padStart(f'{x[6]}', 19)}\n"
                else:
                    arrayOfStrings[counter] += '```'
                    await ctx.send(f'Podstawowe dane {tabela}u:\n{arrayOfStrings[counter]}')
                    counter += 1
                    arrayOfStrings.append('```python\n')
                    arrayOfStrings[counter] += f"{padMiddle(f'RangaNazw',20)} | {padMiddle(f'Nickname',12)} | {padMiddle(f'Specka',10)} | {padMiddle(f'Numer',6)} | {padMiddle(f'Pozycja',18)}\n"
                    arrayOfStrings[counter] += f"-----------------------------------------------------------------------------\n"
                    arrayOfStrings[counter] += f" {padStart(f'{x[1]}',18)} | {padStart(f'{x[2]}', 12)} | {padStart(f'{x[3]}',10)} | {padStart(f'{x[4]}', 5)} | {padStart(f'{x[6]}', 19)}\n"


            arrayOfStrings[counter] += '```'
            print(len(arrayOfStrings[counter]))
            await ctx.send(f'Podstawowe dane {tabela}u:\n{arrayOfStrings[counter]}')

        elif pp.lower() == 'aktywnosc' or pp.lower() =="ak":
            mycursor.execute(f"select  a.Nickname, a.Stat, a.Plusy, a.Minusy, a.Aktywnosc, a.Zachowanie FROM {tabela} a")
            re = mycursor.fetchall()
            print(re)

            arrayOfStrings[counter] += f"{padMiddle(f'Nickname',12)} | {padMiddle(f'Stat',8)} | {padMiddle('Plusy', 6)} | {padMiddle('Minusy', 8)} | {padMiddle(f'Aktywnosc',10)} | {padMiddle(f'Zachowanie',12)}|\n"
            arrayOfStrings[counter] += f"-----------------------------------------------------------------------------\n"
            for x in re:
                 print(x[0])
                 if(len(arrayOfStrings[counter]) < 1900):
                     arrayOfStrings[counter] += f" {padStart(f'{x[0]}', 11)} | {padStart(f'{x[1]}',8)} | {padStart(f'{x[2]}', 9)} | {padStart(f'{x[3]}',11)} | {padStart(f'{x[4]}', 5)} | {padStart(f'{x[5]}', 7)}\n"
                 else:
                     arrayOfStrings[counter] += '```'
                     await ctx.send(f'Dane dotyczące aktywności {tabela}u:\n{arrayOfStrings[counter]}')
                     counter += 1
                     arrayOfStrings.append('```python\n')
                     arrayOfStrings[counter] += f"{padMiddle(f'Nickname',12)} | {padMiddle(f'Stat',8)} | {padMiddle('Plusy', 6)} | {padMiddle('Minusy', 8)} | {padMiddle(f'Aktywnosc',10)} | {padMiddle(f'Zachowanie',12)}|\n"
                     arrayOfStrings[counter] += f"-----------------------------------------------------------------------------\n"
                     arrayOfStrings[counter] += f" {padStart(f'{x[0]}', 11)} | {padStart(f'{x[1]}',8)} | {padStart(f'{x[2]}', 9)} | {padStart(f'{x[3]}',11)} | {padStart(f'{x[4]}', 5)} | {padStart(f'{x[5]}', 7)}\n"



            arrayOfStrings[counter] += '```'
            await ctx.send(f'Dane dotyczące aktywności {tabela}u:\n{arrayOfStrings[counter]}')


        elif pp.lower() == 'awanse' or pp.lower() =="aw" :
            mycursor.execute(f"select  a.Nickname, a.DataAwDeg, a.Awansujacy FROM {tabela} a")
            re = mycursor.fetchall()
            print(re)

            arrayOfStrings[counter] += f"{padMiddle(f'Nickname',14)} | {padMiddle(f'DataAwDeg',12)} | {padMiddle(f'Awansujacy',22)} |\n"
            arrayOfStrings[counter] += f"-------------------------------------------------------\n"
            for x in re:
                print(x[0])
                print(x[2] is not None)
                if len(arrayOfStrings[counter])>= 1900:
                    arrayOfStrings[counter] += '```'
                    await ctx.send(f'Dane na temat awansów {tabela}u:\n{arrayOfStrings[counter]}')
                    counter += 1
                    arrayOfStrings.append('```python\n')
                    arrayOfStrings[counter] += f"{padMiddle(f'Nickname',14)} | {padMiddle(f'DataAwDeg',12)} | {padMiddle(f'Awansujacy',22)} |\n"
                    arrayOfStrings[counter] += f"-------------------------------------------------------\n"
                if x[2] is not None and ctx.message.guild.get_member(int(x[2])) is not None:
                    prin = ctx.message.guild.get_member(int(x[2]))
                    sliced = prin.nick[2:]
                    print(sliced)
                    arrayOfStrings[counter] += f" {padStart(f'{x[0]}', 13)} | {padStart(f'{x[1]}',11)} | {padStart(f'{sliced}', 22)} |\n"
                else:
                    arrayOfStrings[counter] += f" {padStart(f'{x[0]}', 13)} | {padStart(f'{x[1]}',11)} | {padStart(f'None', 22)} |\n"
            arrayOfStrings[counter] += '```'
            await ctx.send(f'Dane na temat awansów {tabela}u:\n{arrayOfStrings[counter]}')
        else:
            await ctx.send('Podaj poprawne dane!!!')
    else:
        await ctx.send('Nie znalazłem takiego oddziału')

    mycursor.close()
    conn.close()

client.run(config['TOKEN'])
