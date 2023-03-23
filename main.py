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

"""
GIF:
Update(
    message=Message(
        animation=Animation(
            duration=6, 
            file_id='CgACAgQAAxkBAAOBZBvgVSOj6mKt6D98zoJgOHZWH5EAAukCAAIlYXxSh9P9nlaQIqwvBA', 
            file_name='mp4.mp4', 
            file_size=76345, 
            file_unique_id='AgAD6QIAAiVhfFI', 
            height=122, 
            mime_type='video/mp4', 
            width=166), 
        channel_chat_created=False, 
        chat=Chat(
            first_name='PhantomPixie', 
            id=6258736196, 
            type=<ChatType.PRIVATE>, 
            username='phantom_pixie'), 
        date=datetime.datetime(2023, 3, 23, 5, 15, 1, tzinfo=<UTC>), 
        delete_chat_photo=False, 
        document=Document(
            file_id='CgACAgQAAxkBAAOBZBvgVSOj6mKt6D98zoJgOHZWH5EAAukCAAIlYXxSh9P9nlaQIqwvBA', 
            file_name='mp4.mp4', 
            file_size=76345, 
            file_unique_id='AgAD6QIAAiVhfFI', 
            mime_type='video/mp4'), 
        from_user=User(
            first_name='PhantomPixie', 
            id=6258736196, 
            is_bot=False, 
            language_code='en', 
            username='phantom_pixie'), 
            group_chat_created=False, 
            message_id=129, 
            supergroup_chat_created=False), 
        update_id=326301465)
STICKER:
message=Message(
    channel_chat_created=False, 
    chat=Chat(
        first_name='-y', 
        id=774301386, 
        type=<ChatType.PRIVATE>, 
        username='igamamaev'), 
    date=datetime.datetime(2023, 3, 23, 5, 31, 23, tzinfo=<UTC>), 
    delete_chat_photo=False, 
    from_user=User(
        first_name='-y', 
        id=774301386, is_bot=False, 
        language_code='en', 
        username='igamamaev'), 
    group_chat_created=False, 
    message_id=138, 
    sticker=Sticker(
        api_kwargs={'thumbnail': {'file_id': 'AAMCAgADGQEAA4pkG-QrLp0KWbL5KAABC3tYwD5hhQEAAh8OAAIUavhInRN6ucIJPC8BAAdtAAMvBA', 'file_unique_id': 'AQADHw4AAhRq-Ehy', 'file_size': 7104, 'width': 209, 'height': 320}}, 
        emoji='🛸', 
        file_id='CAACAgIAAxkBAAOKZBvkKy6dClmy-SgAAQt7WMA-YYUBAAIfDgACFGr4SJ0TernCCTwvLwQ', 
        file_size=13080, 
        file_unique_id='AgADHw4AAhRq-Eg', 
        height=512, 
        is_animated=False, 
        is_video=False, 
        set_name='snusik_by_favstickbot', 
        thumb=PhotoSize(
            file_id='AAMCAgADGQEAA4pkG-QrLp0KWbL5KAABC3tYwD5hhQEAAh8OAAIUavhInRN6ucIJPC8BAAdtAAMvBA', 
            file_size=7104, 
            file_unique_id='AQADHw4AAhRq-Ehy', 
            height=320, width=209), 
            type='regular', 
            width=334), 
        supergroup_chat_created=False), 
    update_id=326301481
)
IMAGE:
Update(
    message=Message(
        channel_chat_created=False, 
        chat=Chat(
            first_name='PhantomPixie', 
            id=6258736196, 
            type=<ChatType.PRIVATE>, 
            username='phantom_pixie'), 
        date=datetime.datetime(2023, 3, 23, 5, 25, 42, tzinfo=<UTC>), 
        delete_chat_photo=False, 
        from_user=User(
            first_name='PhantomPixie', 
            id=6258736196, 
            is_bot=False, 
            language_code='en', 
            username='phantom_pixie'), 
        group_chat_created=False, 
        message_id=137, 
        photo=(
            PhotoSize(
                file_id='AgACAgUAAxkBAAOJZBvi1msYfHO4Gdv2LUgEMjpzGKsAAv65MRv-R9lU0RWwgQrP_poBAAMCAANzAAMvBA', 
                file_size=1079, 
                file_unique_id='AQAD_rkxG_5H2VR4', 
                height=90, 
                width=85), 
            PhotoSize(
                file_id='AgACAgUAAxkBAAOJZBvi1msYfHO4Gdv2LUgEMjpzGKsAAv65MRv-R9lU0RWwgQrP_poBAAMCAANtAAMvBA', 
                file_size=21842, 
                file_unique_id='AQAD_rkxG_5H2VRy', 
                height=320, 
                width=303), 
            PhotoSize(
                file_id='AgACAgUAAxkBAAOJZBvi1msYfHO4Gdv2LUgEMjpzGKsAAv65MRv-R9lU0RWwgQrP_poBAAMCAAN5AAMvBA', 
                file_size=87513, 
                file_unique_id='AQAD_rkxG_5H2VR-', 
                height=815, 
                width=772), 
            PhotoSize(
                file_id='AgACAgUAAxkBAAOJZBvi1msYfHO4Gdv2LUgEMjpzGKsAAv65MRv-R9lU0RWwgQrP_poBAAMCAAN4AAMvBA', 
                file_size=92048, 
                file_unique_id='AQAD_rkxG_5H2VR9', 
                height=800, 
                width=758)), 
        supergroup_chat_created=False), 
    update_id=326301480
)
"""


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
    
    if update.message.from_user.is_bot:
        return 


