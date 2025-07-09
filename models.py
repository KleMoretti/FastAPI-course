from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base


class Users(Base):
    __tablename__='users'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    email=Column(String(255), unique=True)
    username = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role= Column(String(50))
    phone_number = Column(String(255), nullable=True)

class Todos(Base):
    __tablename__ = 'todos'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255))
    description = Column(String(500))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer,ForeignKey('users.id'))
