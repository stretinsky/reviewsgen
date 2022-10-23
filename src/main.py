import logging
from aiogram import Bot, Dispatcher, executor, types
from os import getenv
from dotenv import load_dotenv
import requests


def get_from_dotenv(key):
    dotenv_path = '.env'
    load_dotenv(dotenv_path)
    return getenv(key)


logging.basicConfig(level=logging.INFO)
bot = Bot(token=get_from_dotenv("TELEGRAM_API_TOKEN"))
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_program(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add()
    button_phone = types.KeyboardButton(text="☎️Отправить телефон",
                                        request_contact=True)
    keyboard.add(button_phone)
    await bot.send_message(message.from_user.id,
                           '👋Привет!Отправьте номер телефона:',
                           reply_markup=keyboard)


@dp.message_handler(content_types=['contact'])
async def contact(message: types.Message):
    if message.contact is not None:
        keyboard2 = types.ReplyKeyboardRemove()
        phonenumber = str(message.contact.phone_number)
        if phonenumber[0] != "+":
            phonenumber = f"+{phonenumber}"
        user_id = str(message.from_user.id)
        username = str(message.from_user.username)
        await bot.send_message(
            message.from_user.id,
            f'Вы успешно отправили свой номер телефона🙂',
            reply_markup=keyboard2
        )
        url = "http://45.86.183.186/api/register"
        data = {
            "number": phonenumber,
            "telegramUserId": user_id,
            "username": username

        }
        response = requests.post(url=url, data=data).json()
        status = response['alreadyRegistered']
        if status:
            await bot.send_message(message.from_user.id, "Вы уже зарегистрированы🙂")
        else:
            login = response['login']
            password = response['password']
            await bot.send_message(
                message.from_user.id,
                f'Ваш логин: {login}\n'
                f'Ваш пароль: {password}'
            )
    else:
        await bot.send_message(
            message.from_user.id,
            "Произошла какая-то ошибка, отправьте номер еще раз🤔"
        )
        await process_start_program(message=message)


async def on_startup(x):
    print(f"Бот онлайн")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
