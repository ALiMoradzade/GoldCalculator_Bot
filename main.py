from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import currency
import gold_calculator
import timezone

# Install python-telegram-bot

TOKEN: Final = '7541291889:AAGyjX1tu332PwOD3SFFIqytal8YZ9gw8G4'
BOT_USERNAME: Final = '@GoldCalculator_bot'
log_path = 'log.txt'


def write_log_command(user_id: str, command: str):
    with open(log_path, 'a') as file:
        file.write(f'{timezone.tehran_datetime("%Y/%m/%d, %H:%M")} - @{user_id} => \"/{command}\"\n')


def write_log_text(text: str, end: str = '\n'):
    with open(log_path, 'a') as file:
        file.write(text + end)


def clear_log_file():
    open(log_path, 'w').close()


def successful_message():
    text = '✅با موفقیت انجام شد!'
    return text


def access_denied_message():
    text = 'ببخشیندااا!, شما اونی نیستی که منو ساخته😳\nشرط می بندم که میخواستی اون باشی🙂'
    return text


# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'start')
    await update.message.reply_text('سلام\nچطوری میتونم کمک ت کنم؟\n\n(از دکمه پایین به نام \"Menu\" استفاده کن)')


async def currency_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'currency')
    await update.message.reply_text('لطفا صبور باشید...\nدر حال جمع آوری اطلاعات' + '🔄...')
    await update.message.reply_text(currency.message())


async def gold_sell_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'gold_sell_price')
    await update.message.reply_text("لطفا همانند پیام زیر,\nپارامتر های مورد نیاز را وارد کنید:👇")
    await update.message.reply_text("وزن طلا\nهر گرم طلا 750")
    await update.message.reply_text("1.234\n12345678")


async def gold_buy_secondhand_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'gold_buy_secondhand_price')
    await update.message.reply_text("لطفا همانند پیام زیر,\nپارامتر های مورد نیاز را وارد کنید:👇")
    await update.message.reply_text("وزن طلا\nهر گرم طلا 750\nقیمت فروش")
    await update.message.reply_text("1.234\n12345678\n123456789")


async def gold_buy_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'gold_buy_price')
    await update.message.reply_text("لطفا همانند پیام زیر,\nپارامتر های مورد نیاز را وارد کنید:👇")
    await update.message.reply_text("وزن طلا\nهر گرم طلا 750\nدرصد اجرت\nقیمت فروش")
    await update.message.reply_text("1.234\n12345678\n1.23\n123456789")


async def log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_command(update.message.chat.username, 'log')
    if(update.message.chat.username == "ALiCSharps"):
        await update.message.reply_text('در حال ارسال⬆️...')
        await update.message.reply_document(log_path, caption='انشاءالله که خیره📿\nتقدیم با عشق به خودم🧡\nیادت باشه, اگه خسته میشدی😩 به اینجا نمی رسیدی!😉')
    else:
        await update.message.reply_text(access_denied_message())


async def clear_log(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if(update.message.chat.username == "ALiCSharps"):
        await update.message.reply_text('🫡الساعه...')
        clear_log_file()
        write_log_command(update.message.chat.username, 'clear_log')
        await update.message.reply_text(successful_message())
    else:
        await update.message.reply_text(access_denied_message())


# Responses
def handle_response(text: str) -> str:
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Hey there!'
    return 'نزن این حرف رو!\nدارم یادداشت میکنم😕!'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    #write_log_text(f'{date.getDate("%Y/%m/%d, %H:%M")} - ({message_type}) @{update.message.chat.username} => \"{text.replace('\n', '\\n')}\" \n')
    write_log_text(timezone.tehran_datetime("%Y/%m/%d, %H:%M") + ' - (' + message_type + ') @' + update.message.chat.username + ' => \"' + text.replace('\n', '\\n') + '\" \n')

    newlineCount = text.count('\n')
    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return
    elif newlineCount == 1:
        s = text.replace(',', '').split()
        tmp = [float(x.strip()) for x in s if x is not None]
        await update.message.reply_text(gold_calculator.sell(tmp[0], tmp[1]))
        return
    elif newlineCount == 2:
        s = text.replace(',', '').split()
        tmp = [float(x.strip()) for x in s if x is not None]
        await update.message.reply_text(gold_calculator.buy_secondhand(tmp[0], tmp[1], tmp[2]))
        return
    elif newlineCount == 3:
        s = text.replace(',', '').split()
        tmp = [float(x.strip()) for x in s if x is not None]
        await update.message.reply_text(gold_calculator.buy(tmp[0], tmp[1], tmp[2], tmp[3]))
        return
    else:
        response: str = handle_response(text)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    write_log_text(f'{timezone.tehran_datetime("%Y/%m/%d, %H:%M")} - Update => {update}, caused error => {context.error}')


# Robot
if __name__ == '__main__':
    write_log_text(f'\n{timezone.tehran_datetime("%Y/%m/%d, %H:%M")} - Starting bot...', '')
    print('Starting...')

    app = Application.builder().token(TOKEN).build()

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
    write_log_text(' bot is polling...')
    print('Polling...')
    app.run_polling(poll_interval=3)
