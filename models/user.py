from sqlalchemy import Column, Integer, String
from models.base import TimeStampedModel


class User(TimeStampedModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    furnace = Column(String(4), nullable=False)
    state = Column(Integer, nullable=False)


    def __repr__(self):
        return f"{self.id}, {self.username}, {self.furnace}, {self.state}"