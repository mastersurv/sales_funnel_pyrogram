from pyrogram import Client, types
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db import engine, metadata
from models import User
import asyncio
from pyrogram.methods.utilities.idle import idle
from db import DATABASE_URL, get_users, add_user, user_exists
import datetime

api_id =
api_hash =
app = Client('my_account', api_id=api_id, api_hash=api_hash)

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@app.on_message()
async def handle_message(client, message: types.Message):
	# Данные нового пользователя
	user_data = {
		"id": message.from_user.id,
		"created_at": datetime.datetime.utcnow(),
		"status": "active",
		"status_updated_at": datetime.datetime.utcnow()
	}
	# Проверка существования пользователя в базе данных
	if await user_exists(async_session, user_data['id'], User):
		print("Пользователь уже существует в базе данных")
	else:
		await add_user(async_session, user_data, User)

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
