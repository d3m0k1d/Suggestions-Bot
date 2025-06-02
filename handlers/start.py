import os
import json
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

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
    """Сохранить конфигурацию в файл"""
    with open(ADMIN_FILE, 'w', encoding='utf-8') as file:
        json.dump(config, file, ensure_ascii=False, indent=2)


def load_admins():
    """Загрузить список администраторов (для обратной совместимости)"""
    config = load_config()
    return config.get('admin', [])


def save_admins(admin_ids):
    """Сохранить список администраторов (для обратной совместимости)"""
    config = load_config()
    config['admin'] = admin_ids
    save_config(config)


def parse_admin_ids(text):
    """Парсит строку с id админов, возвращает список строк-чисел"""
    return [i.strip() for i in text.split(',') if i.strip().isdigit()]


@router.message(CommandStart())
async def start(message: Message, bot: Bot):
    config = load_config()

    if not config['admin']:
        await message.answer(
            "В боте не указаны администраторы.\n"
            "Добавьте их командой:\n"
            "/add_admins 12345,67890"
        )
    elif not config['forum_chat_id']:
        await message.answer(
            "Чат с темами не настроен.\n"
            "1. Создайте супергруппу с режимом форума\n"
            "2. Добавьте бота как администратора с правами управления темами\n"
            "3. Укажите ID чата командой:\n"
            "/set_forum_chat <ID_чата>"
        )
    else:
        await message.answer("Бот готов к работе!")


@router.message(Command("add_admins"))
async def add_admins(message: Message):
    config = load_config()
    admins_exist = bool(config['admin'])
    admins = config.get('admin', [])

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer(
            "Пожалуйста, укажите id администраторов через запятую:\n"
            "/add_admins 12345,67890"
        )
        return

    admin_ids = parse_admin_ids(args[1])
    if not admin_ids:
        await message.answer("Некорректный формат. Используйте только числа через запятую.")
        return

    if admins_exist:
        if str(message.from_user.id) not in admins:
            await message.answer("Вы не являетесь администратором.")
            return
        config['admin'] = admin_ids
        save_config(config)
        await message.answer(f"Администраторы обновлены: {', '.join(admin_ids)}")
    else:
        config['admin'] = admin_ids
        save_config(config)
        await message.answer(f"Администраторы добавлены: {', '.join(admin_ids)}")

    if not config.get('forum_chat_id'):
        await message.answer(
            "⚠️ Не забудьте настроить чат с темами командой /set_forum_chat"
        )


@router.message(Command("set_forum_chat"))
async def set_forum_chat(message: Message, bot: Bot):
    """Установка ID форум-чата"""
    config = load_config()
    admins = config.get('admin', [])

    if str(message.from_user.id) not in admins:
        await message.answer("❌ Вы не являетесь администратором")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Укажите ID чата: /set_forum_chat <ID_чата>")
        return

    chat_id = args[1].strip()
    try:
        chat = await bot.get_chat(chat_id)

        # Проверяем, является ли чат форумом
        if not getattr(chat, "is_forum", False):
            await message.answer("❌ Указанный чат не является форумом")
            return

        # Проверяем права бота в чате
        admins_list = await bot.get_chat_administrators(chat_id)
        bot_member = next((m for m in admins_list if m.user.id == bot.id), None)

        if not bot_member:
            await message.answer("❌ Бот не является администратором в этом чате")
            return

        if not getattr(bot_member, "can_manage_topics", False):
            await message.answer("❌ Бот не имеет прав управления темами в этом чате")
            return

    except Exception as e:
        await message.answer(f"❌ Ошибка при проверке чата: {str(e)}")
        return

    config['forum_chat_id'] = chat_id
    save_config(config)
    await message.answer(f"✅ Чат форума установлен: {chat_id}")


@router.message(Command("create_topic"))
async def create_topic(message: Message, bot: Bot):
    """Создание новой темы в форум-чате"""
    config = load_config()
    admins = config.get('admin', [])

    if str(message.from_user.id) not in admins:
        await message.answer("❌ Вы не являетесь администратором")
        return

    if not config.get('forum_chat_id'):
        await message.answer("❌ Форум-чат не настроен. Используйте /set_forum_chat")
        return

    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.answer("❌ Укажите название темы: /create_topic <название>")
        return

    topic_name = args[1].strip()
    if not topic_name:
        await message.answer("❌ Название темы не может быть пустым")
        return

    try:
        topic = await bot.create_forum_topic(
            chat_id=config['forum_chat_id'],
            name=topic_name,
            icon_color=7322096  # Синий цвет по умолчанию
        )
        await message.answer(f"✅ Тема создана: {topic.name} (ID: {topic.message_thread_id})")
    except Exception as e:
        await message.answer(f"❌ Ошибка при создании темы: {str(e)}")


@router.message(Command("forum_info"))
async def forum_info(message: Message, bot: Bot):
    """Информация о настроенном форум-чате"""
    config = load_config()
    admins = config.get('admin', [])

    if str(message.from_user.id) not in admins:
        await message.answer("❌ Вы не являетесь администратором")
        return

    if not config.get('forum_chat_id'):
        await message.answer("❌ Форум-чат не настроен")
        return

    try:
        chat = await bot.get_chat(config['forum_chat_id'])
        info = f"📋 Информация о форум-чате:\n\n"
        info += f"Название: {chat.title}\n"
        info += f"ID: {chat.id}\n"
        info += f"Тип: {'Форум' if getattr(chat, 'is_forum', False) else 'Обычный чат'}\n"
        info += f"Описание: {chat.description or 'Не указано'}"

        await message.answer(info)
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении информации: {str(e)}")


@router.message(Command("config"))
async def show_config(message: Message):
    """Показать текущую конфигурацию"""
    config = load_config()
    admins = config.get('admin', [])

    if str(message.from_user.id) not in admins:
        await message.answer("❌ Вы не являетесь администратором")
        return

    info = "⚙️ Текущая конфигурация:\n\n"
    info += f"Администраторы: {', '.join(admins) if admins else 'Не указаны'}\n"
    info += f"Форум-чат: {config.get('forum_chat_id', 'Не настроен')}"

    await message.answer(info)