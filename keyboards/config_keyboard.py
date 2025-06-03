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

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Посмотреть текующую конфигурацию", callback_data='get_config_bot')],
    [InlineKeyboardButton(text="Добавить администаторов", callback_data='add_admins'), InlineKeyboardButton(text="Удалить администратора", callback_data='del_admin')],
    [InlineKeyboardButton(text="Добавить чат-форум", callback_data='add_themes'), InlineKeyboardButton(text="Удалить чат-форум", callback_data='del_forum_chat')],
    [InlineKeyboardButton(text="Сбросить конфигруцаию", callback_data='del_config_bot')]
])


approved_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да", callback_data='del_confirm_config_bot'), InlineKeyboardButton(text="Нет", callback_data='del_notconfirm_config_bot')],
])