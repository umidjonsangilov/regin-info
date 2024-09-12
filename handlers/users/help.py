from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp
from filters.chat_filtr import IsPrivate
from loader import dp, db


@dp.message_handler(IsPrivate(),CommandHelp())
async def bot_help(message: types.Message):
    text = ("Buyruqlar: ",
            "/start - Botni ishga tushirish",
            "/stat - statistikani ko'rish"
            "admin @Umidjon_Sangilov")
    
    await message.answer("\n".join(text))

@dp.message_handler(IsPrivate(),commands="stat", state="*")
async def stat(message: types.Message):
    user_count = db.stat_bot()[0]
    print(user_count)
    await message.answer("Bot ishga tushgan sana: 27.04.2024 Soat: 21:22.\n\n"
                         f"Bot statstikasi:\n\nOxirgi bir oyda qo'shilganlar: {user_count[0]} ta.\n"
                         f"Oxirgi bir kunda qo'shilganlar: {user_count[1]} ta.")
