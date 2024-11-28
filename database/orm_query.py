from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database.models import Question


async def orm_add_question_pic(session: AsyncSession, data: dict):
    obj = Question(
        name = data["name"],
        description = data["description"],
        keywords = data["keywords"],
        image = data["image"]
    )
    session.add(obj)
    await session.commit()

async def orm_add_question(session: AsyncSession, data: dict):
    obj = Question(
        name = data["name"],
        description = data["description"],
        keywords = data["keywords"]
    )
    session.add(obj)
    await session.commit()

async def orm_get_questions(session: AsyncSession):
    query = select(Question)
    result = await session.execute(query)
    return result.scalars().all()


async def orm_get_question(session: AsyncSession, question_id: int):
    query = select(Question).where(Question.id == question_id)
    result = await session.execute(query)
    return result.scalar()


async def orm_update_question(session: AsyncSession, question_id: int, data):
    query = update(Question).where(Question.id == question_id).values(
        name=data["name"],
        description=data["description"],
        keywords=data["keywords"],
        image=data["image"],)
    await session.execute(query)
    await session.commit()


async def orm_delete_product(session: AsyncSession, question_id: int):
    query = delete(Question).where(Question.id == question_id)
    await session.execute(query)
    await session.commit()