from models.Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Channel(Base):
    __tablename__ = 'channels'

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str]
    franchise_name: Mapped[int] = mapped_column(ForeignKey('franchises.name', ondelete='CASCADE'))
    franchise = relationship('Franchise', back_populates='channels')
    groups = relationship('Group', secondary='channels_groups', back_populates='channels')