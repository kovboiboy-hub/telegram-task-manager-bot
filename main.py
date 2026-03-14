import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from database import Database  # Импортируем наш класс из соседнего файла

load_dotenv() # Загружаем токен из .env
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
db = Database()

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Бот запущен! Напиши задачу или используй /tasks")

@dp.message(Command("tasks"))
async def show_tasks(message: Message):
    tasks = await db.get_tasks(message.from_user.id)
    if not tasks:
        await message.answer("Задач нет.")
        return

    for task_id, text in tasks:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Удалить", callback_data=f"delete_{task_id}")]
        ])
        await message.answer(f"• {text}", reply_markup=keyboard)

@dp.callback_query(F.data.startswith("delete_"))
async def delete_callback(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    await db.delete_task(task_id)
    await callback.message.edit_text(f"{callback.message.text}", parse_mode="HTML")
    await callback.answer("Удалено")

@dp.message()
async def handle_text(message: Message):
    await db.add_task(message.from_user.id, message.text)
    await message.reply("Записал!")

async def main():
    await db.init()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
