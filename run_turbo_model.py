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

ai_messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': 'Do you know everething?'},
    {'role': 'assistant',
        'content': 'As an AI language model, I have knowledge on a wide range of topics'}
]


def update(messages, role, content):
    messages.append({'role': role, 'content': content})
    return messages


@dp.message_handler()
async def send(message: types.Message):
    update(ai_messages, 'user', message.text)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=ai_messages
    )

    await message.answer(response['choices'][0]['message']['content'])

executor.start_polling(dp, skip_updates=True)
