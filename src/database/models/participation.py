from sqlalchemy import Boolean, Double, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class GamePlayer(Base):
    __tablename__ = "game_player"

    game_id: Mapped[str] = mapped_column(
        ForeignKey("game.game_id"), primary_key=True
    )
    player_id: Mapped[str] = mapped_column(
        ForeignKey("player.player_id"), primary_key=True
    )
    team_id: Mapped[str | None] = mapped_column(
        ForeignKey("team.team_id")
    )
    car_id: Mapped[str | None] = mapped_column(
        ForeignKey("car.car_id")
    )
    color: Mapped[str | None] = mapped_column(String)
    winner: Mapped[bool | None] = mapped_column(Boolean)
    platform: Mapped[str | None] = mapped_column(String)
    platform_id: Mapped[str | None] = mapped_column(String)
    steering_sensitivity: Mapped[float | None] = mapped_column(Double)
    camera_fov: Mapped[float | None] = mapped_column(Double)
    camera_height: Mapped[float | None] = mapped_column(Double)
    camera_pitch: Mapped[float | None] = mapped_column(Double)
    camera_distance: Mapped[float | None] = mapped_column(Double)
    camera_stiffness: Mapped[float | None] = mapped_column(Double)
    camera_swivel_speed: Mapped[float | None] = mapped_column(Double)
    camera_transition_speed: Mapped[float | None] = mapped_column(Double)

    game: Mapped["Game"] = relationship(back_populates="game_players")
    player: Mapped["Player"] = relationship(back_populates="game_players")
    team: Mapped["Team"] = relationship(back_populates="game_players")
    car: Mapped["Car"] = relationship(back_populates="game_players")


class GameTeam(Base):
    __tablename__ = "game_team"

    game_id: Mapped[str] = mapped_column(
        ForeignKey("game.game_id"), primary_key=True
    )
    team_id: Mapped[str] = mapped_column(
        ForeignKey("team.team_id"), primary_key=True
    )
    color: Mapped[str | None] = mapped_column(String)
    winner: Mapped[bool | None] = mapped_column(Boolean)
    core_goals: Mapped[int | None] = mapped_column(Integer)

    game: Mapped["Game"] = relationship(back_populates="game_teams")
    team: Mapped["Team"] = relationship(back_populates="game_teams")
