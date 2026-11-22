from decouple import config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession


#  --------------- Синхронное подключение к SQLite -------------------------

# Строка подключения для SQLite
# DATABASE_URL = "sqlite:///ecommerce.db"
DATABASE_URL = config("DATABASE_URL")

# Пример для PostgreSQL:
# DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/dbname"

# Создаём Engine
engine = create_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)


#  --------------- Асинхронное подключение к PostgreSQL -------------------------


# Строка подключения для PostgreSQL
# DATABASE_URL_PG = "postgresql+asyncpg://ecommerce_user:12345@localhost:5432/ecommerce_db"
DATABASE_URL_PG = config("DATABASE_URL_PG")

# Создаём Engine
async_engine = create_async_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

# Определяем базовый класс для моделей
class Base(DeclarativeBase):  # New
    pass
