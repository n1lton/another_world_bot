from models.Base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class UsersGroups(Base):
    __tablename__ = 'users_groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'))