from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models import User
from src.schemas.schemas import UserCreate
from src.utils.password import get_password_hash

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Retrieve a user by email.

    Parameters:
    -----------
    db : AsyncSession
        Database session.
    email : str
        Email address to search for.

    Returns:
    --------
    User
        The user object if found, otherwise None.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()

async def create_user(db: AsyncSession, user: UserCreate):
    """
    Create a new user.

    Parameters:
    -----------
    db : AsyncSession
        Database session.
    user : UserCreate
        The user data.

    Returns:
    --------
    User
        The created user object.
    """
    hashed_password = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

