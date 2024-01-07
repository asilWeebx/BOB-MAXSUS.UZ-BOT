import logging

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile
# Logging sozlamalari
logging.basicConfig(level=logging.INFO)

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

user_file = 'users.txt'
user_contact = 'users_contact.txt'
user_id_txt = 'id.txt'

admin_id = 6620097375
TOKEN = '6873674634:AAETBNP5VlOTb1xwOVSzJE-YdoC5nRXVC9o'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class XABAR(StatesGroup):
    waiting_for_hello = State()
class SEND(StatesGroup):
    waiting_send = State()

class SEND_ID(StatesGroup):
    waiting_send_id = State()

class SEND_ID_txt(StatesGroup):
    waiting_send_id_txt = State()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if message.from_user.id == admin_id:
        photo = open('images/ava1.jpg', 'rb')
        caption = f'Salom {message.from_user.full_name}-admin!\nBOBMAXSUS.UZ ning rasmiy botiga xush kelibsiz.'
        user_id = message.from_user.id
        # Foydalanuvchi ID-sini users.txt fayliga yozamiz
        with open(user_file, 'r') as file:
            user_ids = [int(line.strip()) for line in file]

        if user_id not in user_ids:
            with open(user_file, 'a') as file:
                file.write(str(user_id) + '\n')
        keyboard = InlineKeyboardMarkup(row_width=2)
        button_biz = InlineKeyboardButton('Biz Haqimizdaℹ️', callback_data='biz')
        button_boglanish = InlineKeyboardButton('Bog\'lanish☎️', callback_data='boglanish')
        button_xodimlar = InlineKeyboardButton('Xodimlar🛠', callback_data='xodimlar')
        button_admin = InlineKeyboardButton('Admin Panel🎛', callback_data='adminka')
        keyboard.add(button_boglanish, button_xodimlar, button_biz,button_admin)
        message_text = f"*{caption}*"
        await bot.send_photo(message.chat.id, photo=photo, caption=message_text, reply_markup=keyboard,
                             parse_mode=types.ParseMode.MARKDOWN)
    else:
            photo = open('images/ava1.jpg', 'rb')
            caption = 'Salom!\nBOBMAXSUS.UZ ning rasmiy botiga xush kelibsiz.'
            user_id = message.from_user.id
            # Foydalanuvchi ID-sini users.txt fayliga yozamiz
            with open(user_file, 'r') as file:
                user_ids = [int(line.strip()) for line in file]

            if user_id not in user_ids:
                with open(user_file, 'a') as file:
                    file.write(str(user_id) + '\n')
            keyboard = InlineKeyboardMarkup(row_width=2)
            button_biz = InlineKeyboardButton('Biz Haqimizdaℹ️', callback_data='biz')
            button_boglanish = InlineKeyboardButton('Bog\'lanish☎️', callback_data='boglanish')
            button_xodimlar = InlineKeyboardButton('Xodimlar🛠', callback_data='xodimlar')
            keyboard.add(button_boglanish, button_xodimlar, button_biz)
            message_text = f"*{caption}*"
            await bot.send_photo(message.chat.id, photo=photo, caption=message_text, reply_markup=keyboard,
                                 parse_mode=types.ParseMode.MARKDOWN)



