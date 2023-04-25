import os
"""Don't worry about these goofy imports, 
they are made to easily run my project on an alien cloud server 
without worrying about terminal and requirements.txt, but it will also present"""
try:
    from telegram.ext import *  # Updater, CommandHandler, MessageHandler, filters
    from telegram import *  # sendChatAction
except Exception:
    # Try harder
    os.system("pip install python-telegram-bot[ext] --upgrade")
    from telegram.ext import *
    from telegram import *
import logging
try:
    import pandas as pd
except Exception:
    # Try even harder
    os.system("pip install pandas")
    import pandas as pd
import time
try:
    import asyncio
except Exception:
    # TRY VERY-VERY HARD
    os.system("pip install asyncio")
    import asyncio
from data import db_session
try:
    import sqlalchemy as sa
    import sqlalchemy.orm as orm
    import sqlalchemy.ext.declarative as dec
except Exception:
    # NHAHHHHH
    os.system("pip install sqlalchemy")
    import sqlalchemy as sa
    import sqlalchemy.orm as orm
    import sqlalchemy.ext.declarative as dec
from data.users import Users
from data.spam_words import SpamWords
from data.groups import Group
try:
    from translate import Translator
except ModuleNotFoundError:
    os.system("pip install translate")
    from translate import Translator
try:
    import schedule
except ModuleNotFoundError:
    os.system("pip install schedule")
    import schedule
import datetime
import json
import sys

from multiprocessing import Process


EMOJIS = """😁😂😃😄😅😆😉😊😋😌😍😏😒😓😔😖😘😚😜
😝😞😠😡😢😣😤😥😨😩😪😫😭😰😱😲😳😵😷😸😹😺😻😼😽
😾😿🙀🙅🙆🙇🙈🙉🙊🙋🙌🙍🙎🙏✂✅✈✉✊✋✌✏✒✔✖✨✳✴❄❇❌
❎❓❔❕❗❤➕➖➗➡➰🚀🚃🚄🚅🚇🚉🚌🚏🚑🚒🚓🚕🚗🚙🚚
🚢🚤🚥🚧🚨🚩🚪🚫🚬🚭🚲🚶🚹🚺🚻🚼🚽🚾🛀Ⓜ🅰🅱🅾🅿🆎🆑
🆒🆓🆔🆕🆖🆗🆘🆙🆚🇩🇪🇩🇪🇩🇪🇬🇧🇬🇧🇬🇧🇨🇳🇨🇳🇨🇳🇯🇵🇯🇵🇯🇵🇰🇷🇰🇷🇰🇷🇫🇷
🇫🇷🇫🇷🇪🇸🇪🇸🇪🇸🇮🇹🇮🇹🇮🇹🇺🇸🇺🇸🇺🇸🇷🇺🇷🇺🇷🇺🈁🈂🈚🈯🈲🈳🈴🈵🈶🈷🈸🈹
🈺🉐🉑©®‼⁉#⃣#⃣#⃣™ℹ↔↕↖↗↘↙↩↪⌚⌛⏩⏪⏫⏬⏰⏳▪▫▶◀◻◼◽◾☀☁
☎☑☔☕☝☺♈♉♊♋♌♍♎♏♐♑♒♓♠♣♥♦♨♻♿⚓⚠⚡⚪⚫⚽⚾⛄⛅⛎⛔⛪⛲⛳⛵
⛺⛽⤴⤵⬅⬆⬇⬛⬜⭐⭕〰〽㊗㊙🀄🃏🌀🌁🌂🌃🌄🌅🌆🌇🌈🌉🌊🌋
🌌🌏🌑🌓🌔🌕🌙🌛🌟🌠🌰🌱🌴🌵🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂
🍃🍄🍅🍆🍇🍈🍉🍊🍌🍍🍎🍏🍑🍒🍓🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝
🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🍵🍶🍷
🍸🍹🍺🍻🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎠🎡
🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭🎮🎯🎰🎱🎲🎳🎴🎵🎶🎷🎸🎹🎺🎻
🎼🎽🎾🎿🏀🏁🏂🏃🏄🏆🏈🏊🏠🏡🏢🏣🏥🏦🏧🏨🏩🏪🏫🏬🏭🏮
🏯🏰🐌🐍🐎🐑🐒🐔🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨
🐩🐫🐬🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽🐾👀👂👃👄👅
👆👇👈👉👊👋👌👍👎👏👐👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟
👠👡👢👣👤👦👧👨👩👪👫👮👯👰👱👲👳👴👵👶👷👸👹👺👻👼
👽👾👿💀💁💂💃💄💅💆💇💈💉💊💋💌💍💎💏💐💑💒💓💔💕💖
💗💘💙💚💛💜💝💞💟💠💡💢💣💤💥💦💧💨💩💪💫💬💮💯💰💱
💲💳💴💵💸💹💺💻💼💽💾💿📀📁📂📃📄📅📆📇📈📉📊📋📌📍
📎📏📐📑📒📓📔📕📖📗📘📙📚📛📜📝📞📟📠📡📢📣📤📥📦📧
📨📩📪📫📮📰📱📲📳📴📶📷📹📺📻📼🔃🔊🔋🔌🔍🔎🔏🔐🔑🔒
🔓🔔🔖🔗🔘🔙🔚🔛🔜🔝🔞🔟🔠🔡🔢🔣🔤🔥🔦🔧🔨🔩🔪🔫🔮🔯
🔰🔱🔲🔳🔴🔵🔶🔷🔸🔹🔺🔻🔼🔽🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛
🗻🗼🗽🗾🗿😀😇😈😎😐😑😕😗😙😛😟😦😧😬😮😯😴😶🚁🚂🚆
🚈🚊🚍🚎🚐🚔🚖🚘🚛🚜🚝🚞🚟🚠🚡🚣🚦🚮🚯🚰🚱🚳🚴🚵🚷🚸
🚿🛁🛂🛃🛄🛅🌍🌎🌐🌒🌖🌗🌘🌚🌜🌝🌞🌲🌳🍋🍐🍼🏇🏉🏤🐀
🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐏🐐🐓🐕🐖🐪👥👬👭💭💶💷📬📭📯
📵🔀🔁🔂🔄🔅🔆🔇🔉🔕🔬🔭🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧"""

