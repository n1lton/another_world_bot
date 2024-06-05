from models.Base import Base


from sqlalchemy.orm import Mapped, mapped_column, relationship


class Group(Base):
    __tablename__ = 'groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    channels = relationship('Channel', secondary='channels_groups', back_populates='groups')
    users = relationship('User', secondary='users_groups', back_populates='groups')