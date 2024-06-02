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
    region = Column(String)
    franchise_name = relationship(Integer, ForeignKey('franchises.name', ondelete='CASCADE'))
    franchise = relationship('Franchise', back_populates='channels')


class Franchise(Base):
    __tablename__ = 'franchises'

    name = Column(String, primary_key=True)
    channels = relationship('Channel', back_populates='franchise', cascade='all, delete', passive_deletes=True)
    partners = relationship('Partner', back_populates='franchise', cascade='all, delete', passive_deletes=True)


class Partner(Base):
    __tablename__ = 'partners'

    id = Column(Integer, primary_key=True)
    franchise_name = Column(String, ForeignKey('franchises.name', ondelete='CASCADE'))
    franchise = relationship('Franchise', back_populates='partners')



Base.metadata.create_all(engine)
    
db = Session(bind=engine)