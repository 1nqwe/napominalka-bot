from aiogram.types import ReplyKeyboardMarkup
from aiogram import types

def main_keyboard():
    main_kb = [
        [types.KeyboardButton(text='Команды')],
        [
            types.KeyboardButton(text='Профиль'),
            types.KeyboardButton(text='О боте')
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=main_kb, resize_keyboard=True)




def get_timezone_kb():
    timezone_kb = [
    [
            types.InlineKeyboardButton(text='UTC+2', callback_data='2'),
            types.InlineKeyboardButton(text='UTC+3', callback_data='3'),
        ],
        [
            types.InlineKeyboardButton(text='UTC+4', callback_data='4'),
            types.InlineKeyboardButton(text='UTC+5', callback_data='5'),
        ],
        [
            types.InlineKeyboardButton(text='UTC+6', callback_data='6'),
            types.InlineKeyboardButton(text='UTC+7', callback_data='7'),
        ],
        [
            types.InlineKeyboardButton(text='UTC+8', callback_data='8'),
            types.InlineKeyboardButton(text='UTC+9', callback_data='9'),
        ],
        [
            types.InlineKeyboardButton(text='UTC+10', callback_data='10'),
            types.InlineKeyboardButton(text='UTC+11', callback_data='11'),
        ],
        [
            types.InlineKeyboardButton(text='UTC+12', callback_data='12')
        ]

    ]
    return types.InlineKeyboardMarkup(inline_keyboard=timezone_kb)
