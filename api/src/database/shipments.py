from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from settings import database_host,database_name,database_password,database_username

class DatabaseShipments:

    database_url = f'postgresql+asyncpg://{database_username}:{database_password}@{database_host}/{database_name}'
    session = None

    @classmethod
    async def connect(cls):
        try:
            engine = create_async_engine(cls.database_url)
            async with engine.connect() as connection:
                cls.session = AsyncSession(bind=engine,expire_on_commit=False)
                print('Connection established with the database')
        except Exception as e:
            raise e

    @classmethod
    async def disconnect(cls):
        try:
            await cls.session.close()
            print('Connection closed with the database')
        except Exception as e:
            raise e