from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_
from typing import Optional, Dict, List, Union

from config import config

# Конфигурация PostgreSQL
DB_CONFIG = {
    "protocol": "postgresql+asyncpg", #postgresql+psycopg
    "user": config.postgres_user.get_secret_value(),
    "password": config.postgres_password.get_secret_value(),
    "host": config.postgres_host.get_secret_value(),
    "port": config.postgres_port.get_secret_value(),
    "db_name": config.postgres_db.get_secret_value()
}



# Настройка подключения к базе данных
protocol = DB_CONFIG["protocol"]
username = DB_CONFIG.get("user")  # 🔹 Логин от PostgreSQL
password = DB_CONFIG.get("password")  # 🔹 Пароль от PostgreSQL
server = DB_CONFIG.get("host")    # 🔹 Например, localhost или IP
port = DB_CONFIG.get("port")              # 🔹 Порт (по умолчанию 5432)
database = DB_CONFIG.get("db_name")  # 🔹 Название базы данных

connection_string = f"{protocol}://{username}:{password}@{server}:{port}/{database}"
print(connection_string)

# Создаем асинхронный движок
engine = create_async_engine(connection_string)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)


async def get_db():
    """Асинхронный генератор сессий"""
    async with AsyncSessionLocal() as session:
        yield session

class DataBase:
    @staticmethod
    async def add_to_db(obj):
        """Асинхронно добавляет объект в базу данных"""
        async with AsyncSessionLocal() as session:
            try:
                session.add(obj)
                await session.commit()
                await session.refresh(obj)
                return obj
            except Exception as e:
                await session.rollback()
                print(f"Error occurred: {e}")
                return None

    @staticmethod
    async def get_from_db(
            model_class,
            filters: Optional[Dict] = None,
            order_by: Optional[Union[str, List[str]]] = None,
            group_by: Optional[Union[str, List[str]]] = None,
            having: Optional[Dict] = None,
            limit: Optional[int] = None,
            join: Optional[Dict] = None,
            only_fields: Optional[List[str]] = None,
            distinct: bool = False,
            where_clauses: Optional[List] = None
    ):
        """Асинхронная версия универсального запроса"""
        async with AsyncSessionLocal() as session:
            try:
                # Базовый запрос
                stmt = select(model_class)

                # Фильтрация
                if filters:
                    stmt = stmt.filter_by(**filters)

                if where_clauses:
                    stmt = stmt.where(*where_clauses)

                # Сортировка
                if order_by:
                    if isinstance(order_by, str):
                        order_by = [order_by]

                    for field in order_by:
                        if field.startswith('-'):
                            stmt = stmt.order_by(getattr(model_class, field[1:]).desc())
                        else:
                            stmt = stmt.order_by(getattr(model_class, field))

                # Группировка
                if group_by:
                    if isinstance(group_by, str):
                        group_by = [group_by]

                    for field in group_by:
                        stmt = stmt.group_by(getattr(model_class, field))

                # HAVING условия
                if having:
                    having_conditions = []
                    for field, value in having.items():
                        having_conditions.append(getattr(model_class, field) == value)
                    stmt = stmt.having(and_(*having_conditions))

                # JOIN
                if join:
                    for join_model, condition in join.items():
                        stmt = stmt.join(join_model, condition)

                # Выбор конкретных полей
                if only_fields:
                    stmt = stmt.with_only_columns(
                        [getattr(model_class, field) for field in only_fields]
                    )

                # DISTINCT
                if distinct:
                    stmt = stmt.distinct()

                # Лимит
                if limit:
                    stmt = stmt.limit(limit)

                # Выполнение запроса
                result = await session.execute(stmt)
                return result.scalars().all()

            except Exception as e:
                print(f"Database error occurred: {e}")
                return None

    @staticmethod
    async def update_db(model_class, filters: dict, update_data: dict):
        """Асинхронное обновление записей"""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(model_class).filter_by(**filters)
                result = await session.execute(stmt)
                record = result.scalars().first()

                if record:
                    for key, value in update_data.items():
                        setattr(record, key, value)

                    await session.commit()
                    await session.refresh(record)
                    return record
                return None

            except Exception as e:
                await session.rollback()
                print(f"Error occurred: {e}")
                return None

    @staticmethod
    async def delete_from_db(model_class, filters: dict, delete_all: bool = False):
        """Асинхронно удаляет записи из базы данных по фильтрам."""
        async with AsyncSessionLocal() as session:
            try:
                stmt = select(model_class).filter_by(**filters)
                result = await session.execute(stmt)

                if delete_all:
                    # Удаляем все записи
                    records = result.scalars().all()
                    for record in records:
                        await session.delete(record)
                    await session.commit()
                    return len(records)
                else:
                    # Удаляем только первую запись
                    record = result.scalars().first()
                    if record:
                        await session.delete(record)
                        await session.commit()
                        return 1
                    return 0

            except Exception as e:
                await session.rollback()
                print(f"Error occurred in async delete_from_db: {e}")
                return 0
