import logging
import asyncio
# from datetime import datatime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.types import FSInputFile

TELEGRAM_TOKEN ="6387811620:AAHs1af4nDG65dJ6rNnCpk6-fFacQJia5mA"

# вывод отладочных сообщений в терминал
logging.basicConfig(level=logging.INFO)

# создали обьект bot
bot = Bot(token=TELEGRAM_TOKEN)

# создаем обьект диспетчер 
dp = Dispatcher()

# обрабатываем команду старт
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Рад тебя видеть!")







# непрерывный режим работы бота в АССИНХРОННОМ режиме 
async def main():
    await dp.start_polling(bot)

# основной цикл
if __name__ == '__main__':
    asyncio.run(main())