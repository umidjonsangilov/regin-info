from typing import Union
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from data.config import ADMINS
from loader import db

class BotAdmin(BoundFilter):
    async def check(self, message: types.Message):
        return str(message.from_user.id) in ADMINS

class IsPrivate(BoundFilter):
    async def check(self, message: Union[types.Message, types.CallbackQuery]):
        if isinstance(message, types.Message):
            return message.chat.type == types.ChatType.PRIVATE
        elif isinstance(message, types.CallbackQuery):
            return message.message.chat.type == types.ChatType.PRIVATE

class IsGroup(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return message.chat.type in (
            types.ChatType.GROUP,
            types.ChatType.SUPERGROUP,
        )

class AdminFilter(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        member = await message.chat.get_member(message.from_user.id)
        return member.is_chat_admin()

class IsBotUser(BoundFilter):
    async def check(self, message: types.Message):
        users = db.users()
        return message.from_user.id not in users
