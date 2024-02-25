from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from asyncpgsa import create_pool
from sqlalchemy.future import select
import datetime

DATABASE_URL = "postgresql+asyncpg://postgres:1@localhost/voronkawebinar"

engine = create_engine(DATABASE_URL)
metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)


async def init_pg(app):
	app['db_pool'] = await create_pool(DATABASE_URL)


async def close_pg(app):
	await app['db_pool'].close()


# Функция для получения информации о пользователе из базы данных
async def get_user(async_session, user_id, User):
    async with async_session() as session:
        # Выполняем запрос к таблице users
        query = await session.execute(
            select(User).filter(User.id == user_id)
        )
        user = query.scalar()
        return user


async def update_status(async_session, user_id, new_status, User):
    async with async_session() as session:
        # Находим пользователя по его идентификатору
        user = await session.get(User, user_id)
        if user:
            # Обновляем статус пользователя
            user.status = new_status
            user.status_updated_at = datetime.datetime.utcnow()
            await session.commit()
            print(f"Статус пользователя с ID {user_id} успешно обновлен")
        else:
            print(f"Пользователь с ID {user_id} не найден в базе данных")



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


# Функция для проверки существования пользователя в базе данных
async def user_exists(async_session, id, User):
	async with async_session() as session:
		stmt = select(User)
		result = await session.execute(stmt)
		users = result.scalars().all()
		for user in users:
			if user.id == id:
				return True
		return False


# Метод взять id всех пользователей из базы, взять время срабатывания тригера (в минутах)
# записать все id в отдельный список


async def add_user(async_session, user_data, User):
	# Создаем новый объект пользователя на основе переданных данных
	new_user = User(**user_data)

	# Добавляем пользователя в базу данных
	async with async_session() as session:
		session.add(new_user)
		await session.commit()


# Функция для обновления информации о пользователе в базе данных
async def update_user(async_session, user):
    async with async_session() as session:
        # Обновляем информацию о пользователе
        session.add(user)
        await session.commit()