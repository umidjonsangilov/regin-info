from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

location = ReplyKeyboardMarkup(resize_keyboard=True,keyboard=[
    [KeyboardButton(text="📍Joriy joylashuvni yuborish↗️", request_location=True)]
])