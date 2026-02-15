from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class Player(Base):
    __tablename__ = "player"

    player_id: Mapped[str] = mapped_column(String, primary_key=True)
    player_tag: Mapped[str | None] = mapped_column(String)
    player_name: Mapped[str | None] = mapped_column(String)
    country_id: Mapped[str | None] = mapped_column(
        ForeignKey("country.country_id")
    )

    country: Mapped["Country"] = relationship(back_populates="players")
    game_players: Mapped[list["GamePlayer"]] = relationship(
        back_populates="player"
    )


class Team(Base):
    __tablename__ = "team"

    team_id: Mapped[str] = mapped_column(String, primary_key=True)
    team_name: Mapped[str | None] = mapped_column(String)
    region_id: Mapped[str | None] = mapped_column(
        ForeignKey("region.region_id")
    )

    region: Mapped["Region"] = relationship(back_populates="teams")
    game_players: Mapped[list["GamePlayer"]] = relationship(
        back_populates="team"
    )
    game_teams: Mapped[list["GameTeam"]] = relationship(
        back_populates="team"
    )
