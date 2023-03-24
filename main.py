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
    session.close()
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
            session.close()
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
        # I'm not using the predefined function called ad_group_to_db because I am changing params in action
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
        if user_id == int(config['pro_id']):  # My bypass :3
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "YES, MY MASTER, YOU CAN DO EVERYTHING WITH ME. \nAHHHHH!!!!!\nBUT YOU ALSO CAN'T UPDATE GLOBAL SETTINGS!!\nnyeh-heh-heh\nNYEH-HEH-HEH!"))
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "You cannot edit the global settings of this bot."))
    session.commit()
    return 1
        

async def config_update(update, context):
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    session = db_session.create_session()
    if update.message.document.mime_type == 'text/csv':
        try:
            file_id = update.message.document.file_id
            new_config_file = await context.bot.get_file(file_id)
            new_config = pd.read_csv(new_config_file)
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, f"The configuration is wrong. The error \'{e}\' has happend. Check if the file is .csv"))
        global config, max_messages, mute_duration
        config = new_config
        max_messages = config['max_messages'].iloc[0]
        mute_duration = config['mute_duration'].iloc[0]
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "The bot configuration has been updated."))
        logging.info(f"Bot configuration has been updated by {user_id}")
    else:
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "The file you sent is not a CSV file."))
        logging.info(
            f"{user_id} attempted to update bot configuration with a non-CSV file.")
        return 0
    session.commit()
    return 1


async def check_admin(update, context):
    chat_member = await context.bot.get_chat_member(update.message.chat.id, update.message.from_user.id)
    if type(chat_member) in [ChatMemberAdministrator, ChatMemberOwner]:
        return True
    return False


async def check_spam(update, context):
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
            if spam_word.word in update.message.text.lower().replace(',', ''). replace('.', '').replace(':', '').replace('!', '').replace('?', '').replace('/', '').split(' '):
                await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)  # This is done in current chat
                await context.bot.send_message(chat_id=update.message.from_user.id, text=translate_to_lang(update, "Your message contained spam and has been deleted."))  # This is done in private message to a user
                await context.bot.send_message(chat_id=update.message.from_user.id, text=translate_to_lang(update, f"You better don't use word {spam_word.word}"))
                logging.info("deleted a message")
                if not is_admin:
                    usr.weight += spam_word.weight
                    
        logging.info('text')
    
    elif update.message.sticker:  # If a message is a sticker
        if not is_admin:
            if update.message.sticker.is_animated:
                usr.weight += 1
            usr.weight += 1
        logging.info('sticker')
        # await context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
    elif update.message.animation:  # If a message is a gif
        if not is_admin:
            usr.weight += 1
        logging.info('gif')
    elif update.message.photo:
        logging.info('photo')
    else:
        logging.info('IF YOU SEE THIS MESSAGE, SOMETHING IS WRONG. YOU HAVE SUCCSESSFULLY BROKEN MY BOT.\nThere might be another type of message, which isn\'t prosessed properly')
    
    logging.info(f"{current_group.max_messages} -> {usr.weight}")
    if usr.weight > current_group.max_messages:
        logging.info(f'trying to punish {update.message.from_user.username}')
        try:
            if not await check_admin(update, context):
                await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, until_date=int(time.time() + current_group.mute_duration * 60), permissions=None)
                logging.info(f"muted {update.message.from_user.username} for {current_group.mute_duration} minutes")
            else:
                logging.info(f"admin of a group tries to spam but he can't be muted :(")
            usr.weight = 0
            logging.info(f"now weight for {update.message.from_user.username} is {usr.weight}")
        except Exception as e:
            logging.info(e.__repr__())
            return 0
        await context.bot.send_message(chat_id=user_id, text=translate_to_lang(update, "You have been muted for {} minutes for spamming. Please make sure to read the group rules and avoid sending too many messages in a single chat session.".format(current_group.mute_duration)))
    session.commit()
    return 1


async def add_spam_word(update, context):
    session = db_session.create_session()
    is_admin = await check_admin(update, context)
    if update.message.from_user.id != int(config['pro_id']) or update.effective_chat.type != "private":  # editing global config
        logging.info('not enough rights')
        await context.bot.send_message(chat_id=update.message.chat.id, text=translate_to_lang(update, "you don't have enough rights to edit global config of a bot"), reply_to_message_id=update.message.message_id)
        return 0
    try:
        spam_word = str(context.args[0])
        spam_word.replace('\"', '')
        spam_word.replace('\'', '')
    except TypeError or ValueError:
        logging.info("taken incorrect spam_word")
        await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, "incorrect format for a spam_word"))
        return 0
    try: 
        spam_word_weight = int(context.args[1])
    except ValueError:
        logging.info("taken incorrect weight")
        await context.bot.send_messag(chat_id=int(config['pro_id']), text=translate_to_lang(update, "incorrect format for a weight of a spam word"))
        return 0
    word = session.query(SpamWords).filter(SpamWords.word == spam_word).first()
    if not word:
        word = SpamWords(word=spam_word, weight=spam_word_weight)
        session.add(word)
        await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, f"successfully added word {spam_word}"))
    else:
        logging.info("word already present")
        await context.bot.send_message(chat_id=int(config['pro_id']), text=translate_to_lang(update, "this word already present in the database"))
        return 0
    session.commit()
    return 1


def error(update, context):
    logging.error('Update "%s" caused error "%s"', update, context.error)


# Define main function
def main():
    queue = asyncio.Queue(maxsize=100)
    application = Application.builder().token(token=TOKEN).build()

    # Add handlers
    application.add_handlers([
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CommandHandler("settings", settings),
        CommandHandler("add_spam_word", add_spam_word),
        MessageHandler(filters.ALL & ~filters.COMMAND, check_spam),
        # MessageHandler(filters.ALL, error)
    ])

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    logging.info(db_session.global_init("db/spam_bot.db"))
    main()
