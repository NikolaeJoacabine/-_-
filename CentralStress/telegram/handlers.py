import logging
from aiogram import types, Router, F, Bot
from telegram import bot_db
from aiogram.filters import Command
from dotenv import dotenv_values
import cv.face_db
import os

config = dotenv_values(".env")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = Router()
person_data = {}
BOT_TOKEN = config["BOT_TOKEN"]
bot = Bot(token="7985787217:AAFyHwZsHfQigij2u41ymyxF_XfuDFP7Nn8")

add_kb = [
    [
        types.KeyboardButton(text="Создать аккаунт"),
        types.KeyboardButton(text="Войти в аккаунт"),
    ],
]
add_keyboard = types.ReplyKeyboardMarkup(
    keyboard=add_kb,
    resize_keyboard=True,
)

undo_kb = [
    [
        types.KeyboardButton(text="Отмена создания"),
    ],
]
undo_keyboard = types.ReplyKeyboardMarkup(
    keyboard=undo_kb,
    resize_keyboard=True,
)

menu_kb = [
    [
        types.KeyboardButton(text="Статистика"),
    ],
]
menu_keyboard = types.ReplyKeyboardMarkup(
    keyboard=menu_kb,
    resize_keyboard=True,
)

vibes = {}


@router.message(Command("start"))
async def start(message: types.Message):
    logger.info(f"Received message from user {message.from_user.id}")
    await message.answer(config["GREETING"], reply_markup=add_keyboard)


@router.message(F.text.lower() == "создать аккаунт")
@router.message(Command("register"))
async def add_person(message: types.Message):
    logger.info(f"User {message.from_user.id} started adding a person")
    person_data[message.from_user.id] = {}
    await message.answer('Введите ваше Фамилию и Имя', reply_markup=undo_keyboard)


@router.message(F.text.lower() == "войти в аккаунт")
@router.message(Command("login"))
async def add_person(message: types.Message):
    logger.info(f"User {message.from_user.id} start login")
    person_data[message.from_user.id] = {}
    await message.answer('Вы вошли в аккаунт!', reply_markup=menu_keyboard)


@router.message(F.text.lower() == "отмена создания")
async def undo(message: types.Message):
    del person_data[message.from_user.id]
    await message.answer('Создание аккаунта отменено', reply_markup=add_keyboard)


@router.message(F.text.lower() == "статистика")
async def add_person(message: types.Message):
    bot_db.get_vibe(message.from_user.id)
    print(bot_db.get_vibe(message.from_user.id))
    if len(bot_db.get_vibe(message.from_user.id)) == 0:
        await message.answer(
            'Здесь будет приходить статистика эмоционального состояния, но пока мы ещё недостаточно знакомы!',
            reply_markup=menu_keyboard)
    else:
        await message.answer(
            f'Ваше последнее состояние - {bot_db.get_vibe(message.from_user.id)}',
            reply_markup=menu_keyboard)
    logger.info(f"User {message.from_user.id} start login")
    person_data[message.from_user.id] = {}


@router.message(F.photo)
async def get_photo(message: types.Message):
    if message.from_user.id in person_data:
        logger.info(f"User {message.from_user.id} sent photo")
        person_data[message.from_user.id]['photo'] = message.photo[-1].file_id
        logger.info(f"Get photo - {message.photo}")
        bot_db.add_user(message.from_user.id, person_data[message.from_user.id])
        await message.answer('Ваш аккаунт создан!', reply_markup=menu_keyboard)
        # передаем фото в другую часть кода
        await process_photo(message, person_data[message.from_user.id]['photo'])


@router.message()
async def get_name(message: types.Message):
    if message.from_user.id in person_data:
        logger.info(f"User {message.from_user.id} sent name: {message.text}")
        person_data[message.from_user.id]['name'] = message.text
        await message.answer('Отправьте фото вашего лица', reply_markup=undo_keyboard)


async def process_photo(message, photo_id):
    await bot.download(file=photo_id, destination=f"C:\\Users\\User14\\PycharmProjects\\CentralStress\\database\\faces\\{photo_id}.jfif")
    logging.info("Photo saved")
    image_path = f"C:\\Users\\User14\\PycharmProjects\\CentralStress\\database\\faces\\{photo_id}.jfif"
    cv.face_db.add_new_face(image_path, person_data[message.from_user.id]['name'])
    del person_data[message.from_user.id]
    if os.path.exists(image_path):
        os.remove(image_path)
    else:
        logging.info("Photo does not exist")