# Clear log files for the simplicity
with open("info.log", "w"):
    pass
with open("debug.log", "w"):
    pass
with open("error.log", "w"):
    pass


# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Create handlers for different log levels, it is made to simplify debug for me
info_handler = logging.FileHandler('info.log')
info_handler.setLevel(logging.INFO)

debug_handler = logging.FileHandler('debug.log')
debug_handler.setLevel(logging.DEBUG)

error_handler = logging.FileHandler('error.log')
error_handler.setLevel(logging.ERROR)

# Create formatter, it's beatiful! (NO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Set formatter for each handler, idk why im doing this
info_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(info_handler)
logger.addHandler(debug_handler)
logger.addHandler(error_handler)


# Load configuration from a file "config.csv", this function is also loaded when a user is sending a .csv file to a bot in private. This is very vinurable, i know
def load_config():
    global config
    try:
        config = pd.read_csv('data/config.csv')
        logger.info('Configuration file loaded.')
    except FileNotFoundError:
        logger.error('Configuration file not found.')


"""To use your token, make a file named token.csv and put it into data folder. Or you can just put it into this constant"""
TOKEN = ""
def load_token():
    global TOKEN
    try:
        with open('data/token.csv') as token_file:
            TOKEN = str(token_file.readlines()[0].strip())
        logger.info('TOKEN LOADED')
    except FileNotFoundError:
        logger.error('TOKEN NOT FOUND')


load_config()
load_token()


def translate_to_lang(update, message):
    to_lang = update.message.from_user.language_code
    translt = Translator(to_lang)
    return translt.translate(str(message))


def add_user_to_db(update, context):
    """This function is made to simplify adding new users to database."""
    session = db_session.create_session()
    
    usr = session.query(Users).filter(Users.id == update.message.from_user.id).first()
    
    if not usr:
        usr = Users(
            id=update.message.from_user.id, 
            username=update.message.from_user.username, 
            first_name=update.message.from_user.first_name, 
            is_bot=update.message.from_user.is_bot, 
            weight=0
            )
        session.add(usr)
        logging.info(f"added {update.message.from_user.username} to db")
    session.commit()
    return usr


