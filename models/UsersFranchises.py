from models.Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UsersFranchises(Base):
    __tablename__ = 'users_franchises'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    franchise_name: Mapped[str] = mapped_column(ForeignKey('franchises.name', ondelete='CASCADE'))