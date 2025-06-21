import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

from aiogram.utils.keyboard import ReplyKeyboardBuilder

import json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


API_TOKEN = '123456789:asdfghj-qwertyuiopasdfghjklzxcvbnm'
WEB_APP_URL = 'https://yoursite.ru/webapp/app'


bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Используйте мини-приложение для заказа.", 
                         reply_markup=ReplyKeyboardBuilder().row(
                            types.KeyboardButton(text='click', web_app=types.WebAppInfo(url=WEB_APP_URL))
                         ).as_markup(resize_keyboard=True))


@dp.message(F.web_app_data)
async def handle_web_app_data(message: types.Message):
    
    # Парсим данные из мини-приложения
    data = json.loads(json.loads(message.web_app_data.data))

    
    # Формируем ответ
    response = \
        "🚖 Новый заказ!\n\n"\
        f"📍 Откуда: {data['startAddress']}\n\n"\
        f"📍 Откуда: {data['startPoint']}\n\n"\
            \
        f"📍 Куда: {data['endAddress']}\n\n"\
        f"📍 Куда: {data['endPoint']}\n\n"\
            \
        f"💳 Тариф ID: {data['tariffId']}\n"\
        f"💳 Город UINTID: {data['uintId']}\n\n"\
            \
        f"💰 Сумма: {data['finalPrice']} руб\n"\
        f"💵 Оплата: {data['paymentMethod']}\n"\
        f'''🎁 Опции: {", ".join(data['options']) or 'нет'}'''
    
    
    await message.answer(response)
    logger.info(f"Received order: {data}")
    

if __name__ == '__main__':
    dp.run_polling(bot)