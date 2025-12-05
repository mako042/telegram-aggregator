from telethon import TelegramClient
import asyncio
import os

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone_number = os.getenv('PHONE_NUMBER')

async def main():
    client = TelegramClient('/app/sessions/user_session', api_id, api_hash)
    await client.start(phone=phone_number)
    
    # Получаем список всех диалогов
    async for dialog in client.iter_dialogs():
        print(f"{dialog.name}: ID = {dialog.id}")
    
    await client.disconnect()

asyncio.run(main())
