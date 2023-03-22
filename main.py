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
        TOKEN = pd.read_csv('data/token.csv')
        logger.info('TOKEN LOADED')
    except FileNotFoundError:
        logger.error('TOKEN NOT FOUND')


load_config()
load_token()


# Define global variables, don't worry, they are fine
max_messages = config['max_messages'].iloc[0]
mute_duration = config['mute_duration'].iloc[0]


def add_user_to_db(update, context):
    """This function is made to simplify adding new users to database."""
    session = db_session.create_session()
    
    usr = session.query(Users).filter(Users.id == user_id).first()
    
    if not usr:
        usr = Users(id=user_id, username=update.message.from_user.username, weight=0)
        session.add(usr)
        logging.info(f"added {update.message.from_user.username} to db")
        session.commit()


async def start_command(update, context):
    """Sends a diffrent greeting to a user if he is writing in private or he is using it in a group"""
    user_id = update.effective_user.id
    add_user_to_db(update, context)
    
    logging.info("start-taken")
    if update.message.chat.type == 'private':
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Hi, I'm an anti-spam bot. I will help you fight spam in your group chats. To add me to a group, simply add me to a group as a member and grant me administrator privileges.")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Hi, I'm an anti-spam bot. I will help you fight spam in this group chat. Please make sure I have been granted administrator privileges and that I have the permission to delete messages and ban users.")


async def help_command(update, context):
    """Sends brief info about how to properly use bot"""
    logging.info("help-taken")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="To add me to a group chat, simply add me as a member and grant me administrator privileges. Once I am added, I will start monitoring the chat for spam and automatically remove any messages that contain spam words. If a user sends more than {} messages in a single chat session, they will be muted for {} minutes. To manage my settings, use the /settings command.".format(max_messages, mute_duration))


async def settings(update, context):
    """This function changes config of a bot in groups"""
    logging.info("settings-taken")
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    session = db_session.create_session()
    
    # Check if the message was sent in a group chat
    if update.effective_chat.type != "private":
        # My bypass :3
        if user_id == 774301386:
            group = session.query(Group).get(chat_id)
            if not group:
                group = Group(id=chat_id, max_messages=max_messages, mute_duration=mute_duration)
                session.add(group)
            else:
                try:
                    group.max_messages = int(context.args[0])
                    group.mute_duration = int(context.args[1])
                except TypeError:
                    group.max_messages = max_messages
                    group.mute_duration = mute_duration
            await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
            await context.bot.send_message(chat_id=774301386, text=f"ok, settings updated, new settings are \n\t{context.args[0]} max messages;\n\t{context.args[1]} mute duration")
            session.commit()
            return
        
        # Check if the user is an admin of the group chat
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if type(chat_member) not in [ChatMemberAdministrator, ChatMemberOwner]:
            await context.bot.send_message(chat_id=chat_id, text="You need to be an admin of this group to use this command.", reply_to_message=update.message.message_id)
            return
        
        # Check if the arguments are valid
        try:
            max_messages = int(context.args[0])
            mute_duration = int(context.args[1])
            if max_messages <= 0 or mute_duration <= 0:
                raise ValueError()
        except:
            await context.bot.send_message(chat_id=chat_id, text="Invalid arguments. Please provide two positive integers.")
            return
        
        # Update the settings for the group in the database
        group = session.query(Group).get(chat_id)
        if not group:
            group = Group(id=chat_id, max_messages=max_messages, mute_duration=mute_duration)
            session.add(group)
        else:
            group.max_messages = max_messages
            group.mute_duration = mute_duration
        session.commit()
        
        await context.bot.send_message(chat_id=chat_id, text=f"Settings for this group successfully updated!\nNew settings are {max_messages} max messages and mute duration of {mute_duration}!")
    
    # If the message was sent in a private chat, inform the user that they cannot use this command
    else:
        if user_id == 774301386:
            await context.bot.send_message(chat_id=chat_id, text="YES, MY MASTER, YOU CAN DO EVERYTHING WITH ME. \nAHHHHH!!!!!\nBUT YOU ALSO CAN'T UPDATE GLOBAL SETTINGS!!\nnyeh-heh-heh\nNYEH-HEH-HEH!")
        await context.bot.send_message(chat_id=chat_id, text="You cannot edit the global settings of this bot.")
        

async def config_update(update, context):
    """Updates the bot configuration with a new CSV file.
    This is a very goofy function so I don't recommend using it anyway.
    It uses global variables, so it isn't very good."""
    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    session = db_session.create_session()
    if update.message.document.mime_type == 'text/csv':
        try:
            file_id = update.message.document.file_id
            new_config_file = await context.bot.get_file(file_id)
            new_config = pd.read_csv(new_config_file)
        except Exception as e:
            await context.bot.send_message(chat_id=chat_id, text=f"The configuration is wrong. The error \'{e}\' has happend. Check if the file is .csv")
        global config, max_messages, mute_duration
        config = new_config
        max_messages = config['max_messages'].iloc[0]
        mute_duration = config['mute_duration'].iloc[0]
        await context.bot.send_message(chat_id=chat_id, text="The bot configuration has been updated.")
        logging.info(f"Bot configuration has been updated by {user_id}")
    else:
        await context.bot.send_message(chat_id=chat_id, text="The file you sent is not a CSV file.")
        logging.info(
            f"{user_id} attempted to update bot configuration with a non-CSV file.")


async def check_spam(update, context):
    message = update.message.text.lower()
    user_id = update.message.from_user.id
    chat_id = update.effective_chat.id

    session = db_session.create_session()

    # Count the number of times a user has sent a message
    usr = session.query(Users).filter(Users.id == user_id).first()
    logging.info(f"{usr}, {user_id}")
    
    if not usr:
            usr = Users(id=user_id, username=update.message.from_user.username, weight=0)
            session.add(usr)
    session.commit()
    bad_words = session.query(SpamWords).all()
    for word in message.split(' '):
        for bad_word in bad_words:
            if str(word) == str(bad_word.word):
                usr.weight += int(bad_word.weight)
                logging.info(f"Message from {user_id} contained {word} and was added {bad_word.weight}")
                await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
                await context.bot.send_message(chat_id=user_id, text="Your message contained spam and has been deleted.")
                logging.info(f"deleted a message \"{message}\"")
    chat_member = await context.bot.get_chat_member(chat_id, user_id)
    if type(chat_member) not in [ChatMemberAdministrator, ChatMemberOwner]:  # Admins can send as many messages as they want
        usr.weight += 1
    if usr.weight > max_messages:
        await context.bot.delete_message(chat_id=chat_id, message_id=update.message.message_id)
        try:
            await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, until_date=int(time.time() + mute_duration * 60), permissions=None)
            logging.info(f"muted {user_id} for {mute_duration} minutes")
            usr.weight = 0
            logging.info(f"now weight for {user_id} is {usr.weight}")
        except Exception as e:
            logging.info(f"admin of a group tries to spam but he can't be muted :(")
            logging.info(f"error is {e} which has type {type(e)}")
        await context.bot.send_message(chat_id=user_id, text="You have been muted for {} minutes for spamming. Please make sure to read the group rules and avoid sending too many messages in a single chat session.".format(mute_duration))
    session.commit()


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
        MessageHandler(filters.TEXT & ~filters.COMMAND, check_spam),
        MessageHandler(filters.ALL, error)
    ])

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    db_session.global_init("db/spam_bot.db")
    main()
