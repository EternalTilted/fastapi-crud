from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from schemas import User, UserCreate, UserUpdate
from models import User
from sqlalchemy import select


async def get_user(db: AsyncSession, user_id: int):
    user = await db.execute(select(User).filter(User.id == user_id))
    return user.scalars().first()


async def get_users(db: AsyncSession):
    users = await db.execute(select(User))
    return users.scalars().all()


async def create_user(db: AsyncSession, user: UserCreate):
    db_user = User(first_name=user.first_name, last_name=user.last_name, email=user.email)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user(db: AsyncSession, user: UserUpdate):
    db_user = await get_user(db, user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    await db.commit()


async def delete_user(db: AsyncSession, id: int):
    db_user = await get_user(db, id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(db_user)
    await db.commit()
