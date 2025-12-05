from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat
import os
import asyncio
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
phone_number=os.getenv('PHONE_NUMBER')
bot_token=os.getenv('BOT_TOKEN')

#ID целевого чата (куда будут приходить все сообщения)
TARGET_CHAT_ID = int(os.getenv('TARGET_CHAT_ID'))  # Замените на ID вашей группы/канала

# Список чатов-источников (username)
source_chats=os.getenv('SOURCE_CHATS')
source_chats = [chat.strip() for chat in source_chats.split(',') if chat.strip()]


SOURCE_CHATS = source_chats

chat_ids = []

async def main():
    # Инициализируем клиента внутри async функции
    client = TelegramClient('/app/sessions/user_session', api_id, api_hash)
    bot = TelegramClient('/app/sessions/bot_session', api_id, api_hash)
    await client.start(phone=phone_number)
    await bot.start(bot_token=bot_token)

    global chat_ids
    chat_ids = []

    async for dialog in client.iter_dialogs():
        if dialog.name in SOURCE_CHATS:
            chat_ids.append(dialog.id)
            logger.info(f"Найден чат: {dialog.name} -> {dialog.id}")

    if not chat_ids:
        logger.error("Не найдены указанные чаты!")
        return False

    @client.on(events.NewMessage(chats=chat_ids))
    async def message_handler(event):
        try:
            sender = await event.get_sender()
            if sender.bot:
                return
            username = sender.username
            if username:
                username_display = f"@{username}"
            else:
                username_display = ""
            if isinstance(event.chat, (Channel, Chat)):
                chat_title = event.chat.title  # У каналов и групп есть title
            else:
                chat_title = f"{sender.first_name} {username_display}".strip()
            # Создаем ссылку на сообщение
            chat_id_raw = str(event.chat_id)
            if chat_id_raw.startswith('-100'):
                chat_id_clean = chat_id_raw[4:]  # Убираем '-100'
            else:
                chat_id_clean = chat_id_raw
        
            message_link = f"https://t.me/c/{chat_id_clean}/{event.message.id}"

            if event.chat:
                info_text = (
                    f"**📨 Сообщение из:** {chat_title}\n"
                    f"**🔗 Ссылка:** {message_link}\n"
                    f"**💬 От:** {sender.first_name} {username_display}\n"
                    f"━━━━━━━━━━━━━━━━"
                    f"\n{event.message.message}"
                )

                
            else:
                info_text = (
                    f"**💬 Сообщение от пользователя:** {sender.first_name} {username_display}\n"
                    f"━━━━━━━━━━━━━━━━\n"
                    f"\n{event.message.message}"
                )
            await bot.send_message(
                TARGET_CHAT_ID, 
                info_text,
                link_preview=False
            )

#            await bot.forward_messages(TARGET_CHAT_ID, event.message)

#            await client.send_message(TARGET_CHAT_ID, "Из чата "+event.chat.title)
#            await client.forward_messages(TARGET_CHAT_ID, event.message)

            if event.chat:
                logger.info(f"Переслано сообщение {chat_title}")
            else:
                logger.info(f"Переслано сообщение от {sender.first_name} {username_display}")
        except Exception as e:
            await bot.send_message(TARGET_CHAT_ID, "Не удалось переслать сообщение: \n"+str(event.original_update))
            logger.error(f"Ошибка при пересылке: {e}\nСобытие: \n{event}")

    logger.info("Бот-агрегатор запущен!")
    logger.info(f"Отслеживаются чаты: {chat_ids}")
    
    # Запускаем прослушивание
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
