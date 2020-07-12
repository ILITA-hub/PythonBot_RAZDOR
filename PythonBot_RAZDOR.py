import random
import discord
import asyncio
import requests
import bs4
from bs4 import SoupStrainer
import datetime
import pickle
import os
# import mydata

DISCORD_BOT_TOKEN = 'NTk5MTU5MDY3OTU2NjA5MDMz.XWjN6A.GsFvA9wHsoVt1vHUaTXcKmUwdpM'
DISCORD_BOT_CHATID = '<@!599159067956609033>'
DATA_FILE = 'Bot_RAZDOR_data.txt'
TMP_PIC = 'Bot_RAZDOR_temp_picture'

INTERES_ROLE_NAME = 'ᅠᅠᅠᅠᅠИнтересыᅠᅠᅠᅠᅠᅠ'
MY_GUILD_ID = '307487249933664267'
MY_CHANNEL_ID = '661142202671693834'
MY_CHANNEL_PRIME_ID = '720984648381104210'

EMOJI_SPECIAL = 'bot_interest_'
BOT_PREF = 'lox'

client = discord.Client()


def START():
    LOGprint("ЗАПУСКАЮСЬ, ЖДИ")
    # data = mydata.data_class()
    # BOT_PREF2 = data.get_param_value('BOT_PREF')
    s = 1
    client.run(DISCORD_BOT_TOKEN)


