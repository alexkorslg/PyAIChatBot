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

bot_chats = {}
ai_messages = [
    {'role': 'system',
     'content': 'You are a helpful assistant.'},
    {'role': 'user',
     'content': 'Hi, I`m USER_NAME. '
                'Сall me by name when replying to me in any language'},
    {'role': 'assistant',
     'content': 'You wrote that your name is USER_NAME. '
                'So I can call you that. Glad to help, USER_NAME!'}
]


def update_chat(user_id, user_name, role, content):
    if user_id not in bot_chats:
        bot_chats[user_id] = []
        for message in ai_messages:
            bot_chats[user_id].append(
                {'role': message['role'],
                 'content': message['content'].replace('USER_NAME', user_name)}
            )

    bot_chats[user_id].append({'role': role, 'content': content})
    return bot_chats[user_id]


@dp.message_handler()
async def chat_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    update_chat(user_id, user_name, 'user', message.text)

    await bot.send_chat_action(message.chat.id, action=types.ChatActions.TYPING)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=bot_chats[user_id]
    )

    await message.answer(response['choices'][0]['message']['content'])

executor.start_polling(dp, skip_updates=True)