@dp.callback_query_handler(lambda c: c.data == 'biz',)
async def about(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    photo_path = 'images/service.jpg'
    caption = f"BOBMAXSUS.UZ Yo'l qurilish MCHJ\nO'zbekiston bo'ylab sifatli yo'l qurilishi,\nbitum emulsiyasi ishlari, asfalt ishlab chiqarish\nva qo'shimcha xizmatlarni taklif etuvchi \nkatta kompaniya. Ijara xizmati, texnikaviy yaxlitlik va qulay\nbog'lanish uchun biz bilan +998 XX XXX-XX-XX raqamidan yoki\nbotimizning (Bog'lanish☎️) tugmasi bilan tez va oson bog'laning.\nBOBMAXSUS.UZ Yuqori muvaffaqiyatlar!"
    message_text = f"*{caption}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='back')
    keyboard.add(button_orqaga)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_photo(user_id, photo=open(photo_path, 'rb'), caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'adminka',)
async def about(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    photo = open('images/admin.png', 'rb')
    caption = 'Salom!\nBOBMAXSUS.UZ ning admin paneliga xush kelibsiz'
    message_text = f"*{caption}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_statistika = InlineKeyboardButton('Statistika📊', callback_data='statistika')
    button_xabar = InlineKeyboardButton('Xabar Yuborish💬', callback_data='users_xabar')
    button_id = InlineKeyboardButton('ID orqalik xabar yuborish🆔', callback_data='users_id')
    button_back = InlineKeyboardButton('Bosh menyu🔙', callback_data='back_admin')
    keyboard.add(button_xabar, button_statistika, button_id, button_back)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_photo(user_id, photo=photo, caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data == 'users_id', state=None)
async def send_users(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    caption = 'Siz id orqalik xabar yuborish bo\'limidasiz!\nMarhamat menga Foydalanuvchi id sini kiriting...🆔'
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_admin_id')
    keyboard.add(button_orqaga)
    message_text = f"*{caption}*"
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_message(user_id, text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
    await SEND_ID.waiting_send_id.set()

@dp.message_handler(state=SEND_ID.waiting_send_id)
async def process_id(message: types.Message, state: FSMContext):
    text = message.text
    with open(user_id_txt, 'w') as file:
        file.write(str(text) + '\n')
        # Xabarni yuborish
    await bot.send_message(admin_id,f'*{text} Foydalanuvchiga yubormoqchi bo\'gan xabaringizni kiriting...*',
                           parse_mode=types.ParseMode.MARKDOWN)
    await state.finish()
    await SEND_ID_txt.waiting_send_id_txt.set()


@dp.message_handler(state=SEND_ID_txt.waiting_send_id_txt)
async def process_send(message: types.Message, state: FSMContext):
    text = message.text
    with open(user_id_txt, 'r') as file:
        user_ids = [int(line.strip()) for line in file]
        # Xabarni yuborish
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, f'*BOB-MAXSUS.UZ dan yangi xabar:\n{message.text}*',
                                   parse_mode=types.ParseMode.MARKDOWN)
        except Exception as e:
            logging.exception(f"Xabar yuborishda xatolik: {e}")
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_admin_1')
    keyboard.add(button_orqaga)
    await bot.send_message(admin_id, f'{user_ids} foydalanuvchiga ({text}) xabaringiz yetkazildi✅',
                           parse_mode=types.ParseMode.MARKDOWN, reply_markup=keyboard)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'statistika',)
@dp.callback_query_handler(lambda c: c.data == 'statistika',)
async def statistika(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    photo_path = 'images/statistika.jpg'
    with open(user_file, 'r') as file:
        user_ids = [int(line.strip()) for line in file]

    total_users = len(user_ids)
    with open(user_contact, 'r') as file:
        user_ids_c = [str(line.strip()) for line in file]

    total_users_c = len(user_ids_c)
    caption = f'BOBMAXSUS.UZ ning statistikasi\nFoydalanuvchilar soni: {total_users} ta\nBiz bilan bog\'langanlar soni: {total_users_c} ta'
    message_text = f"*{caption}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_file = InlineKeyboardButton('File 📁', callback_data='admin_file')
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_admin_1')
    keyboard.add(button_file,button_orqaga)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_photo(user_id, photo=open(photo_path, 'rb'), caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data == 'admin_file')
async def file(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    photo_path = 'images/base.jpg'
    caption = f'BOBMAXSUS.UZ bilan bog\'langanlar xaqida ma\'lumotlari'
    message_text = f"*{caption}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_admin_1')
    keyboard.add(button_orqaga)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_photo(user_id, photo=open(photo_path, 'rb'), caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
    file_path = 'users_contact.txt'
    file_path_2 = 'users.txt'
    await bot.send_document(user_id, InputFile(file_path))
    await bot.send_document(user_id, InputFile(file_path_2))

@dp.callback_query_handler(lambda c: c.data == 'users_xabar', state=None)
async def send_users(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    photo_path = 'images/message.jpg'
    caption = 'Siz foydalanuvchilarga xabar yuborish bo\'limidasiz!\nMarhamat menga xabaringizni kiriting...✍🏻'
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_admin')
    keyboard.add(button_orqaga)

    message_text = f"*{caption}*"
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_photo(user_id, photo=open(photo_path, 'rb'), caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
    await SEND.waiting_send.set()

@dp.message_handler(state=SEND.waiting_send)
async def process_message(message: types.Message, state: FSMContext):
    text = message.text
    with open(user_file, 'r') as file:
        user_ids = [int(line.strip()) for line in file]
        # Xabarni yuborish
    for user_id in user_ids:
        try:
            await bot.send_message(user_id, f'*BOB-MAXSUS.UZ dan yangi xabar:\n{message.text}*',parse_mode=types.ParseMode.MARKDOWN)
        except Exception as e:
            logging.exception(f"Xabar yuborishda xatolik: {e}")
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_admin_1')
    keyboard.add(button_orqaga)
    await bot.send_message(admin_id,f'_Hamma foydalanuvchilarga_ *{text}* _xabaringiz yetqazildi_',
                           parse_mode=types.ParseMode.MARKDOWN,reply_markup=keyboard)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'boglanish', state=None)
async def send_boglanish(callback_query: types.CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    user_name = callback_query.from_user.username
    photo_path = 'images/boglanish.jpg'
    caption = 'Siz bog\'lanish bo\'limidasiz marhamat savolingizni yoki taklifingizni yozing...'
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga')
    keyboard.add(button_orqaga)

    message_text = f"*{caption}*"
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await bot.send_photo(user_id, photo=open(photo_path, 'rb'), caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
    await XABAR.waiting_for_hello.set()


@dp.message_handler(state=XABAR.waiting_for_hello)
async def process_message(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    user_name = message.from_user.username
    ism = message.from_user.full_name
    text = message.text

    if 'biz bilan bog\'langaningizdan xursandmiz' in text.lower():
        pass
    else:
        with open(user_contact, 'a') as file:
            file.write(str(f'Username: @{user_name} || ID: ({user_id}) || qoldirilgan xabar: {text}') + '\n')
        await bot.send_message(user_id, "*Sizning xabaringiz muvaffaqiyatli qabul qilindi! Javobni kuting⏰!*",
                               parse_mode=types.ParseMode.MARKDOWN)
        await state.finish()
        await bot.send_message(admin_id,
                                   f"\n*🌐 BOB-MAXSUS.UZ bot foydalanuvchisi biz bilan bog'lanmoqchi\n👤Foydalanuvchi: \nTo'liq ismi: {ism}\nUsername: @{user_name} \nID: ({user_id}) \nXabari: {text} \n*",
                                   parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'orqaga',state=XABAR.waiting_for_hello)
async def go_back(callback_query: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    photo = open('images/ava1.jpg', 'rb')
    caption = 'Salom!\nBOBMAXSUS.UZ ning rasmiy botiga xush kelibsiz.'
    keyboard = InlineKeyboardMarkup(row_width=2)
    user_id = callback_query.from_user.id
    button_biz = InlineKeyboardButton('Biz Haqimizdaℹ️', callback_data='biz')
    button_boglanish = InlineKeyboardButton('Bog\'lanish☎️', callback_data='boglanish')
    button_xodimlar = InlineKeyboardButton('Xodimlar🛠', callback_data='xodimlar')
    keyboard.add(button_boglanish, button_xodimlar, button_biz)
    message_text = f"*{caption}*"
    await bot.send_photo(user_id, photo=photo, caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'back')
async def back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    photo = open('images/ava1.jpg', 'rb')
    caption = 'Salom!\nBOBMAXSUS.UZ ning rasmiy botiga xush kelibsiz.'
    keyboard = InlineKeyboardMarkup(row_width=2)
    user_id = callback_query.from_user.id
    button_biz = InlineKeyboardButton('Biz Haqimizdaℹ️', callback_data='biz')
    button_boglanish = InlineKeyboardButton('Bog\'lanish☎️', callback_data='boglanish')
    button_xodimlar = InlineKeyboardButton('Xodimlar🛠', callback_data='xodimlar')
    keyboard.add(button_boglanish, button_xodimlar, button_biz)
    message_text = f"*{caption}*"
    await bot.send_photo(user_id, photo=photo, caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data == 'back_admin')
async def back(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    photo = open('images/ava1.jpg', 'rb')
    caption = 'Salom!\nBOBMAXSUS.UZ ning rasmiy botiga xush kelibsiz.'
    keyboard = InlineKeyboardMarkup(row_width=2)
    user_id = callback_query.from_user.id
    button_biz = InlineKeyboardButton('Biz Haqimizdaℹ️', callback_data='biz')
    button_boglanish = InlineKeyboardButton('Bog\'lanish☎️', callback_data='boglanish')
    button_xodimlar = InlineKeyboardButton('Xodimlar🛠', callback_data='xodimlar')
    button_admin = InlineKeyboardButton('Admin Panel🎛', callback_data='adminka')
    keyboard.add(button_boglanish, button_xodimlar, button_biz, button_admin)
    message_text = f"*{caption}*"
    await bot.send_photo(user_id, photo=photo, caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'orqaga_admin',state=SEND.waiting_send)
async def go_back_admin(callback_query: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    photo = open('images/admin.png', 'rb')
    caption = 'BOBMAXSUS.UZ ning admin paneliga qaytdingiz🔙'
    message_text = f"*{caption}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_statistika = InlineKeyboardButton('Statistika📊', callback_data='statistika')
    button_xabar = InlineKeyboardButton('Xabar Yuborish💬', callback_data='users_xabar')
    button_id = InlineKeyboardButton('ID orqalik xabar yuborish🆔', callback_data='users_id')
    button_back = InlineKeyboardButton('Bosh menyu🔙', callback_data='back_admin')
    keyboard.add(button_xabar, button_statistika, button_id, button_back)
    await bot.send_photo(user_id, photo=photo, caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
    await state.finish()
@dp.callback_query_handler(lambda c: c.data == 'orqaga_admin_id',state=SEND_ID.waiting_send_id)
async def go_back_admin(callback_query: types.CallbackQuery,state: FSMContext):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    photo = open('images/admin.png', 'rb')
    caption = 'BOBMAXSUS.UZ ning admin paneliga qaytdingiz🔙'
    message_text = f"*{caption}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_statistika = InlineKeyboardButton('Statistika📊', callback_data='statistika')
    button_xabar = InlineKeyboardButton('Xabar Yuborish💬', callback_data='users_xabar')
    button_id = InlineKeyboardButton('ID orqalik xabar yuborish🆔', callback_data='users_id')
    button_back = InlineKeyboardButton('Bosh menyu🔙', callback_data='back_admin')
    keyboard.add(button_xabar, button_statistika, button_id, button_back)
    await bot.send_photo(user_id, photo=photo, caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
    await state.finish()
@dp.callback_query_handler(lambda c: c.data == 'orqaga_admin_1')
async def go_back_admin(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    photo = open('images/admin.png', 'rb')
    caption = 'BOBMAXSUS.UZ ning admin paneliga qaytdingiz🔙'
    message_text = f"*{caption}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_statistika = InlineKeyboardButton('Statistika📊', callback_data='statistika')
    button_xabar = InlineKeyboardButton('Xabar Yuborish💬', callback_data='users_xabar')
    button_id = InlineKeyboardButton('ID orqalik xabar yuborish🆔', callback_data='users_id')
    button_back = InlineKeyboardButton('Bosh menyu🔙', callback_data='back_admin')
    keyboard.add(button_xabar, button_statistika, button_id,button_back)
    await bot.send_photo(user_id, photo=photo, caption=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'xodimlar')
async def send_xodimlar(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'Marhamat BOBMAXSUS.UZ ning xodimlari bilan tanishing'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_obidov = InlineKeyboardButton('FARRUX OBIDOV', callback_data='FARRUX_OBIDOV')
    button_qurbonov = InlineKeyboardButton('QURBONOV BAXODIR', callback_data='QURBONOV_BAXODIR')
    button_ruziyev= InlineKeyboardButton('RUZIYEV SANJAR', callback_data='RUZIYEV_SANJAR')
    button_karimov = InlineKeyboardButton('SHAXBOZ KARIMOV', callback_data='SHAXBOZ_KARIMOV')
    button_bozorov = InlineKeyboardButton('DONI BOZOROV', callback_data='DONI_BOZOROV')
    button_sayimov = InlineKeyboardButton('AZIM SAYIMOV', callback_data='AZIM_SAYIMOV')
    button_zohid = InlineKeyboardButton('ABDULLAYEV ZOHID', callback_data='ABDULLAYEV_ZOHID')
    button_qodirov = InlineKeyboardButton('ABBOS QODIROV', callback_data='ABBOS_QODIROV')
    button_mamadiyev = InlineKeyboardButton('JAMSHID MAMADIYEV', callback_data='JAMSHID_MAMADIYEV')
    button_narzullayev = InlineKeyboardButton('FAZLIDDIN NARZULLAYEV', callback_data='FAZLIDDIN_NARZULLAYEV')
    button_back = InlineKeyboardButton('🔙Orqaga', callback_data='back')
    keyboard.add(button_obidov, button_qurbonov,
                 button_ruziyev,button_karimov,
                 button_bozorov,button_sayimov,
                 button_zohid,button_qodirov,
                 button_mamadiyev,button_narzullayev,button_back)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'FARRUX_OBIDOV')
async def farrux(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: FARRUX OBIDOV\nTelefon Raqam: +998887604474\nMoshina raqami: 01 831 OLA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'QURBONOV_BAXODIR')
async def qurbonov(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: QURBONOV BAXODIR\nTelefon Raqam: +998996280876\nMoshina raqami: 01 831 OLA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'RUZIYEV_SANJAR')
async def ruziyev(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: RUZIYEV SANJAR\nTelefon Raqam: +998975852579\nMoshina raqami: 01 826 OLA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data == 'SHAXBOZ_KARIMOV')
async def shaxboz(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nOPERATOR\nIsm sharif: SHAXBOZ KARIMOV\nTelefon Raqam: +998990720967'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data == 'DONI_BOZOROV')
async def doni(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: DONI BOZOROV\nTelefon Raqam: +998912267787\nMoshina raqami: 70 701 QBA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data == 'AZIM_SAYIMOV')
async def azim(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: AZIM SAYIMOV\nTelefon Raqam: +998940268707\nMoshina raqami: 70 701 MBA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'ABDULLAYEV_ZOHID')
async def zohid(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: ABDULLAYEV ZOHID\nTelefon Raqam: +998977066260\nMoshina raqami: 70 444 QBA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'ABBOS_QODIROV')
async def abbos(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: ABBOS QODIROV\nTelefon Raqam: +998992466962\nMoshina raqami: 70 701 NBA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)

@dp.callback_query_handler(lambda c: c.data == 'JAMSHID_MAMADIYEV')
async def jamshid(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: JAMSHID MAMADIYEV\nTelefon Raqam: +998883177871\nMoshina raqami: 01 830 OLA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)


@dp.callback_query_handler(lambda c: c.data == 'FAZLIDDIN_NARZULLAYEV')
async def fazliddin(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'BOB-MAXSUS.UZ\nIsm sharif: FAZLIDDIN NARZULLAYEV\nTelefon Raqam: +998975882230\nMoshina raqami: 01 829 OLA'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_orqaga_xodim = InlineKeyboardButton('🔙Orqaga', callback_data='orqaga_xodim')
    keyboard.add(button_orqaga_xodim)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)





@dp.callback_query_handler(lambda c: c.data == 'orqaga_xodim')
async def send_xodimlar(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    user_id = callback_query.from_user.id
    message = 'Marhamat BOBMAXSUS.UZ ning xodimlari bilan tanishing'
    message_text = f"*{message}*"
    keyboard = InlineKeyboardMarkup(row_width=2)
    button_obidov = InlineKeyboardButton('FARRUX OBIDOV', callback_data='FARRUX_OBIDOV')
    button_qurbonov = InlineKeyboardButton('QURBONOV BAXODIR', callback_data='QURBONOV_BAXODIR')
    button_ruziyev= InlineKeyboardButton('RUZIYEV SANJAR', callback_data='RUZIYEV_SANJAR')
    button_karimov = InlineKeyboardButton('SHAXBOZ KARIMOV', callback_data='SHAXBOZ_KARIMOV')
    button_bozorov = InlineKeyboardButton('DONI BOZOROV', callback_data='DONI_BOZOROV')
    button_sayimov = InlineKeyboardButton('AZIM SAYIMOV', callback_data='AZIM_SAYIMOV')
    button_zohid = InlineKeyboardButton('ABDULLAYEV ZOHID', callback_data='ABDULLAYEV_ZOHID')
    button_qodirov = InlineKeyboardButton('ABBOS QODIROV', callback_data='ABBOS_QODIROV')
    button_mamadiyev = InlineKeyboardButton('JAMSHID MAMADIYEV', callback_data='JAMSHID_MAMADIYEV')
    button_narzullayev = InlineKeyboardButton('FAZLIDDIN NARZULLAYEV', callback_data='FAZLIDDIN_NARZULLAYEV')
    button_back = InlineKeyboardButton('🔙Orqaga', callback_data='back')
    keyboard.add(button_obidov, button_qurbonov,
                 button_ruziyev,button_karimov,
                 button_bozorov,button_sayimov,
                 button_zohid,button_qodirov,
                 button_mamadiyev,button_narzullayev,button_back)
    await bot.send_message(user_id,text=message_text, reply_markup=keyboard,
                         parse_mode=types.ParseMode.MARKDOWN)
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
