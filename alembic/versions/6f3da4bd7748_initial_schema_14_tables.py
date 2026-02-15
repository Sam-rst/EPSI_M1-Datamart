"""initial schema 14 tables

Revision ID: 6f3da4bd7748
Revises:
Create Date: 2026-02-15 15:34:17.611893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f3da4bd7748'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Référentiels ──
    op.create_table(
        "country",
        sa.Column("country_id", sa.String(), primary_key=True),
        sa.Column("country_name", sa.String(), nullable=True),
    )
    op.create_table(
        "region",
        sa.Column("region_id", sa.String(), primary_key=True),
        sa.Column("region_name", sa.String(), nullable=True),
    )
    op.create_table(
        "map",
        sa.Column("map_id", sa.String(), primary_key=True),
        sa.Column("map_name", sa.String(), nullable=True),
    )
    op.create_table(
        "car",
        sa.Column("car_id", sa.String(), primary_key=True),
        sa.Column("car_name", sa.String(), nullable=True),
    )

    # ── Entités principales ──
    op.create_table(
        "player",
        sa.Column("player_id", sa.String(), primary_key=True),
        sa.Column("player_tag", sa.String(), nullable=True),
        sa.Column("player_name", sa.String(), nullable=True),
        sa.Column("country_id", sa.String(), sa.ForeignKey("country.country_id"), nullable=True),
    )
    op.create_table(
        "team",
        sa.Column("team_id", sa.String(), primary_key=True),
        sa.Column("team_name", sa.String(), nullable=True),
        sa.Column("region_id", sa.String(), sa.ForeignKey("region.region_id"), nullable=True),
    )

    # ── Hiérarchie Event → Stage → Match → Game ──
    op.create_table(
        "event",
        sa.Column("event_id", sa.String(), primary_key=True),
        sa.Column("event_name", sa.String(), nullable=True),
        sa.Column("event_split", sa.String(), nullable=True),
        sa.Column("event_slug", sa.String(), nullable=True),
        sa.Column("event_start_date", sa.String(), nullable=True),
        sa.Column("event_end_date", sa.String(), nullable=True),
        sa.Column("event_tier", sa.String(), nullable=True),
        sa.Column("event_phase", sa.String(), nullable=True),
        sa.Column("prize_money", sa.Double(), nullable=True),
        sa.Column("region_id", sa.String(), sa.ForeignKey("region.region_id"), nullable=True),
    )
    op.create_table(
        "stage",
        sa.Column("stage_id", sa.String(), primary_key=True),
        sa.Column("event_id", sa.String(), sa.ForeignKey("event.event_id"), nullable=True),
        sa.Column("stage_name", sa.String(), nullable=True),
        sa.Column("stage_step", sa.Integer(), nullable=True),
        sa.Column("stage_start_date", sa.String(), nullable=True),
        sa.Column("stage_end_date", sa.String(), nullable=True),
        sa.Column("is_lan", sa.Boolean(), nullable=True),
        sa.Column("is_qualifier", sa.Boolean(), nullable=True),
        sa.Column("location_venue", sa.String(), nullable=True),
        sa.Column("location_city", sa.String(), nullable=True),
        sa.Column("location_country", sa.String(), nullable=True),
    )
    op.create_table(
        "match",
        sa.Column("match_id", sa.String(), primary_key=True),
        sa.Column("stage_id", sa.String(), sa.ForeignKey("stage.stage_id"), nullable=True),
        sa.Column("match_slug", sa.String(), nullable=True),
        sa.Column("match_number", sa.Integer(), nullable=True),
        sa.Column("match_round", sa.String(), nullable=True),
        sa.Column("match_date", sa.String(), nullable=True),
        sa.Column("match_format", sa.String(), nullable=True),
        sa.Column("reverse_sweep_attempt", sa.Boolean(), nullable=True),
        sa.Column("reverse_sweep", sa.Boolean(), nullable=True),
    )
    op.create_table(
        "game",
        sa.Column("game_id", sa.String(), primary_key=True),
        sa.Column("match_id", sa.String(), sa.ForeignKey("match.match_id"), nullable=True),
        sa.Column("map_id", sa.String(), sa.ForeignKey("map.map_id"), nullable=True),
        sa.Column("game_number", sa.Integer(), nullable=True),
        sa.Column("game_date", sa.String(), nullable=True),
        sa.Column("game_duration", sa.Double(), nullable=True),
        sa.Column("overtime", sa.Boolean(), nullable=True),
        sa.Column("ballchasing_id", sa.String(), nullable=True),
    )

    # ── Participation ──
    op.create_table(
        "game_player",
        sa.Column("game_id", sa.String(), sa.ForeignKey("game.game_id"), primary_key=True),
        sa.Column("player_id", sa.String(), sa.ForeignKey("player.player_id"), primary_key=True),
        sa.Column("team_id", sa.String(), sa.ForeignKey("team.team_id"), nullable=True),
        sa.Column("car_id", sa.String(), sa.ForeignKey("car.car_id"), nullable=True),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column("winner", sa.Boolean(), nullable=True),
        sa.Column("platform", sa.String(), nullable=True),
        sa.Column("platform_id", sa.String(), nullable=True),
        sa.Column("steering_sensitivity", sa.Double(), nullable=True),
        sa.Column("camera_fov", sa.Double(), nullable=True),
        sa.Column("camera_height", sa.Double(), nullable=True),
        sa.Column("camera_pitch", sa.Double(), nullable=True),
        sa.Column("camera_distance", sa.Double(), nullable=True),
        sa.Column("camera_stiffness", sa.Double(), nullable=True),
        sa.Column("camera_swivel_speed", sa.Double(), nullable=True),
        sa.Column("camera_transition_speed", sa.Double(), nullable=True),
    )
    op.create_table(
        "game_team",
        sa.Column("game_id", sa.String(), sa.ForeignKey("game.game_id"), primary_key=True),
        sa.Column("team_id", sa.String(), sa.ForeignKey("team.team_id"), primary_key=True),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column("winner", sa.Boolean(), nullable=True),
        sa.Column("core_goals", sa.Integer(), nullable=True),
    )

    # ── Stats polymorphiques (EAV) ──
    op.create_table(
        "stat_type",
        sa.Column("type_id", sa.String(), primary_key=True),
        sa.Column("stat_name", sa.String(), unique=True, nullable=False),
        sa.Column("category", sa.String(), nullable=False),
    )
    op.create_table(
        "stat",
        sa.Column("stat_id", sa.String(), primary_key=True),
        sa.Column("entity_id", sa.String(), nullable=False),
        sa.Column("entity_type", sa.String(), nullable=False),
        sa.Column("game_id", sa.String(), sa.ForeignKey("game.game_id"), nullable=False),
        sa.Column("type_id", sa.String(), sa.ForeignKey("stat_type.type_id"), nullable=False),
        sa.Column("value", sa.Double(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("stat")
    op.drop_table("stat_type")
    op.drop_table("game_team")
    op.drop_table("game_player")
    op.drop_table("game")
    op.drop_table("match")
    op.drop_table("stage")
    op.drop_table("event")
    op.drop_table("team")
    op.drop_table("player")
    op.drop_table("car")
    op.drop_table("map")
    op.drop_table("region")
    op.drop_table("country")
