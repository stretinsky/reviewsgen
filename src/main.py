import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv
import openai


def get_from_dotenv(key):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)
    return getenv(key)


logging.basicConfig(level=logging.INFO)
bot = Bot(token=get_from_dotenv("TELEGRAM_API_TOKEN"))
dp = Dispatcher(bot)

openai.api_key = get_from_dotenv("OPENAI_API_TOKEN")

@dp.message_handler(commands=['start'])
async def process_start_program(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '👋Привет! Отправь что сгенерить',
                           )


@dp.message_handler()
async def echo(message: types.Message):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text,
        temperature=0.5,
        max_tokens=300,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    await message.answer(response['choices'][0]['text'])


async def on_startup(x):
    print(f"Бот онлайн")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
