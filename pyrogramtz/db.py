from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from asyncpgsa import create_pool
from sqlalchemy.future import select

DATABASE_URL = "postgresql+asyncpg://postgres:1@localhost/voronkawebinar"

engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)


async def init_pg(app):
	app['db_pool'] = await create_pool(DATABASE_URL)


async def close_pg(app):
	await app['db_pool'].close()


async def get_users(async_session, User):
	# Выполняем запрос к таблице users
	async with async_session() as session:
		# Выполняем запрос на выборку всех записей из таблицы users
		stmt = select(User)
		# Получаем результаты запроса
		result = await session.execute(stmt)
		# Получаем список пользователей
		users = result.scalars().all()

		# Выводим информацию о каждом пользователе
		for user in users:
			print(
				f"ID: {user.id}, Created At: {user.created_at}, Status: {user.status}, Status Updated At: {user.status_updated_at}")

		return users


async def add_user(async_session, user_data, User):
	# Создаем новый объект пользователя на основе переданных данных
	new_user = User(**user_data)

	# Добавляем пользователя в базу данных
	async with async_session() as session:
		session.add(new_user)
		await session.commit()
