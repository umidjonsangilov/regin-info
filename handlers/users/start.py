from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
import requests
from loader import dp,db,bot
from aiogram.dispatcher import FSMContext
from keyboards.default.req import location
from filters.chat_filtr import IsPrivate
import wikipedia
from googletrans import Translator
from bs4 import BeautifulSoup
from aiogram.types import InlineKeyboardMarkup as IKM, InlineKeyboardButton as IKB


@dp.message_handler(IsPrivate(), CommandStart())
async def bot_start(message: types.Message):
    user_id=message.from_user.id
    name = message.from_user.full_name
    link = message.from_user.mention
    user=db.user(user_id)
    if not user:
        x = db.new_user(user_id)
        await bot.send_message(-1001463084469, f"Bot: @regioninfobot\n\nYangi foydalanuvchi: <code>{user_id}</code>\n"
                               f"Ismi: {name}\nLink: {link}")
        await message.answer(f"Siz botga {x}-bo'lib qo'shildingiz")
    await message.answer(f"Salom, {message.from_user.full_name}!\n\n"
                         "Menga lokatsiya yuboring va men sizga shu joy haqida ma'lumot beraman."
                         "O'zingiz turgan joy uchun pastdagi tugmani bosing. Boshqa joyni ko'rish uchun 📎 ni bosib joylashuvni tanlab shu yerdan belgilang."
                         "Yoki geografik kordinatasini yuboring(komyuterda bo'lsangiz shu usuldan foydalaning.) M-n: <code>41.23925762892969, 69.33607143345013</code> shu ko'rinishda."
                         "Buni onlayn xaritalardan olish mumkin.",
                         reply_markup=location)

@dp.message_handler(IsPrivate(),content_types="text")
@dp.message_handler(IsPrivate(),content_types="location")
async def req_location(message: types.Message, state:FSMContext):
    user_id=message.from_user.id
    if message.location:
        location_user = message.location
        lat = location_user.latitude
        lng = location_user.longitude
    else:
        location_user = message.text.split(", ")
        lat = float(location_user[0])
        lng = float(location_user[1])
        if not (-90<lat<90 and -180<lng<180):
            await message.answer("Bu kordinata mavjud emas.")
            return
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}"
    response = requests.get(url)

    data = response.json()
    if 'error' not in data:
        reg = IKM(row_width=1)

        address:dict = data["address"]

        x = address["country_code"].upper()
        country = address['country']
        text = f"<b>Davlat:</b> {country} {chr(0x1F1E6 + ord(x[0]) - ord('A')) + chr(0x1F1E6 + ord(x[1]) - ord('A'))}.\n"
        reg.insert(IKB(text=f"{country}",callback_data=f"{country}"))

        region = address.get('region')
        sstate = address.get('state')
        county = address.get("county")
        district = address.get("district")
        city = address.get("city")
        town = address.get("town")
        village = address.get("village")
        road = address.get("road")

        if region:
            text += f"<b>Region:</b> {region}.\n"
            reg.insert(IKB(text=f"{region}",callback_data=f"{region}"))
        if sstate:
            text += f"<b>Region:</b> {sstate}.\n"
            reg.insert(IKB(text=f"{sstate}",callback_data=f"{sstate}"))
        if county:
            text += f"<b>Tuman:</b> {county}.\n"
            reg.insert(IKB(text=f"{county}",callback_data=f"{county}"))
        if district:
            text += f"<b>Tuman:</b> {district}.\n"
            reg.insert(IKB(text=f"{district}",callback_data=f"{district}"))
        if city:
            text += f"<b>Shaxar:</b> {city}.\n"
            reg.insert(IKB(text=f"{city}",callback_data=f"{city}"))
        if town:
            text += f"<b>Shaxar:</b> {town}.\n"
            reg.insert(IKB(text=f"{town}",callback_data=f"{town}"))
        if village:
            text += f"<b>Qishloq:</b> {village}.\n"
            reg.insert(IKB(text=f"{village}",callback_data=f"{village}"))
        if road:
            text += f"<b>Yo'l:</b> {road}.\n"
        
        await message.answer("Siz yuborgan joylashuv kordinatasi.\n\n"
                             f"<b>Kenglik:</b> {lat}\n<b>Uzunlik:</b> {lng}\n\n"
                             f"{text}",reply_markup=reg)
        

        # tr =Translator()
        # print(tr.translate(country, "uz").text)



        # wikipedia.set_lang("uz")
        # try:
        #     respond = wikipedia.summary(f"{tr.translate(country, 'uz').text}")
        #     await message.answer(f"<b>{country}</b>\n\n{respond}")
        # except: pass

        # print(wikipedia.page(tr.translate(country, "uz").text,pageid=1))


        # try:
        #     respond = wikipedia.summary(region)
        #     await message.answer(f"<b>{region}</b>\n\n{respond}")
        # except: pass

        # try:
        #     respond = wikipedia.summary(sstate)
        #     await message.answer(f"<b>{sstate}</b>\n\n{respond}")
        # except: pass

        # try:
        #     respond = wikipedia.summary(county)
        #     await message.answer(f"<b>{county}</b>\n\n{respond}")
        # except: pass

        # try:
        #     respond = wikipedia.summary(city)
        #     await message.answer(f"<b>{city}</b>\n\n{respond}")
        # except: pass

        # try:
        #     respond = wikipedia.summary(town)
        #     await message.answer(f"<b>{town}</b>\n\n{respond}")
        # except: pass

        # try:
        #     respond = wikipedia.summary(village)
        #     await message.answer(f"<b>{village}</b>\n\n{respond}")
        # except: pass

        # try:
        #     respond = wikipedia.summary(country)
        #     await message.answer(respond)
        # except: pass

        # try:
        #     respond = wikipedia.summary(country)
        #     await message.answer(respond)
        # except: pass



        await bot.send_message(-1001463084469, "Bot: @regioninfobot\n#location\n\n"
                           f"Foydalanuvchi lokatsiya yubordi.\nuser id: <code>{user_id}</code>\n\n"
                           f"<b>Kenglik:</b> {lat}\n<b>Uzunlik:</b> {lng}\n\n"
                           f"{text}")
    else:
        await message.answer("Nomalum xatolik. Qaytadan yuboring. Balki bu yerda hech nima yo'qdir.")