def data_get():
    data = {'message_to_watch': '', 'dop_data': ''}

    if not os.path.isfile(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        with open(DATA_FILE, 'wb') as f:
            pickle.dump(data, f)

        return data

    with open(DATA_FILE, 'rb') as f:
        data = pickle.load(f)

    return data


def data_set(data):
    with open(DATA_FILE, 'wb') as f:
        pickle.dump(data, f)


def LOGprint(str1, end=''):
    print('[' + str(datetime.datetime.time(datetime.datetime.now())) + '] ' + str(str1), end)


def MSG_SEND(channel, message):
    LOGprint(message)
    return channel.send(message)


def ChitoNaAve(Member):
    PROP = ' '
    NaAve = 'Кажется, на аве'
    url = Member.avatar_url._url
    url = 'https://cdn.discordapp.com/avatars/' + str(Member.id) + '/' + Member.avatar
    print(url)

    Checking_url = 'https://yandex.ru/images/search?source=collections&rpt=imageview&url=' + url

    request = requests.get(Checking_url)
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    contenty = bs.find("div", {"class": "Tags Tags_type_simple"}).contents

    for tag in contenty:
        NaAve = NaAve + PROP + tag.text
        PROP = ', '

    print(NaAve)

    return NaAve


async def AnimeNaAveMatVKanave(Member, Guild):
    NaAve = ChitoNaAve(Member)
    Role = discord.utils.get(Guild.roles, name="Аниме на аве, мать в канаве")
    Message = Member.name
    RoleList = [Role]

    if NaAve.lower().find('anime') > -1 or NaAve.lower().find('аниме') > -1:
        if Role in Member.roles:
            Message = Message + '    аниме'

        else:
            Message = Message + '    аниме роль установлена'
            res = await Member.add_roles(Role)  # 'Аниме на аве!'


    else:
        if Role in Member.roles:
            Message = Message + '    неани роль снята'
            res = await Member.remove_roles(Role)  # 'Аниме на аве отсутствует!'

        else:
            Message = Message + '    неани'

    print(Message)


async def get_my_message(data, my_channel):
    my_message_id = data['message_to_watch']
    need_to_resent = False

    if my_message_id == '':
        need_to_resent = True

    try:
        my_message = await my_channel.fetch_message(my_message_id)

    except discord.errors.NotFound:
        need_to_resent = True

    if need_to_resent:
        my_message = await my_channel.send('О даа закидай меня своими эмоджи')
        data['message_to_watch'] = my_message.id
        data_set(data)

    return my_message


def get_role_by_name(Guild, Name):
    roles = Guild.roles
    for role in roles:
        if role.name == Name:
            return role


async def interes_add(data, guild, name, emoji_pic_url, roles=None, reason=None):
    # with open(emoji_pic, "rb") as image:
    #    emoji_pic = image

    response = requests.get(emoji_pic_url)
    with open(TMP_PIC, 'wb') as file:
        file.write(response.content)

    with open(TMP_PIC, 'rb') as file:
        readed_file = file.read()
        emoji_pic = bytearray(readed_file)

    new_emoji_name = EMOJI_SPECIAL + name
    new_emoji = await guild.create_custom_emoji(name=new_emoji_name, image=emoji_pic, roles=roles, reason=reason)

    Interes_base_role = get_role_by_name(guild, INTERES_ROLE_NAME)

    new_role = await guild.create_role(name=name, mentionable=True, reason=reason)
    await new_role.edit(position=Interes_base_role.position)

    await update_serv_message(data)

    LOGprint('Загружена эможди ' + new_emoji_name + ' ' + reason)


async def update_serv_message(data):
    my_channel = client.get_channel(int(MY_CHANNEL_PRIME_ID))
    my_message = await get_my_message(data, my_channel)

    emojis = my_channel.guild.emojis

    data['emojis'] = []

    for emoji in emojis:
        if emoji.name.find(EMOJI_SPECIAL) > -1:
            await my_message.add_reaction(emoji)
            data['emojis'].append(emoji.id)

    data_set(data)


@client.event
async def on_ready():
    data = data_get()

    activity = discord.Game("Дегродация")
    await client.change_presence(status=discord.Status.idle, activity=activity)

    await update_serv_message(data)

    LOGprint('ГОТОВ РАБОТАТЬ ☭')
    LOGprint(client.user.name)
    LOGprint(client.user.id)
    LOGprint('--------------')

mas = ["й","Слышь","ы"]
@client.event
async def on_message(message):
    egor = 0
    data = data_get()
    egor_bot = DISCORD_BOT_CHATID
    if message.channel.name == 'бот':
        if message.author.discriminator != "4351" and message.author.name != "Lazychock":
            if message.content.startswith('Чмо' + ' help'):
                await message.channel.send('Я не знаю команд')

            # elif message.content.startswith(DISCORD_BOT_CHATID + ' кинь ту гифку ну эт самую, ну крч ты понял'):
            #     file = discord.File('E:\\Новая папка\\397387805.gif', 'Ты, бьющийся головой об стену.gif')
            #     await message.channel.send('Эту?', file=file)

            elif message.content.startswith('Подскажи аниме'):
                await message.channel.send('Нахуй иди тупой анимешник')

            elif message.content.startswith('О великий робот! Скинь авы упомянутых пользователей!'):
                for member in message.mentions:
                    url = 'https://cdn.discordapp.com/avatars/' + str(member.id) + '/' + member.avatar
                    await message.channel.send(url)
                    print(url)

            elif message.content.startswith('О великий робот! Что у меня на аве?'):
                NaAve = ChitoNaAve(message.author)
                await message.channel.send(NaAve)

            elif message.content.startswith('О великий робот! Что на аве?'):
                NaAve = ChitoNaAve(message.mentions[0])
                await message.channel.send(NaAve)


            elif message.content.startswith('О великий робот! Проверь всех!'):
                for guild in client.guilds:
                    for member in guild.members:
                        await AnimeNaAveMatVKanave(member, guild)


            elif message.content.startswith('О великий робот! Проверь'):
                for member in message.mentions:
                    await AnimeNaAveMatVKanave(member, member.guild)


            elif message.content.startswith(BOT_PREF + ' добавь интерес'):
                Interes = message.content[message.content.find('интерес') + 8:]

                if (Interes):
                    if (message.attachments.__len__):
                        Interes_picture = message.attachments[0].url;
                        await interes_add(data, message.guild, Interes, Interes_picture, None,
                                          reason='Создано ботом по сообщению пользователя ' + message.author.name)

                    else:
                        message.channel.send('Нужно добавить картинку!')
            else :
                userMessage = message.content
                while egor < len(mas):
                    if mas[egor] in userMessage:
                        await message.channel.send("Cам ты " + mas[egor])
                        break
                    egor = egor + 1



@client.event
async def on_raw_reaction_add(payload):
    data = data_get()

    if payload.message_id == data['message_to_watch']:
        my_channel = client.get_channel(payload.channel_id)
        my_messge = await my_channel.fetch_message(payload.message_id)

        if payload.member != my_messge.author:
            if payload.emoji.id in data['emojis']:
                role_name = payload.emoji.name[len(EMOJI_SPECIAL):]
                role = get_role_by_name(my_channel.guild, role_name)
                await payload.member.add_roles(*[role], reason=None, atomic=True)


# @client.event
# async def on_raw_reaction_remove(payload):

# data = data_get()

# if payload.message_id == data['message_to_watch']:
#    my_channel = client.get_channel(payload.channel_id)
#     my_messge = await my_channel.fetch_message(payload.message_id)
#    await my_messge.remove_reaction(payload.emoji, my_messge.author)


START()
