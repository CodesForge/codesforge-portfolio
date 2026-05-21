from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, async_sessionmaker, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional

from src.common.logger import logger
from src.config.database_settings import DatabaseSettings

class DataBaseConfig:
    def __init__(self, settings: DatabaseSettings) -> None:
        self._async_engine: Optional[AsyncEngine] = None
        self._async_session: Optional[async_sessionmaker[AsyncSession]] = None
        self._settings = settings
    
    @property
    def async_engine(self) -> AsyncEngine:
        if self._async_engine is None:
            try:
                self._async_engine = create_async_engine(
                    url=self._settings.get_db_url
                )
                logger.info(
                    "AsyncEngine успешно инициализирован"
                )
            except SQLAlchemyError as e:
                logger.exception(
                    f"AsyncEngine sqlalchemy-error: {e}"
                )
                raise
            except Exception as e:
                logger.exception(
                    f"AsyncEngine ошибка инициализации: {e}"
                )
                raise
        return self._async_engine

    @property
    def async_session(self) -> async_sessionmaker[AsyncSession]:
        if self._async_session is None:
            try:
                self._async_session = async_sessionmaker(
                    bind=self._async_engine, expire_on_commit=False, class_=AsyncSession
                )
                logger.info(
                    "AsyncSession успешно инициализирован"
                )
            except SQLAlchemyError as e:
                logger.exception(
                    f"AsyncSession sqlalchemy-error: {e}"
                )
                raise
            except Exception as e:
                logger.exception(
                    f"AsyncSession ошибка инициализации: {e}"
                )
                raise
        return self._async_session

    async def connect(self) -> None:
        try:
            _ = self.async_engine
            logger.info(
                "Успешное подключение к базе данных"
            )
        except Exception as e:
            logger.exception(
                f"Ошибка подключения к базе данных: {e}"
            )
            raise
    
    async def disconnect(self) -> None:
        if self.async_engine is not None:
            try:
                await self.async_engine.dispose()
                self.async_engine = None
                self.async_session = None
                logger.info(
                    "Успешное отключение от базы данных"
                )
            except Exception as e:
                logger.exception(
                    f"Ошибка отключения от базы данных: {e}"
                )
                raise
