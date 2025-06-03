import os
from dotenv import load_dotenv
import json
from aiogram import Router, Bot
from aiogram.types import Message

router = Router()
load_dotenv()
bot_username = os.getenv("bot_username")


def load_config():
    try:
        with open('admin.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {'admin': [], 'forum_chat_id': None}


@router.message()
async def handle_user_message(message: Message, bot: Bot):
    config = load_config()
    admins = config.get('admin', [])
    forum_chat_id = config.get('forum_chat_id')

    if not forum_chat_id:
        await message.answer("❌ Форум-чат не настроен администратором")
        return

    if str(message.from_user.id) in admins:
        return

    has_content = False

    if message.text and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.username}",
            icon_color=7322096
        )

        await bot.send_message(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            text=message.text
        )
    if message.photo and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.username}",
            icon_color=7322096
        )

        await bot.send_photo(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            photo=message.photo[-1].file_id,
            caption=message.caption or message.text or ""
        )

    if message.video and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.username}",
            icon_color=7322096
        )

        await bot.send_video(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            video=message.video.file_id,
            caption=message.caption or message.text or ""
        )

    if message.document and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.username}",
            icon_color=7322096
        )

        await bot.send_document(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            document=message.document.file_id,
            caption=message.caption or message.text or ""
        )
    if message.audio and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.username}",
            icon_color=7322096
        )

        await bot.send_audio(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            audio=message.audio.file_id,
            caption=message.caption or message.text or ""
        )

    if message.sticker and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.username}",
            icon_color=7322096
        )

        await bot.send_sticker(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            sticker=message.sticker.file_id
        )

    if message.animation and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.username}",
            icon_color=7322096
        )

        await bot.send_animation(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            animation=message.animation.file_id,
            caption=message.caption or message.text or ""
        )

    if message.voice and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.id}",
            icon_color=7322096
        )

        await bot.send_voice(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            voice=message.voice.file_id,
            caption=message.caption or message.text or ""
        )

    if message.video_note and message.from_user.username != bot_username:
        topic = await bot.create_forum_topic(
            chat_id=forum_chat_id,
            name=f"Предложка от @{message.from_user.id}",
            icon_color=7322096
        )

        await bot.send_video_note(
            chat_id=forum_chat_id,
            message_thread_id=topic.message_thread_id,
            video_note=message.video_note.file_id
        )
