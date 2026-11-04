from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


# Строка подключения для SQLite
DATABASE_URL = "sqlite:///ecommerce.db"

# Пример для PostgreSQL:
# DATABASE_URL = "postgresql+psycopg2://username:password@localhost:5432/dbname"

# Создаём Engine
engine = create_engine(DATABASE_URL, echo=True)

# Настраиваем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)

# Определяем базовый класс для моделей
class Base(DeclarativeBase):  # New
    pass
