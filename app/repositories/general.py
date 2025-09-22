from abc import ABC, abstractmethod

from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.repositories.exceptions import EntityAlreadyExistError


class AbstractRepository(ABC):
    @abstractmethod
    async def add():
        raise NotImplementedError

    @abstractmethod
    async def get_by_id():
        raise NotImplementedError

    @abstractmethod
    async def update_by_id():
        raise NotImplementedError

    @abstractmethod
    async def delete():
        raise NotImplementedError


class GeneralRepository(AbstractRepository):
    def __init__(self, session: async_sessionmaker):
        self.session = session

    model = None

    async def add(self, **kwargs):
        object = self.model(**kwargs)
        self.session.add(object)
        try:
            await self.session.commit()
            self.session.refresh(object)
            return object
        except IntegrityError:
            raise EntityAlreadyExistError(
                (
                    "Запись с данными уже существует или"
                    f"отсутствуют необходимые поля, {kwargs}"
                )
            )

    async def get_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(self, model_id: int):
        result = await self.session.execute(
            select(self.model).where(self.model.id == model_id)
        )
        return result.scalars().first()

    async def update_by_id(self, model_id: int, **data):
        instance = await self.get_by_id(model_id=model_id)

        if not instance:
            return None

        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)

        return instance

    async def delete(self, model_id: int):
        await self.session.execute(
            delete(self.model).where(self.model.id == model_id)
        )
        await self.session.commit()