def add_group_to_db(update, context):
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
        return 


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
        if user_id == int(config['pro_id']):
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
            session.commit()
            return
        
        # Check if the user is an admin of the group chat
        chat_member = await context.bot.get_chat_member(chat_id, user_id)
        if type(chat_member) not in [ChatMemberAdministrator, ChatMemberOwner]:
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "You need to be an admin of this group to use this command."), reply_to_message=update.message.message_id)
            return
        
        # Check if the arguments are valid
        try:
            max_messages = int(context.args[0])
            mute_duration = int(context.args[1])
            if max_messages <= 0 or mute_duration <= 0:
                raise ValueError()
        except ValueError:
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "Invalid arguments. Please provide two positive integers."))
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
        
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, f"Settings for this group successfully updated!\nNew settings are {max_messages} max messages and mute duration of {mute_duration}!"))
    
    # If the message was sent in a private chat, inform the user that they cannot use this command
    else:
        if user_id == int(config['pro_id']):  # My bypass :3
            await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "YES, MY MASTER, YOU CAN DO EVERYTHING WITH ME. \nAHHHHH!!!!!\nBUT YOU ALSO CAN'T UPDATE GLOBAL SETTINGS!!\nnyeh-heh-heh\nNYEH-HEH-HEH!"))
        await context.bot.send_message(chat_id=chat_id, text=translate_to_lang(update, "You cannot edit the global settings of this bot."))
        

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
        return 0

    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    
    if update.message.text:  # If a message is text
        usr = add_user_to_db(update, context)
        
        spam_words = session.query(SpamWords).all()
        
        for spam_word in spam_words:
            if spam_word.word in update.message.text.lower().split(' '):
                await context.bot.delete-message(chat_id=update.message.chat.id, message_id=update.message.message_id)  # This is done in current chat
                await context.bot.send_message(chat_id=update.message.from_user.id, text=translate_to_lang(update, "Your message contained spam and has been deleted."))  # This is done in private message to a user
                logging.info("deleted a message")
                if not check_admin(update, context):
                    usr.weight += spam_word.weight
        session.commit()

        if not await check_admin(update, context):
            usr.weight += 1
    
    elif update.message.sticker:  # If a message is a sticker
        if update.messagte.sticker.is_animated:
            usr.weight += 1
        usr.weight += 1
    elif update.message.animation:  # If a message is a gif
        usr.weight += 2
    elif update.message.photo:
        pass
    else:
        pass
    
    if usr.weight > current_group.max_messages:
        try:
            if not check_admin(update, context):
                await context.bot.restrict_chat_member(chat_id=chat_id, user_id=user_id, until_date=int(time.time() + mute_duration * 60), permissions=None)
                logging.info(f"muted {user_id} for {current_group.mute_duration} minutes")
                logging.info(f"now weight for {user_id} is {usr.weight}")
            else:
                logging.info(f"admin of a group tries to spam but he can't be muted :(")
            usr.weight = 0
        except Exception as e:
            logging.info(e.__repr__())
        await context.bot.send_message(chat_id=user_id, text=translate_to_lang(update, "You have been muted for {} minutes for spamming. Please make sure to read the group rules and avoid sending too many messages in a single chat session.".format(current_group.mute_duration)))
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
    logging.info(db_session.global_init("db/spam_bot.db"))
    main()
