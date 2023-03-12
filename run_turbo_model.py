import os
import openai
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv('OPENAI_PASSWORD')
bot = Bot(os.getenv('TELEGRAM_BOT_TOKEN'))
dp = Dispatcher(bot)

BOT_ROLE = 'You are a helpful assistant.'
bot_chats = {}


def update(bot_chat, role, content):
    bot_chat.append({'role': role, 'content': content})
    return bot_chat


@dp.message_handler()
async def chat_handler(message: types.Message):
    await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)

    user_id = message.from_user.id
    user_name = message.from_user.full_name

    if user_id not in bot_chats:
        bot_chats[user_id] = [{'role': 'system', 'content': BOT_ROLE}]
        update(bot_chats[user_id], 'user', f'Hi, my name is {user_name}')
    update(bot_chats[user_id], 'user', message.text)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=bot_chats[user_id]
    )

    await message.answer(response['choices'][0]['message']['content'])

executor.start_polling(dp, skip_updates=True)
