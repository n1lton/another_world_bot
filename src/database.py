import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.Base import Base

DATABASE_NAME = 'data.db'

engine = create_engine(f'sqlite:///{DATABASE_NAME}')
Session = sessionmaker(bind=engine)


for i in os.listdir('models'):
    if i.endswith('.py') and i != 'Base.py':
        __import__('models.' + i.removesuffix('.py'))


Base.metadata.create_all(engine)
    
db = Session(bind=engine)