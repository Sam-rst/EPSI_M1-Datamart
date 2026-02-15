from sqlalchemy import Double, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.models.base import Base


class StatType(Base):
    __tablename__ = "stat_type"

    type_id: Mapped[str] = mapped_column(String, primary_key=True)
    stat_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)

    stats: Mapped[list["Stat"]] = relationship(back_populates="stat_type")


class Stat(Base):
    """Table polymorphique EAV — granularité : 1 stat × 1 entité × 1 game.

    entity_type = 'player' → entity_id pointe vers Player
    entity_type = 'team'   → entity_id pointe vers Team
    """

    __tablename__ = "stat"

    stat_id: Mapped[str] = mapped_column(String, primary_key=True)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    game_id: Mapped[str] = mapped_column(
        ForeignKey("game.game_id"), nullable=False
    )
    type_id: Mapped[str] = mapped_column(
        ForeignKey("stat_type.type_id"), nullable=False
    )
    value: Mapped[float] = mapped_column(Double, nullable=False)

    game: Mapped["Game"] = relationship(back_populates="stats")
    stat_type: Mapped["StatType"] = relationship(back_populates="stats")
