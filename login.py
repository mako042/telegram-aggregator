import asyncio
from telethon import TelegramClient
import os

async def create_session():
    api_id = int(os.getenv('API_ID'))
    api_hash = os.getenv('API_HASH')
    phone_number = os.getenv('PHONE_NUMBER')
    bot_token = os.getenv('BOT_TOKEN')

    # Создаем клиенты
    client = TelegramClient('/app/sessions/user_session', api_id, api_hash)
    bot = TelegramClient('/app/sessions/bot_session', api_id, api_hash)

    try:
        # Запускаем клиент пользователя
        await client.start(phone=phone_number)
        print("✅ Сессия юзера успешно создана!")
        
        # Запускаем бота
        await bot.start(bot_token=bot_token)
        print("✅ Сессия бота успешно создана!")

        # Получаем информацию о пользователе
        me = await client.get_me()
        print(f"✅ Вы вошли как: {me.first_name}")

        # Получаем информацию о боте
        bot_me = await bot.get_me()
        print(f"✅ Бот: @{bot_me.username}")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        # Корректно закрываем соединения
        await client.disconnect()
        await bot.disconnect()
        print("✅ Сессии закрыты")

if __name__ == '__main__':
    asyncio.run(create_session())
