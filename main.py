import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.methods import DeleteWebhook
from aiogram.types import Message

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

mistral_api_key = "4wyfTKOF17yx2V5veUXaefiF39FkQSkp"
TOKEN = '7623755774:AAHfIGTzbIGQOxcQf5Q1LqXQoaCYjIaamsU'

model = "mistral-large-latest"
client = MistralClient(api_key=mistral_api_key)

chat_history = {}

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer('Привет! Я - бот с подключенной нейросетью, отправь свой запрос')

@dp.message(F.text)
async def filter_messages(message: Message):
    chat_id = message.chat.id

    if chat_id not in chat_history:
        chat_history[chat_id] = [
            ChatMessage(role="system", content="")
        ]

    chat_history[chat_id].append(
        ChatMessage(role="user", content=message.text)
    )

    response = client.chat(
        model=model,
        messages=chat_history[chat_id]
    )

    response_text = response.choices[0].message.content

    chat_history[chat_id].append(
        ChatMessage(role="assistant", content=response_text)
    )

    if len(chat_history[chat_id]) > 10:
        chat_history[chat_id] = [chat_history[chat_id][0]] + chat_history[chat_id][-9:]

    await message.answer(response_text, parse_mode="Markdown")

async def main():
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
