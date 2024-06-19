from models.Base import Base


from sqlalchemy.orm import Mapped, mapped_column, relationship


class Franchise(Base):
    __tablename__ = 'franchises'

    name: Mapped[str] = mapped_column(primary_key=True)
    channels = relationship('Channel', back_populates='franchise', cascade='save-update, delete', passive_deletes=True)
    users = relationship('User', secondary='users_franchises', back_populates='franchises')