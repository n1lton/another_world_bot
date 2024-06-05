from models.Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    franchises = relationship('Franchise', secondary='users_franchises', back_populates='users')
    groups = relationship('Group', secondary='users_groups', back_populates='users')