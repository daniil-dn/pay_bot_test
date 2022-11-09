from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    balance = Column(Integer, unique=False, default=0)
    when = Column(DateTime, default=func.now())

    def __repr__(self):
        return 'id: {}, root cause: {}'.format(self.id, self.root_cause)


class Black_list(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('user.id'), index=True)
    when = Column(DateTime, default=func.now())
    user = relationship(User)

    def __repr__(self):
        return 'id: {}, root cause: {}'.format(self.id, self.root_cause)
