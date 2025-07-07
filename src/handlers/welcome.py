from main import bot

# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    text = 'Привет, я Рубик.\nМожешь мне что нибуть написать, я повторю!'
    await bot.reply_to(message, text)