def add_group_to_db(update, context):
    try:
        if update.message.chat.type != "private":
            session = db_session.create_session()

            group = session.query(Group).filter(Group.id == update.message.chat.id).first()

            if not group:
                group = Group(
                    id=int(update.message.chat.id),
                    is_forum=bool(update.message.chat.is_forum),
                    title=str(update.message.chat.title),
                    max_messages=int(config['max_messages']),
                    mute_duration=int(config['mute_duration'])
                    )
                session.add(group)
                logging.info(f"added {update.message.chat.title} to db")
            session.commit()
            return group
        else:
            logging.info(f"failed adding private chat to db")
            return False
    except Exception as e:
        logging.info(e.__repr__())
        return False


async def start_command(update, context):
    """Sends a diffrent greeting to a user if he is writing in private or he is using it in a group"""
    user_id = update.effective_user.id
    add_user_to_db(update, context)
    add_group_to_db(update, context)
    
    logging.info("start-taken")
    if update.message.chat.type == 'private':
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=translate_to_lang(update, "Hi, I'm an anti-spam bot. I will help you fight spam in your group chats. To add me to a group, simply add me to a group as a member and grant me administrator privileges."))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=translate_to_lang(update, "Hi, I'm an anti-spam bot. I will help you fight spam in this group chat. Please make sure I have been granted administrator privileges and that I have the permission to delete messages and ban users."))
        if update.message.chat.is_forum:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text=translate_to_lang(update, "Because I am in a forum-type group I can't manage messages properly. I am sorry for inconvenience, this will be fixed later."))
    return 1


async def help_command(update, context):
    """Sends brief info about how to properly use bot"""
    logging.info("help-taken")
    add_user_to_db(update, context)
    add_group_to_db(update, context)
    
    if update.message.chat.type == "private":
        await context.bot.send_message(chat_id=update.effective_chat.id, text=translate_to_lang(update, "To add me to a group chat, simply add me as a member and grant me administrator privileges. Once I am added, I will start monitoring the chat for spam and automatically remove any messages that contain spam words. If a user sends more than {} messages in a single chat session, they will be muted for {} minutes. To manage my settings, use the /settings command.".format(int(config['max_messages']), int(config['mute_duration']))))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=translate_to_lang(update, "If I am currently an admin in this chat, I will manage it and remove unwanted flood and spam!"))


async def settings(update, context):
    """This function changes config of a bot in groups"""
    logging.info("settings-taken")
    add_user_to_db(update, context)
    add_group_to_db(update, context)
    
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    session = db_session.create_session()
    
    # Check if the message was sent in a group chat
    if update.effective_chat.type != "private":
        # My bypass :3
        if user_id == int(config['pro_id']) and not await check_admin(update, context):
            group = session.query(Group).filter(Group.id == chat_id)
            if not group:
                group = Group(id=chat_id, max_messages=config['max_messages'], mute_duration=mute_duration)
                session.add(group)
            else:
                try:
                    group.max_messages = int(context.args[0])
                    group.mute_duration = int(context.args[1])
                except TypeError:
                    group.max_messages = config['max_messages']
                    group.mute_duration = mute_duration
                except IndexError:
                    await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, f"sempai, you have to give me the desired settings in format\n/settings [max messages per minute] [mute duration]"))
                    await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
                    return 
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, f"ok, settings updated, new settings are \n\t{context.args[0]} max messages;\n\t{context.args[1]} mute duration"))
            return
        
        # Check if the user is an admin of the group chat
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if type(chat_member) not in [ChatMemberAdministrator, ChatMemberOwner]:
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "You need to be an admin of this group to use this command."), reply_to_message_id=update.message.message_id)
            return
        
        # Check if the arguments are valid
        try:
            max_messages = int(context.args[0])
            mute_duration = int(context.args[1])
            if max_messages <= 0 or mute_duration <= 0:
                raise ValueError()
        except ValueError:
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "Invalid arguments. Please provide two positive integers. Arguments should be positive."), reply_to_message_id=update.message.message_id)
            return
        except IndexError:
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "Invalid arguments. Please provide two positive integers. They should follow the following format:\n\t\t/settings [max_messages] [mute_duration]"), reply_to_message_id=update.message.message_id)
            return 
        
        # Update the settings for the group in the database
        # I'm not using the predefined function called add_group_to_db because I am changing params in action
        group = session.query(Group).filter(Group.id == chat_id).first()
        session.add(group)
        if not group:
            group = Group(
                    id=int(update.message.chat.id),
                    is_forum=bool(update.message.chat.is_forum),
                    title=str(update.message.chat.title),
                    max_messages=int(max_messages),
                    mute_duration=int(mute_duration)
                    )
        else:
            group.max_messages = max_messages
            group.mute_duration = mute_duration
        
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, f"Settings for this group successfully updated!\nNew settings are {max_messages} max messages and mute duration of {mute_duration} minutes!"))
    
    # If the message was sent in a private chat, inform the user that they cannot use this command
    else:
        if user_id == int(config['pro_id']):  # My bypass :3 It allows to edit global settings in action
            try:
                max_messages = int(context.args[0])
                mute_duration = int(context.args[1])
                if max_messages <= 0 or mute_duration <= 0:
                    raise ValueError()
            except ValueError:
                await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "Invalid arguments. Please provide two positive integers. Arguments should be positive."), reply_to_message_id=update.message.message_id)
                return
            except IndexError:
                await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "Invalid arguments. Please provide two positive integers. They should follow the following format:\n\t\t/settings [max_messages] [mute_duration]"), reply_to_message_id=update.message.message_id)
                return 
            config['max_messages'] = max_messages
            config['mute_duration'] = mute_duration
            config.to_csv("data/config.csv")
            load_config()
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, f"Current settings are:\n\t\t· {int(config['max_messages'])} max messages per minute\n\t\t· {int(config['mute_duration'])} minutes mute duration"))
    session.commit()
    return 1
        

