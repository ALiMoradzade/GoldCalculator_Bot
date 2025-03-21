from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random
from typing import Final
import os
from dotenv import load_dotenv
import currency
import gold_calculator
import json_logger

# bot initial
load_dotenv()
TELEGRAM_BOT_TOKEN: Final = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_BOT_USERNAME: Final = os.getenv("TELEGRAM_BOT_USERNAME")
ADMIN_USERNAME: Final = os.getenv("ADMIN_USERNAME")
LOG_PATH: Final = "log.json"
json_logger.file_path = LOG_PATH
POLL_INTERVAL_SECONDS: Final = 5

responses = [
    "نزن این حرف رو!🫢\nدارم یادداشت میکنم!😕",
    "این چیزی که گفتی یعنی چی؟🤔",
    "چرا میخوای بیرون از دستوراتم چیزی بگی؟!😫",
    "واقعا؟!🫤",
    "آقا, آقا😧...\nکنترل کن خودتو!🫣",
    "متاسفانه من چیزی برای گفتن ندارم!🤐",
    "چشم, اطلاع میدم🫡",
    "بیرون از دستورات چیزی نفرست🤫",
    "چی میخوای بگی؟🧐",
    "این حرف ت جزء دستورات بود؟!🤨"
]

def get_userinfo(user_info) -> str:
    user = 'Unknown'
    if user_info.username != '' or user_info.username is not None:
        user = '@' + user_info.username
    elif user_info.full_name != '' or user_info.full_name is not None:
        user = user_info.full_name
    return user

def successful_message():
    text = '✅با موفقیت انجام شد!'
    return text

def access_denied_message():
    text = 'ببخشیندااا!, شما اونی نیستی که منو ساخته😳\nشرط می بندم که میخواستی اون باشی🙂'
    return text

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_logger.write_command(get_userinfo(update.message.chat), 'start')
    await update.message.reply_text('سلام\nچطوری میتونم کمک ت کنم؟\n\n(از دکمه پایین به نام \"Menu\" استفاده کن)')

async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_logger.write_command(get_userinfo(update.message.chat), 'currency')
    await update.message.reply_text('لطفا صبور باشید...\nدر حال جمع آوری اطلاعات' + '🔄...')
    await update.message.reply_text(currency.message())

async def gold_sell_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_logger.write_command(get_userinfo(update.message.chat), 'gold_sell_price')
    await update.message.reply_text("لطفا همانند پیام زیر,\nپارامتر های مورد نیاز را وارد کنید:👇")
    await update.message.reply_text("وزن طلا\nمظنه طلا 750")
    await update.message.reply_text("1.234\n12345678")

async def gold_buy_secondhand_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_logger.write_command(get_userinfo(update.message.chat), 'gold_buy_secondhand_price')
    await update.message.reply_text("لطفا همانند پیام زیر,\nپارامتر های مورد نیاز را وارد کنید:👇")
    await update.message.reply_text("وزن طلا\nمظنه طلا 18\nقیمت حجره دار")
    await update.message.reply_text("1.234\n12345678\n123456789")

async def gold_buy_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_logger.write_command(get_userinfo(update.message.chat), 'gold_buy_price')
    await update.message.reply_text("لطفا همانند پیام زیر,\nپارامتر های مورد نیاز را وارد کنید:👇")
    await update.message.reply_text("وزن طلا\nمظنه طلا 18\nدرصد اجرت\nقیمت حجره دار")
    await update.message.reply_text("1.234\n12345678\n1.23\n123456789")

async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    json_logger.write_command(get_userinfo(update.message.chat), 'log')
    if update.message.chat.username == ADMIN_USERNAME:
        await update.message.reply_text('در حال ارسال⬆️...')
        await update.message.reply_document(LOG_PATH, caption='انشاءالله که خیره📿\nتقدیم با عشق به خودم🧡\nیادت باشه, اگه خسته میشدی😩 به اینجا نمی رسیدی!😉')
    else:
        await update.message.reply_text(access_denied_message())

async def clear_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.username == ADMIN_USERNAME:
        await update.message.reply_text('🫡الساعه...')
        json_logger.clear()
        json_logger.write_command(get_userinfo(update.message.chat), 'clear_log')
        await update.message.reply_text(successful_message())
    else:
        await update.message.reply_text(access_denied_message())

# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    elif 'سلام' in processed:
        return 'سلام عشقی🫀!'

    return random.choice(responses)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    newline_count = text.count('\n') + 1
    if message_type == 'group':
        if TELEGRAM_BOT_USERNAME in text:
            new_text: str = text.replace(TELEGRAM_BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    elif newline_count == 2:
        s = text.replace(',', '').split()
        tmp = [float(x.strip()) for x in s if x is not None]
        response = gold_calculator.sell(tmp[0], tmp[1])
        return
    elif newline_count == 3:
        s = text.replace(',', '').split()
        tmp = [float(x.strip()) for x in s if x is not None]
        response = gold_calculator.buy_secondhand(tmp[0], tmp[1], tmp[2])
    elif newline_count == 4:
        s = text.replace(',', '').split()
        tmp = [float(x.strip()) for x in s if x is not None]
        response = gold_calculator.buy(tmp[0], tmp[1], tmp[2], tmp[3])
    else:
        response: str = handle_response(text)

    dic = {
        "user text": text.replace("\n", "\\n"),
        "robot response": response
    }
    json_logger.write_text(get_userinfo(update.message.chat), dic)

    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dic = {
        "user text": update.message.text,
        "error message": context.error.__str__()
    }
    json_logger.write_text(get_userinfo(update.message.chat), dic)

# Robot
if __name__ == '__main__':
    dic = {
        "text": "Starting bot..."
    }
    json_logger.write_text("Robot", dic)
    print('Starting...')

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('currency', currency_command))
    app.add_handler(CommandHandler('gold_sell_price', gold_sell_price))
    app.add_handler(CommandHandler('gold_buy_secondhand_price', gold_buy_secondhand_price))
    app.add_handler(CommandHandler('gold_buy_price', gold_buy_price))
    app.add_handler(CommandHandler('log', log))
    app.add_handler(CommandHandler('clear_log', clear_log))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    # Polls the bot
    dic = {
        "text": "Bot is polling..."
    }
    json_logger.write_text("Robot", dic)
    print('Polling...')
    app.run_polling(poll_interval=POLL_INTERVAL_SECONDS)
    
