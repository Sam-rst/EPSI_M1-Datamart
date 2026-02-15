from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class Country(Base):
    __tablename__ = "country"

    country_id: Mapped[str] = mapped_column(String, primary_key=True)
    country_name: Mapped[str | None] = mapped_column(String)

    players: Mapped[list["Player"]] = relationship(back_populates="country")


class Region(Base):
    __tablename__ = "region"

    region_id: Mapped[str] = mapped_column(String, primary_key=True)
    region_name: Mapped[str | None] = mapped_column(String)

    teams: Mapped[list["Team"]] = relationship(back_populates="region")
    events: Mapped[list["Event"]] = relationship(back_populates="region")


class Map(Base):
    __tablename__ = "map"

    map_id: Mapped[str] = mapped_column(String, primary_key=True)
    map_name: Mapped[str | None] = mapped_column(String)

    games: Mapped[list["Game"]] = relationship(back_populates="map")


class Car(Base):
    __tablename__ = "car"

    car_id: Mapped[str] = mapped_column(String, primary_key=True)
    car_name: Mapped[str | None] = mapped_column(String)

    game_players: Mapped[list["GamePlayer"]] = relationship(back_populates="car")
