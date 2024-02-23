from pyrogram import Client
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db import engine, metadata
from models import User
import asyncio
from pyrogram.methods.utilities.idle import idle
from db import DATABASE_URL, get_users, add_user
import datetime

api_id =
api_hash =
app = Client('my_account', api_id=api_id, api_hash=api_hash)

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@app.on_message()
async def handle_message(client, message):
	# Данные нового пользователя
	new_user_data = {
		"created_at": datetime.datetime(2024, 2, 23, 12, 0, 0),
		"status": "active",
		"status_updated_at": datetime.datetime(2024, 2, 23, 12, 0, 0)
	}
	if "добавить" in message.text:
		await message.reply("Вы добавлены в базу данных")
		await add_user(async_session, new_user_data, User)

	# Код обработки сообщения
	if "прекрасно" in message.text or "ожидать" in message.text:
		await message.reply("Прекрасно или ожидание обнаружены. Воронка прекращена.")
		# Логика изменения статуса пользователя в базе данных
		users = await get_users(async_session, User)


async def main():
	await app.start()
	await idle()


if __name__ == "__main__":
	app.loop.run_until_complete(main())
