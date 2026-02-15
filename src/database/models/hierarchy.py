from sqlalchemy import Boolean, Double, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class Event(Base):
    __tablename__ = "event"

    event_id: Mapped[str] = mapped_column(String, primary_key=True)
    event_name: Mapped[str | None] = mapped_column(String)
    event_split: Mapped[str | None] = mapped_column(String)
    event_slug: Mapped[str | None] = mapped_column(String)
    event_start_date: Mapped[str | None] = mapped_column(String)
    event_end_date: Mapped[str | None] = mapped_column(String)
    event_tier: Mapped[str | None] = mapped_column(String)
    event_phase: Mapped[str | None] = mapped_column(String)
    prize_money: Mapped[float | None] = mapped_column(Double)
    region_id: Mapped[str | None] = mapped_column(
        ForeignKey("region.region_id")
    )

    region: Mapped["Region"] = relationship(back_populates="events")
    stages: Mapped[list["Stage"]] = relationship(back_populates="event")


class Stage(Base):
    __tablename__ = "stage"

    stage_id: Mapped[str] = mapped_column(String, primary_key=True)
    event_id: Mapped[str | None] = mapped_column(
        ForeignKey("event.event_id")
    )
    stage_name: Mapped[str | None] = mapped_column(String)
    stage_step: Mapped[int | None] = mapped_column(Integer)
    stage_start_date: Mapped[str | None] = mapped_column(String)
    stage_end_date: Mapped[str | None] = mapped_column(String)
    is_lan: Mapped[bool | None] = mapped_column(Boolean)
    is_qualifier: Mapped[bool | None] = mapped_column(Boolean)
    location_venue: Mapped[str | None] = mapped_column(String)
    location_city: Mapped[str | None] = mapped_column(String)
    location_country: Mapped[str | None] = mapped_column(String)

    event: Mapped["Event"] = relationship(back_populates="stages")
    matches: Mapped[list["Match"]] = relationship(back_populates="stage")


class Match(Base):
    __tablename__ = "match"

    match_id: Mapped[str] = mapped_column(String, primary_key=True)
    stage_id: Mapped[str | None] = mapped_column(
        ForeignKey("stage.stage_id")
    )
    match_slug: Mapped[str | None] = mapped_column(String)
    match_number: Mapped[int | None] = mapped_column(Integer)
    match_round: Mapped[str | None] = mapped_column(String)
    match_date: Mapped[str | None] = mapped_column(String)
    match_format: Mapped[str | None] = mapped_column(String)
    reverse_sweep_attempt: Mapped[bool | None] = mapped_column(Boolean)
    reverse_sweep: Mapped[bool | None] = mapped_column(Boolean)

    stage: Mapped["Stage"] = relationship(back_populates="matches")
    games: Mapped[list["Game"]] = relationship(back_populates="match")


class Game(Base):
    __tablename__ = "game"

    game_id: Mapped[str] = mapped_column(String, primary_key=True)
    match_id: Mapped[str | None] = mapped_column(
        ForeignKey("match.match_id")
    )
    map_id: Mapped[str | None] = mapped_column(
        ForeignKey("map.map_id")
    )
    game_number: Mapped[int | None] = mapped_column(Integer)
    game_date: Mapped[str | None] = mapped_column(String)
    game_duration: Mapped[float | None] = mapped_column(Double)
    overtime: Mapped[bool | None] = mapped_column(Boolean)
    ballchasing_id: Mapped[str | None] = mapped_column(String)

    match: Mapped["Match"] = relationship(back_populates="games")
    map: Mapped["Map"] = relationship(back_populates="games")
    game_players: Mapped[list["GamePlayer"]] = relationship(
        back_populates="game"
    )
    game_teams: Mapped[list["GameTeam"]] = relationship(
        back_populates="game"
    )
    stats: Mapped[list["Stat"]] = relationship(back_populates="game")
