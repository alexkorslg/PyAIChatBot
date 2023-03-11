import openai
import telebot
from dotenv import dotenv_values

SETTINGS = dotenv_values('.env')
openai.api_key = SETTINGS['OPENAI_PASSWORD']
bot = telebot.TeleBot(SETTINGS['TELEGRAM_BOT_TOKEN'])


@bot.message_handler(func=lambda _: True)
def handle_message(message):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=message.text,
        temperature=0.8,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    bot.send_message(
        chat_id=message.from_user.id,
        text=response['choices'][0]['text']
    )


bot.polling()
