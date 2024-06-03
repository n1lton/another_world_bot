from sqlalchemy import create_engine, Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

DATABASE_NAME = 'data.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase): pass

    

class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True)
    type = Column(String)
    franchise_name = Column(Integer, ForeignKey('franchises.name', ondelete='CASCADE'))
    franchise = relationship('Franchise', back_populates='channels')


class Franchise(Base):
    __tablename__ = 'franchises'

    name = Column(String, primary_key=True)
    region = Column(String)
    channels = relationship('Channel', back_populates='franchise', cascade='all, delete', passive_deletes=True)
    users = relationship('User', back_populates='franchise', cascade='all, delete', passive_deletes=True)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    franchise_name = Column(String, ForeignKey('franchises.name', ondelete='CASCADE'))
    franchise = relationship('Franchise', back_populates='users')



Base.metadata.create_all(engine)
    
db = Session(bind=engine)