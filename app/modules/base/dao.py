from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func, exists as sqlalchemy_exists

from loguru import logger

from typing import Any, List


class BaseDAO:
    model = None  # Устанавливается в дочернем классе

    @classmethod
    async def find_one_or_none_by_id(cls, session: AsyncSession, data_id: int):
        # Найти запись по ID
        logger.info(f"Поиск {cls.model.__name__} с ID: {data_id}")
        try:
            query = select(cls.model).filter_by(id=data_id)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись с ID {data_id} найдена.")
            else:
                logger.info(f"Запись с ID {data_id} не найдена.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {data_id}: {e}")
            raise

    @classmethod
    async def find_one_or_none(cls, session: AsyncSession, **filter_by):
        # Найти одну запись по фильтрам
        logger.info(f"Поиск одной записи {cls.model.__name__} по фильтрам: {filter_by}")
        try:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись найдена по фильтрам: {filter_by}")
            else:
                logger.info(f"Запись не найдена по фильтрам: {filter_by}")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи по фильтрам {filter_by}: {e}")
            raise

    @classmethod
    async def find_all(cls, session: AsyncSession, **filter_by):
        # Найти все записи по фильтрам
        filter_by = {k: v for k, v in filter_by.items() if v is not None}
        logger.info(f"Поиск всех записей {cls.model.__name__} по фильтрам: {filter_by}")
        try:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске всех записей по фильтрам {filter_by}: {e}")
            raise

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.flush()
        except IntegrityError:
            raise
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: list[dict]):
        # Добавить несколько записей
        logger.info(f"Добавление нескольких записей {cls.model.__name__}. Количество: {len(instances)}")
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.flush()
            logger.info(f"Успешно добавлено {len(new_instances)} записей.")
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при добавлении нескольких записей: {e}")
            raise e
        return new_instances            

    @classmethod
    async def update(cls, session: AsyncSession, filter_by, **values):
        # Обновить записи по фильтру
        logger.info(f"Обновление записей {cls.model.__name__} по фильтру: {filter_by} с параметрами: {values}")
        query = (
            sqlalchemy_update(cls.model)
            .where(*[getattr(cls.model, k) == v for k, v in filter_by.items()])
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Обновлено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при обновлении записей: {e}")
            raise e
            
    @classmethod
    async def upsert(cls, session: AsyncSession, unique_fields: List[str], **values):
        """Создать запись или обновить существующую"""
        filter_dict = {field: values[field] for field in unique_fields if field in values}

        logger.info(f"Upsert для {cls.model.__name__}")
        try:
            existing = await cls.find_one_or_none(session, **filter_dict)
            if existing:
                # Обновляем существующую запись
                for key, value in values.items():
                    setattr(existing, key, value)
                await session.flush()
                logger.info(f"Обновлена существующая запись {cls.model.__name__}")
                return "existed"
            else:
                # Создаем новую запись
                new_instance = cls.model(**values)
                session.add(new_instance)
                await session.flush()
                logger.info(f"Создана новая запись {cls.model.__name__}")
                return "new"
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при upsert: {e}")
            raise

    @classmethod
    async def delete(cls, session: AsyncSession, **filter_by):
        # Удалить записи по фильтру
        logger.info(f"Удаление записей {cls.model.__name__} по фильтру: {filter_by}")
        if not filter_by:
            logger.error("Нужен хотя бы один фильтр для удаления.")
            raise ValueError("Нужен хотя бы один фильтр для удаления.")

        query = sqlalchemy_delete(cls.model).filter_by(**filter_by)
        try:
            result = await session.execute(query)
            await session.flush()
            logger.info(f"Удалено {result.rowcount} записей.")
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            logger.error(f"Ошибка при удалении записей: {e}")
            raise e

    @classmethod
    async def count(cls, session: AsyncSession, **filter_by):
        # Подсчитать количество записей
        logger.info(f"Подсчет количества записей {cls.model.__name__} по фильтру: {filter_by}")
        try:
            query = select(func.count(cls.model.id)).filter_by(**filter_by)
            result = await session.execute(query)
            count = result.scalar()
            logger.info(f"Найдено {count} записей.")
            return count
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при подсчете записей: {e}")
            raise

    @classmethod
    async def exists(cls, session: AsyncSession, **filter_by) -> bool:
        stmt = select(sqlalchemy_exists(select(1).select_from(cls.model).filter_by(**filter_by)))
        res = await session.execute(stmt)
        return bool(res.scalar())
    

    @classmethod
    async def paginate(cls, session: AsyncSession, page: int = 1, page_size: int = 10, **filter_by):
        # Пагинация записей
        logger.info(
            f"Пагинация записей {cls.model.__name__} по фильтру: {filter_by}, страница: {page}, размер страницы: {page_size}")
        try:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query.offset((page - 1) * page_size).limit(page_size))
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей на странице {page}.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при пагинации записей: {e}")
            raise


    @classmethod
    async def find_by_ids(cls, session: AsyncSession, ids: List[int]) -> List[Any]:
        """Найти несколько записей по списку ID"""
        logger.info(f"Поиск записей {cls.model.__name__} по списку ID: {ids}")
        try:
            query = select(cls.model).filter(cls.model.id.in_(ids))
            result = await session.execute(query)
            records = result.scalars().all()
            logger.info(f"Найдено {len(records)} записей по списку ID.")
            return records
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записей по списку ID: {e}")
            raise