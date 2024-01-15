import os
import random
import html

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

from Grabber import (application, PHOTO_URL, OWNER_ID,
                    user_collection, top_global_groups_collection, top_global_groups_collection, 
                    group_user_totals_collection)

from Grabber import sudo_users as SUDO_USERS 

    
async def global_leaderboard(update: Update, context: CallbackContext) -> None:
   
    cursor = top_global_groups_collection.aggregate([
        {"$project": {"group_name": 1, "count": 1}},
        {"$sort": {"count": -1}},
        {"$limit": 20}
    ])
    leaderboard_data = await cursor.to_list(length=20)

    leaderboard_message = "<b>TOP 20 GROUPS WHO GUESSED MOST CHARACTERS</b>\n\n"

    for i, group in enumerate(leaderboard_data, start=1):
        group_name = html.escape(group.get('group_name', 'Unknown'))

        if len(group_name) > 20:
            group_name = group_name[:25] + '...'
        count = group['count']
        leaderboard_message += f'{i}. <b>{group_name}</b> ➾ <b>{count}</b>\n'
    
    
    photo_url = "https://telegra.ph/file/1d9c963d5a138dc3c3077.jpg"  # Your photo URL

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

async def ctop(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    cursor = group_user_totals_collection.aggregate([
        {"$match": {"group_id": chat_id}},
        {"$project": {"username": 1, "first_name": 1, "character_count": "$count"}},
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>TOP 10 USERS WHO GUESSED CHARACTERS MOST TIME IN THIS GROUP..</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➾ <b>{character_count}</b>\n'
    
    photo_url = "https://telegra.ph/file/1d9c963d5a138dc3c3077.jpg"  # Your photo URL

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

async def ctop(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id

    cursor = group_user_totals_collection.aggregate([
        {"$match": {"group_id": chat_id}},
        {"$project": {"username": 1, "first_name": 1, "character_count": "$count"}},
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>TOP 10 USERS WHO GUESSED CHARACTERS MOST TIME IN THIS GROUP..</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➾ <b>{character_count}</b>\n'
    
    photo_url = "https://telegra.ph/file/1d9c963d5a138dc3c3077.jpg"  # Your photo URL

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')

async def leaderboard(update: Update, context: CallbackContext) -> None:
    
    cursor = user_collection.aggregate([
        {"$project": {"username": 1, "first_name": 1, "character_count": {"$size": "$characters"}}},
        {"$sort": {"character_count": -1}},
        {"$limit": 10}
    ])
    leaderboard_data = await cursor.to_list(length=10)

    leaderboard_message = "<b>TOP 10 USERS WITH MOST CHARACTERS</b>\n\n"

    for i, user in enumerate(leaderboard_data, start=1):
        username = user.get('username', 'Unknown')
        first_name = html.escape(user.get('first_name', 'Unknown'))

        if len(first_name) > 10:
            first_name = first_name[:15] + '...'
        character_count = user['character_count']
        leaderboard_message += f'{i}. <a href="https://t.me/{username}"><b>{first_name}</b></a> ➾ <b>{character_count}</b>\n'
    
    photo_url = "https://telegra.ph/file/1d9c963d5a138dc3c3077.jpg"  # Your photo URL

    await update.message.reply_photo(photo=photo_url, caption=leaderboard_message, parse_mode='HTML')


async def broadcast(update: Update, context: CallbackContext) -> None:
    OWNER_ID = '6392704171'  # Set the OWNER_ID directly within the function

    if str(update.effective_user.id) == OWNER_ID:
        if update.message.reply_to_message is None:
            await update.message.reply_text('Please reply to a message to broadcast.')
            return

        all_users = await user_collection.find({}).to_list(length=None)
        all_groups = await group_user_totals_collection.find({}).to_list(length=None)

        unique_user_ids = set(user['id'] for user in all_users)
        unique_group_ids = set(group['group_id'] for group in all_groups)

        total_sent = 0
        total_failed = 0

        for user_id in unique_user_ids:
            try:
                await context.bot.forward_message(chat_id=user_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        for group_id in unique_group_ids:
            try:
                await context.bot.forward_message(chat_id=group_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Broadcast report:\n\nTotal messages sent successfully: {total_sent}\nTotal messages failed to send: {total_failed}'
        )
    else:
        await update.message.reply_text('Only Murat Can use')


async def broadcast2(update: Update, context: CallbackContext) -> None:
    OWNER_ID = '6392704171'  # Set the OWNER_ID directly within the function

    if str(update.effective_user.id) == OWNER_ID:
        if update.message.reply_to_message is None:
            await update.message.reply_text('Please reply to a message to broadcast.')
            return

        all_groups = await group_user_totals_collection.find({}).to_list(length=None)
        unique_group_ids = set(group['group_id'] for group in all_groups)

        total_sent = 0
        total_failed = 0

        for group_id in unique_group_ids:
            try:
                await context.bot.forward_message(chat_id=group_id, from_chat_id=update.effective_chat.id, message_id=update.message.reply_to_message.message_id)
                total_sent += 1
            except Exception:
                total_failed += 1

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Broadcast report:\n\nTotal messages sent successfully: {total_sent}\nTotal messages failed to send: {total_failed}'
        )
    else:
        await update.message.reply_text('Only the owner can use this command for group broadcast.')

async def stats(update: Update, context: CallbackContext) -> None:
    OWNER_ID = ['6392704171']  # Replace '123456789' with the actual owner ID

    if str(update.effective_user.id) not in OWNER_ID:
        await update.message.reply_text('Only for sudo users...')
        return

    user_count = await user_collection.count_documents({})

    group_count = len(await group_user_totals_collection.distinct('group_id'))

    await update.message.reply_text(f'Total Users: {user_count}\nTotal Groups: {group_count}')




async def send_users_document(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('only For Sudo users...')
        return
    cursor = user_collection.find({})
    users = []
    async for document in cursor:
        users.append(document)
    user_list = ""
    for user in users:
        user_list += f"{user['first_name']}\n"
    with open('users.txt', 'w') as f:
        f.write(user_list)
    with open('users.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('users.txt')

async def send_groups_document(update: Update, context: CallbackContext) -> None:
    if str(update.effective_user.id) not in SUDO_USERS:
        update.message.reply_text('Only For Sudo users...')
        return
    cursor = top_global_groups_collection.find({})
    groups = []
    async for document in cursor:
        groups.append(document)
    group_list = ""
    for group in groups:
        group_list += f"{group['group_name']}\n"
        group_list += "\n"
    with open('groups.txt', 'w') as f:
        f.write(group_list)
    with open('groups.txt', 'rb') as f:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=f)
    os.remove('groups.txt')

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

async def brotu(update: Update, context: CallbackContext) -> None:
    photo_url = 'https://telegra.ph/file/039b4488f7a8ff9c20bf2.jpg'  # Replace with your photo URL

    keyboard = [
        [
            InlineKeyboardButton("Add to Group", url='http://t.me/Dark_waifu_Bot?startgroup=new')
        ],
        [
            InlineKeyboardButton("Support Group", url='https://t.me/dark_world_231'),
            # Add more buttons here if needed
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the photo with the inline keyboard and a message
    await update.message.reply_photo(photo=photo_url, caption="𝖧𝖾𝗒 sukuna 𝗎𝗌𝖾𝗋𝗌, 𝗂𝖿 𝗒𝗈𝗎 𝗐𝖺𝗇𝗍 𝗍𝗈 𝖺𝖽𝖽 𝗒𝗈𝗎𝗋 𝖿𝖺𝗏𝗈𝗋𝗂𝗍𝖾 𝖼𝗁𝖺𝗋𝖺𝖼𝗍𝖾𝗋. 𝖸𝗈𝗎 𝖼𝖺𝗇 𝖺𝖽𝖽 𝖺𝗇𝗒 𝖼𝗁𝖺𝗋𝖺𝖼𝗍𝖾𝗋 𝗂𝗇 𝗍𝗁𝗂𝗌 𝗅𝗂𝗄𝖾 𝖠𝗇𝗂𝗆𝖾 , 𝖼𝖺𝗋𝗍𝗈𝗈𝗇 𝖺𝗇𝖽 𝖬𝖺𝗋𝗏𝖾𝗅 𝖾𝗍𝖼. 𝗒𝗈𝗎 𝖼𝖺𝗇 𝖽𝗆 𝗆𝖾 :- @sukuna201", reply_markup=reply_markup)

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext

def report(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    admins = context.bot.get_chat_administrators(chat_id)
    
    # Extract usernames of admins
    admin_usernames = [f"@{admin.user.username}" for admin in admins if admin.user.username]

    # Create a string mentioning all admins
    admins_mention = ", ".join(admin_usernames)

    # Formulate the message mentioning all admins
    report_message = f"Reporting to all group admins! Admins: {admins_mention}"

    # Send the report message to all admins
    context.bot.send_message(chat_id=chat_id, text=report_message)

def add_report_command(dispatcher):
    dispatcher.add_handler(CommandHandler("report", report))

# Add this handler in your main script:
# updater = Updater("YOUR_TOKEN", use_context=True)
# add_report_command(updater.dispatcher)


application.add_handler(CommandHandler('brotu', brotu, block=False))
application.add_handler(CommandHandler('ctop', ctop, block=False))
application.add_handler(CommandHandler('stats', stats, block=False))
application.add_handler(CommandHandler('TopGroups', global_leaderboard, block=False))
application.add_handler(CommandHandler('broadcast2', broadcast2, block=False))

application.add_handler(CommandHandler('list', send_users_document, block=False))
application.add_handler(CommandHandler('groups', send_groups_document, block=False))


application.add_handler(CommandHandler('top', leaderboard, block=False))
application.add_handler(CommandHandler('broadcast', broadcast, block=False))
