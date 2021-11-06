from aiogram import Bot, Dispatcher, executor, types
from auth_data import auth_data
import parser


bot = Bot(token=auth_data['token'])
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.answer('Hello!')


@dp.message_handler(commands='get_brand')
async def get_brand(message: types.Message):
    try:
        article = message.get_args()
        brand = await parser.get_brand(f'https://www.wildberries.ru/catalog/{article}/detail.aspx')
        parser.write_brand_db(article, brand)
        await message.reply(f'This article belongs to {brand}')
    except:
        await message.reply('Check that you type correct article!')


@dp.message_handler(commands='get_title')
async def get_title(message: types.Message):
    try:
        article = message.get_args()
        title = await parser.get_title(f'https://www.wildberries.ru/catalog/{article}/detail.aspx')
        parser.write_title_db(article, title)
        await message.reply(f'Product with this article has the next title: {title}')
    except:
        await message.reply('Check that you type correct article!')


def main():
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
