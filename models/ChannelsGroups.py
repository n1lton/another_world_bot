from models.Base import Base


from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ChannelsGroups(Base):
    __tablename__ = 'channels_groups'

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey('channels.id', ondelete='CASCADE'))
    group_id: Mapped[int] = mapped_column(ForeignKey('groups.id', ondelete='CASCADE'))