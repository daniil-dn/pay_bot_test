from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(BigInteger, primary_key=True)
    username = Column(String, unique=True)
    balance = Column(Integer, unique=False, default=0)
    when = Column(DateTime, default=func.now())

    def __repr__(self):
        return 'id: {}, root username: {}, balance: {}'.format(self.id, self.username, self.balance)


class Black_list(Base):
    __tablename__ = 'black_list'
    id = Column(BigInteger, ForeignKey('user.id'), primary_key=True)
    when = Column(DateTime, default=func.now())
    user = relationship(User)

    def __repr__(self):
        return 'id: {}, time: {}'.format(self.id, self.when)
