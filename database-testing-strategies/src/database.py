"""Database tables definition."""

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Character(Base):
    """The table that represents a character."""

    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    origin = Column(String, nullable=False)
