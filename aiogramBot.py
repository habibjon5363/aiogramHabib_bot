import logging
import asyncio
import datetime
# from datetime import datatime

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.types import FSInputFile
from random import randint
from aiogram.types import ChatPermissions

TELEGRAM_TOKEN ="6387811620:AAHs1af4nDG65dJ6rNnCpk6-fFacQJia5mA"
GROUP_ID = '-1001674247269'

# вывод отладочных сообщений в терминал
logging.basicConfig(level=logging.INFO)

# создали обьект bot
bot = Bot(token=TELEGRAM_TOKEN)

# создаем обьект диспетчер 
dp = Dispatcher()

# обрабатываем команду старт
@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    image_from_pc = FSInputFile('hello.webp')
    await message.answer_photo(image_from_pc, caption='Пообщаемся?)')
    await asyncio.sleep(2)
    await message.answer("Рад тебя видеть <b> {0.first_name} </b>! ".format(message.from_user), parse_mode='html')


    # обработчик команды рандом 
#  /rnd 1-30
@dp.message(Command(commands=['random', 'rand', 'rnd']))
async def get_random(message: types.Message, command: CommandObject):
    # разбиваем аргументы команды символом "-"
    a, b = [int(n) for n in command.args.split('-')]
    # в личку
    # rnum = randint(1, 6)
    # в группу
    # await message.reply(f'Случайно число цполучилась: \t{rnum}')

    rnum = randint(a, b)
    await message.reply(f'Случайное число получилось: \t {rnum}')
    
    
@dp.message(Command('image'))
async def upload_photo(message: types.Message):
    image_from_pc = FSInputFile('hello.webp')
    await message.answer_photo(image_from_pc, caption='Пообщаемся?)')

@dp.message(Command('mygroup'))
async def cmd_to_group(message: types.Message, bot: Bot):
    await bot.send_message(message.chat.id, 'hello from Habib')

# команда забанить пользователя
@dp.message(Command('ban'))
async def cmd_ban(message: types.Message):
    user_status = await bot.get_chat_member(chat_id= message.chat.id, user_id=message.from_user.id)
    # если в обьекте user_status есть флаг ChatMemberOwner или ChatMemberAdministrator
    if isinstance(user_status, types.chat_member_owner.ChatMemberOwner) or isinstance(user_status, types.chat_member_administrator.ChatMemberAdministrator):
        print('\n\n admin -good\n\n')
    else:
        await message.reply(f' <b>{message.from_user.username} </b>  это не для тебя команда', parse_mode='html')          
        return

    #если команды без цитаты 
    if not message.reply_to_message:
        await message.reply("Пиши команду бан в ответ на собщение")
        return
    bans = message.reply_to_message.from_user.first_name
    await message.bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    await message.bot.ban_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
    await message.reply_to_message.reply (f'Пользователь <b>{bans} </b> забанен', parse_mode='html')   

@dp.message(Command(commands=['mute', 'mt']))
async def echo(message: types.Message, command: CommandObject, bot: Bot):
    adminNAME = message.from_user.first_name
    usrID = message.reply_to_message.from_user.id
    usrNAME = message.reply_to_message.from_user.first_name
    # kakdolga = 3
    long, kakdolga = [n for n in command.args.split('-')]
    kakdolga = int(kakdolga)
    vremiaMuta = datetime.datetime.now() + datetime.timedelta(hours = kakdolga)
    await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=usrID, permissions=ChatPermissions(can_send_messages=+False), until_date=vremiaMuta)
    await message.reply(f'{adminNAME} замутил {usrNAME} на {kakdolga} часов!!!')
    
# ping pong 
@dp.message()
async def echo(message: types.Message):
    print('\nmessage listened\n')
    # await message.answer('бот Хабиб услышал вас: ' + message.text)



# непрерывный режим работы бота в АССИНХРОННОМ режиме 
async def main():
    await dp.start_polling(bot)
    # del all unhandler message удалить все сообщения обработчика
    await bot.delete_webhook(drop_pending_updates=True)

# основной цикл
if __name__ == '__main__':
    asyncio.run(main())