async def config_update(update, context):  # nan -status
    logging.info("begin")
    user_id: int = update.message.from_user.id
    chat_id: int = update.message.chat.id
    is_admin: bool = await check_admin(update, context)
    
    if update.message.chat.type == "private" and update.message.from_user.id != int(config['pro_id']):
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "You have to use this command in a group. You can add me to a group just simply inviting me to it. You will also have to grant me admin priveleges in order for this bot to function properly."))
        return ConversationHandler.END
    
    reply_keyboard = [[translate_to_lang(update, "✅"), translate_to_lang(update, "⛔️")]]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    await context.bot.send_message(chat_id=update.message.chat.id, text=translate_to_lang(update, "To configure this bot for the current group you have to answer to some questions related to this. Continue? "), reply_markup=markup)
    return 1


async def config_stop(update, context):  # 0 -status
    logging.info("0")
    session = db_session.create_session()
    
    await context.bot.send_message(chat_id=update.message.chat.id, text=translate_to_lang(update, f"Ok, default configuration will be applied to the current group! The default configuration is {int(config['max_messages'])} messages per minute and mute duration of {int(config['mute_duration'])} minutes"), reply_markup=ReplyKeyboardRemove())
    
    group = session.query(Group).filter(Group.id == update.message.chat.id)
    if not group:
        group = Group(id=update.message.chat.id, is_forum=update.message.chat.is_forum, max_messages=config['max_messages'], mute_duration=mute_duration, title=update.message.chat.title)
        session.add(group)
    else:
        group.max_messages = config['max_messages']
        mute_duration = config['mute_duration']
    
    session.commit()
    return ConversationHandler.END


async def starting_config(update, context):  # 3 -status
    logging.info("3")
    if update.message.text == "✅":
        return 1
    elif update.message.text == "⛔️":
        await config_stop(update, context)
        return ConversationHandler.END


async def first_response_config(update, context):  # 1 -status
    logging.info("1")
    session = db_session.create_session()
    
    if update.message.text.strip() == "⛔️":
        await config_stop(update, context)
        return ConversationHandler.END
    
    reply_keyboard = [["2", "3", "5"], ["10", "15", "20"], ["30", "40", "60"], ["⛔"]]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    
    await context.bot.send_message(chat_id=update.message.chat.id, text=translate_to_lang(update, f"First you have to specify, how much messages per minute is normal"), reply_markup=markup)
    session.commit()
    return 2


async def second_response_config(update, context):  # 2 -status
    logging.info("2")
    session = db_session.create_session()
    try:
        max_messages = int(str(update.message.text).strip())
    except Exception as e:
        await config_stop(update, context)
        return ConversationHandler.END
    
    group = add_group_to_db(update, context)
    session.add(group)
    group.max_messages = max_messages
    
    reply_keyboard = [["1", "2", "3"], ["5", "10", "15"], ["30", "45", "60"], ["⛔"]]
    markup = ReplyKeyboardMarkup(reply_keyboard)
    
    await context.bot.send_message(chat_id=update.message.chat.id, text=translate_to_lang(update, f"Then, for how long do I have to mute spammers? (in minutes)"), reply_markup=markup)
    session.commit()
    return 4


