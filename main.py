#!/usr/bin/python

import asyncio
from config import BOT_TOKEN
from telebot.async_telebot import AsyncTeleBot
from src import handlers # NoQa

bot = AsyncTeleBot(BOT_TOKEN)

if __name__ == '__main__':
    asyncio.run(bot.polling())