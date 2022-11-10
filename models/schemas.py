from sqlalchemy import Column, DateTime, String, Integer, func, ForeignKey, BigInteger, BOOLEAN
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


class BlackList(Base):
    __tablename__ = 'black_list'
    id = Column(BigInteger, ForeignKey('user.id'), primary_key=True)
    when = Column(DateTime, default=func.now())
    user = relationship(User)

    def __repr__(self):
        return 'id: {}, time: {}'.format(self.id, self.when)


class Bill(Base):
    __tablename__ = 'bill'
    id = Column(BigInteger, ForeignKey('user.id'), primary_key=True)
    billID = Column(BigInteger, index=True)
    amount = Column(Integer, unique=False)
    isSended = Column(BOOLEAN, unique=False, default=False)
    when = Column(DateTime, default=func.now())
    user = relationship(User)

    def __repr__(self):
        return 'UserID: {}, billID: {}, amount: {}, isSended: {}, time: {}'.format(self.id, self.billID, self.amount,
                                                                                   self.isSended, self.when)
