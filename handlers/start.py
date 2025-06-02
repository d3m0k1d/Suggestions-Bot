import os
import json
from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from keyboards.config_keyboard import *

router = Router()

ADMIN_FILE = 'admin.json'


def load_config():
    if not os.path.exists(ADMIN_FILE):
        return {'admin': [], 'forum_chat_id': None}
    with open(ADMIN_FILE, 'r', encoding='utf-8') as file:
        data = json.load(file)
        if 'forum_chat_id' not in data:
            data['forum_chat_id'] = None
        return data


def save_config(config):
    with open(ADMIN_FILE, 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)


def load_admins():
    config = load_config()
    return config.get('admin', [])


def save_admins(admin_ids):
    config = load_config()
    config['admin'] = admin_ids
    save_config(config)


def parse_admin_ids(text):
    return [i.strip() for i in text.split(',') if i.strip().isdigit()]


class AdminStates(StatesGroup):
    waiting_for_admins = State()
    waiting_for_forum_chat_id = State()


@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    config = load_config()
    if not config['admin'] and not config['forum_chat_id']:
        await message.answer(
            text="⚠️ Это первый запуск бота пожалуйста укажите администраторов и чат-форум для того что бы начать работу!",
            reply_markup=full_config_keyboard)

    if not config.get('forum_chat_id'):
        await message.answer(
            "⚠️ Чат-форум не настроен. Для завершения настройки укажите ID чата",
            reply_markup=keyboard_only_for_add_themes
        )

    if message.from_user.id not in load_admins():
        await message.answer("Добро пожаловать в бот предложку, напишите свое предложение")

    if message.from_user.id in parse_admin_ids(message.text):
        pass


class AdminStates(StatesGroup):
    waiting_for_admins = State()
    waiting_for_forum_chat_id = State()


@router.callback_query(F.data == 'add_admins')
async def add_admins_callback(callback_query: CallbackQuery, state: FSMContext):
    config = load_config()
    admins_exist = bool(config.get('admin'))
    admins = config.get('admin', [])

    await callback_query.answer()

    if admins_exist and str(callback_query.from_user.id) not in admins:
        await callback_query.message.answer("❌ Вы не являетесь администратором.")
        return

    await callback_query.message.answer("📝 Введите ID администраторов через запятую:")
    await state.set_state(AdminStates.waiting_for_admins)


@router.message(AdminStates.waiting_for_admins)
async def process_admins_input(message: Message, state: FSMContext):
    config = load_config()
    admin_ids = parse_admin_ids(message.text)

    if not admin_ids:
        await message.answer("❌ Некорректный формат. Используйте только числа через запятую.")
        return

    config['admin'] = admin_ids
    save_config(config)
    await message.answer(f"✅ Администраторы успешно обновлены:\n{', '.join(admin_ids)}")

    if not config.get('forum_chat_id'):
        await message.answer(
            "⚠️ Чат-форум не настроен. Для завершения настройки укажите ID чата",
            reply_markup=keyboard_only_for_add_themes
        )
    await state.clear()


@router.callback_query(F.data == 'add_themes')
async def set_forum_chat_callback(callback_query: CallbackQuery, state: FSMContext):
    config = load_config()
    admins = config.get('admin', [])

    await callback_query.answer()

    if str(callback_query.from_user.id) not in admins:
        await callback_query.message.answer("❌ Доступ запрещён. Требуются права администратора.")
        return

    await callback_query.message.answer("🌐 Введите ID чата-форума:")
    await state.set_state(AdminStates.waiting_for_forum_chat_id)


@router.message(AdminStates.waiting_for_forum_chat_id)
async def process_forum_chat_id(message: Message, state: FSMContext):
    config = load_config()
    chat_id = message.text.strip()

    try:
        chat = await message.bot.get_chat(chat_id)

        if not getattr(chat, "is_forum", False):
            await message.answer("❌ Ошибка: указанный чат не поддерживает темы.")
            return

        admins_list = await message.bot.get_chat_administrators(chat_id)
        bot_member = next((m for m in admins_list if m.user.id == message.bot.id), None)

        if not bot_member:
            await message.answer("❌ Ошибка: бот не добавлен как администратор.")
            return

        if not getattr(bot_member, "can_manage_topics", False):
            await message.answer("❌ Ошибка: недостаточно прав для управления темами.")
            return

    except Exception as e:
        await message.answer(f"❌ Ошибка проверки чата:\n{str(e)}")
        await message.answer("⚠️ Попробуйте еще раз")
        return

    config['forum_chat_id'] = chat_id
    save_config(config)
    await message.answer(f"✅ Чат-форум успешно настроен:\nID: {chat_id}")
    await state.clear()