async def third_response_config(update, context):  # 4 -status
    logging.info("4")
    session = db_session.create_session()
    try:
        mute_duration = int(str(update.message.text).strip())
    except Exception as e:
        await config_stop(update, context)
        return ConversationHandler.END
    group = add_group_to_db(update, context)
    session.add(group)
    group.mute_duration = mute_duration
    
    await context.bot.send_message(chat_id=update.message.chat.id, text=translate_to_lang(update, f"Ok, everything is set up! Now I will follow this configuration:\n\t\t·{group.max_messages} max messages per minute\n\t\t·{group.mute_duration} minutes mute duration"), reply_markup=ReplyKeyboardRemove())
    session.commit()
    return ConversationHandler.END


async def check_admin(update, context):
    chat_member = await context.bot.get_chat_member(update.message.chat.id, update.message.from_user.id)
    if type(chat_member) in [ChatMemberAdministrator, ChatMemberOwner]:
        return True
    return False


def has_too_many_emojis(text, threshold=0.8):
    """
    Checks if a message has too many emojis.
    Returns True if the percentage of emojis in the text
    is greater than or equal to the specified threshold, False otherwise.
    """
    emoji_count = sum([1 for c in text if c in EMOJIS])
    total_chars = len(text)
    if total_chars == 1:
        return False
    emoji_ratio = emoji_count / total_chars
    return emoji_ratio >= threshold



def has_too_many_caps(text, threshold=0.7):
    """
    Checks if a message has too many capitalized letters.
    Returns True if the percentage of capitalized letters in the text
    is greater than or equal to the specified threshold, False otherwise.
    """
    text.replace(' ', '')
    caps_count = sum([1 for c in text if c.isupper()])
    total_chars = len(text)
    caps_ratio = caps_count / total_chars
    if caps_ratio == 1.0:
        return False  # You wouldn't understand.... Sometimes you need to go into battle-mode
    return caps_ratio >= threshold


async def check_spam(update, context):
    logging.info("check-spam")
    session = db_session.create_session()
    
    current_group = add_group_to_db(update, context)
    if update.message.chat.type == "private":  # User is writing in private -> I don't filter and just say him to add me to a group in order for me to work properly
        await start_command(update, context)
        logging.info("user was writing in private")
        return 

    user_id: int = update.message.from_user.id
    chat_id: int = update.message.chat.id
    is_admin: bool = await check_admin(update, context)
    
    usr: Users = add_user_to_db(update, context)
    
    session.add(usr)
    session.add(current_group)
    
    if (update.message.text and not update.message.photo) or update.message.from_user.is_bot:  # If a message is plain text or it was sent from a bot
        spam_words: list = session.query(SpamWords).all()
        
        for spam_word in spam_words:
            if spam_word.word in update.message.text.lower().replace(',', ''). replace('.', '').replace(':', '').replace('!', '').replace('?', '').replace('/', ''):
                # The following part of code is intended to use when a user has been spamming(advertising) in a group
                try:
                    await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
                    await context.bot.send_message(chat_id=update.message.from_user.id, text=translate_to_lang(update, "Your message contained spam and has been deleted."))  # This is done in private message to a user
                    await context.bot.send_message(chat_id=update.message.from_user.id, text=translate_to_lang(update, f"You better don't use word {spam_word.word}"))
                except Exception as e:
                    logging.info("couldn't initiate conversation with spammer")
                if not is_admin:
                    usr.weight += spam_word.weight

        if has_too_many_caps(update.message.text):
            await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
            await context.bot.send_message(chat_id=update.message.from_user.id, text=translate_to_lang(update, "Your message contained too many capitalized letters"))
        elif has_too_many_emojis(update.message.text):
            await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
            await context.bot.send_message(chat_id=update.message.from_user.id, text=translate_to_lang(update, "Your message contained too many emojis"))
    
    elif update.message.sticker:  # If a message is a sticker
        if not is_admin:
            if update.message.sticker.is_animated:
                usr.weight += 1
            usr.weight += 1
    elif update.message.animation:  # If a message is a gif
        if not is_admin:
            usr.weight += 1
    elif update.message.photo:
        pass
    else:
        logging.info('IF YOU SEE THIS MESSAGE, SOMETHING IS WRONG. YOU HAVE SUCCSESSFULLY BROKEN MY BOT.\nThere might be another type of message, which isn\'t prosessed properly')
    
    if usr.weight > current_group.max_messages:
        try:
            if not await check_admin(update, context):
                await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, until_date=int(time.time() + current_group.mute_duration * 60), permissions=None)
            usr.weight = 0
        except Exception as e:
            logging.info(e.__repr__())
            return 0
        try:
            await context.bot.send_message(chat_id=user_id, text=translate_to_lang(update, "You have been muted for {} minutes for spamming. Please make sure to read the group rules and avoid sending too many messages in a single chat session.".format(current_group.mute_duration)))
        except Exception as e:
            logging.info("couldn't initiate conversation with user")
    
    session.commit()
    return 1


