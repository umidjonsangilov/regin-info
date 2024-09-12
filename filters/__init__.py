from loader import dp
from .chat_filtr import AdminFilter, IsGroup, IsPrivate

if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
