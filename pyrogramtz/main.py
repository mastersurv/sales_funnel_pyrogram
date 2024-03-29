from pyrogram import Client, types, filters
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from db import engine, metadata
from models import User
import asyncio
from pyrogram.methods.utilities.idle import idle
from db import DATABASE_URL, get_users, add_user, user_exists, get_user, update_user, update_status
import datetime
from datetime import timedelta
from pyrogram.errors import FloodWait, UserBlocked, UserDeactivated


api_id = 27690174
api_hash = "f90b8c2a7fae9ea03131dedb302d3019"
app = Client('my_account', api_id=api_id, api_hash=api_hash)

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@app.on_message(filters.private)
async def handle_message(client, message: types.Message):
	user_data = {
		"id": message.from_user.id,
		"created_at": datetime.datetime.utcnow(),
		"status": "active",
		"status_updated_at": datetime.datetime.utcnow()
	}
	user_id = user_data['id']
	if await user_exists(async_session, user_id, User):
		print("Пользователь уже существует в базе данных")
	else:
		try:
			await add_user(async_session, user_data, User)
		except Exception as e:
			print(e)


	while True:
		if "прекрасно" in message.text.lower() or "ожидать" in message.text.lower():
			await update_status(async_session, user_id, 'finishied', User)
			await message.reply("Прекрасно или ожидание обнаружены. Воронка прекращена.")
			users = await get_users(async_session, User)

		user = await get_user(async_session, user_data['id'], User)
		if user.status in ('finishied', 'dead'):
			print('Воронка прекращена')
			break

		try:
			if user.message1_sent_at is None:
				next_message_time = user.created_at + datetime.timedelta(seconds=6)
			elif user.message2_sent_at is None:
				next_message_time = user.message1_sent_at + datetime.timedelta(seconds=20)
			elif user.message3_sent_at is None:
				next_message_time = user.message2_sent_at + datetime.timedelta(minutes=1, seconds=2)
			else:
				# Все сообщения уже отправлены
				break

			if datetime.datetime.utcnow() >= next_message_time:
				if user.message1_sent_at is None:
					await client.send_message(user_id, "Текст 1")
					user.message1_sent_at = datetime.datetime.utcnow()
				elif user.message2_sent_at is None:
					await client.send_message(user_id, "Текст 2")
					user.message2_sent_at = datetime.datetime.utcnow()
				elif user.message3_sent_at is None:
					await client.send_message(user_id, "Текст 3")
					user.message3_sent_at = datetime.datetime.utcnow()
					await update_status(async_session, user_id, 'finishied', User)

				await update_user(async_session, user)

			await asyncio.sleep(1)

		except FloodWait as e:
			print(f"FloodWait: {e}")
			await asyncio.sleep(e.x)
		except UserBlocked as e:
			print(f"UserBlocked: {e}")
			await update_status(async_session, user_id, 'dead', User)
			break
		except UserDeactivated as e:
			print(f"UserDeactivated: {e}")
			await update_status(async_session, user_id, 'dead', User)
			break


async def main():
	await app.start()
	await idle()


if __name__ == "__main__":
	app.loop.run_until_complete(main())