async def add_spam_word(update, context):
    session = db_session.create_session()
    is_admin = await check_admin(update, context)
    if update.message.from_user.id != int(config['pro_id']) or update.effective_chat.type != "private":  # editing global config
        await context.bot.send_message(chat_id=update.message.chat.id, text=translate_to_lang(update, "you don't have enough rights to edit global config of a bot"), reply_to_message_id=update.message.message_id)
        return 0
    try:
        spam_word = str(context.args[0])
        spam_word.replace('\"', '')
        spam_word.replace('\'', '')
    except TypeError or ValueError:
        await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, "incorrect format for a spam_word"))
        return 0
    try: 
        spam_word_weight = int(context.args[1])
    except ValueError:
        await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, "incorrect format for a weight of a spam word"))
        return 0
    word = session.query(SpamWords).filter(SpamWords.word == spam_word).first()
    if not word:
        word = SpamWords(word=spam_word, weight=spam_word_weight)
        session.add(word)
        await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, f"successfully added word {spam_word}"))
    else:
        await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, "this word already present in the database"))
        return 0
    session.commit()
    return 1


async def load_json(update, context):
    """
    This function should define if a file is called "config.json" or "config.csv"
    and load this config
    else it should raise up check_spam function
    this function isn't written now
    """
    await check_spam(update, context)


def clear_weight():
    logging.info("clearing weights")
    
    session = db_session.create_session()
    all_users = session.query(Users).all()
    
    logging.info(len(all_users))
    
    for user in all_users:
        user.weight = 0
        logging.info(f"Set weight of {user.username} to {user.weight}")
        # Add each user object to the session individually
        session.add(user)
    session.commit()
    return 1



def clear_weight_process():
    while True:
        clear_weight()
        time.sleep(60)


def error(update, context):
    logging.error('Update "%s" caused error "%s"', update, context.error)


async def stop_bot(update, context):
    """This is a dev function to easily restart bot on a docker-server"""
    if update.message.from_user.id == int(config['pro_id']) and update.message.chat.type == "private":
        sys.exit(1)


# Define main function
def main():
    config_handler = ConversationHandler(
        entry_points=[
            CommandHandler("cfg", config_update), 
            CommandHandler("configure", config_update), 
            CommandHandler("config", config_update)
        ], 
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, first_response_config)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, second_response_config)],
            3: [MessageHandler(filters.TEXT & ~filters.COMMAND, starting_config)],
            4: [MessageHandler(filters.TEXT & ~filters.COMMAND, third_response_config)]
        }, 
        fallbacks=[
            CommandHandler("stop_cfg", config_stop),
            MessageHandler("STOP", config_stop),
            MessageHandler("⛔️", config_stop)
        ]
    )
    
    queue = asyncio.Queue(maxsize=100)
    application = Application.builder().token(token=TOKEN).build()

    # Add handlers
    application.add_handlers([
        config_handler,  # Better config editor
        MessageHandler(filters.ATTACHMENT & ~filters.TEXT & ~filters.COMMAND & ~filters.PHOTO, load_json),  # load json
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CommandHandler("settings", settings),
        CommandHandler("add_spam_word", add_spam_word),
        CommandHandler("stop", stop_bot),
        MessageHandler(filters.ALL & ~filters.COMMAND, check_spam)
        # MessageHandler(filters.ALL, error)
    ])

    p1 = Process(target=application.run_polling)
    p1.start()
    
    p2 = Process(target=clear_weight_process)
    p2.start()
    
    p1.join()
    p2.join()


if __name__ == '__main__':
    logging.info(db_session.global_init("db/spam_bot.db"))
    print('SUCCESS')
    main()
