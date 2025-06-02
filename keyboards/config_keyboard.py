from gc import callbacks

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

"""Inline kb for admin panel"""
full_config_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить администраторов", callback_data='add_admins'),
     InlineKeyboardButton(text="Добавить чат-форум", callback_data='add_themes')],
    [InlineKeyboardButton(text="Инструкция", callback_data='start_guide')]
])

keyboard_without_guide = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить администраторов", callback_data='add_admins'),
     InlineKeyboardButton(text="Добавить чат-форум", callback_data='add_themes')],
])

keyboard_only_for_add_themes = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Добавить чат-форум", callback_data='add_themes')],
])
