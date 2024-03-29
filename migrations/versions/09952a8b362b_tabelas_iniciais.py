"""Tabelas iniciais

Revision ID: 09952a8b362b
Revises:
Create Date: 2022-05-23 15:55:59.490222

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "09952a8b362b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "auth_role",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("permissions", sa.UnicodeText(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("name"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "auth_user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("username", sa.String(length=14), nullable=True),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("last_login_at", sa.DateTime(), nullable=True),
        sa.Column("current_login_at", sa.DateTime(), nullable=True),
        sa.Column("last_login_ip", sa.String(length=100), nullable=True),
        sa.Column("current_login_ip", sa.String(length=100), nullable=True),
        sa.Column("login_count", sa.Integer(), nullable=True),
        sa.Column("fs_uniquifier", sa.String(length=255), nullable=False),
        sa.Column("confirmed_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("fs_uniquifier"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("username"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "champion",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "team",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("tag", sa.String(), nullable=True),
        sa.Column("flag", sa.String(), nullable=True),
        sa.Column("phase", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "auth_role_user",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ("role_id",),
            ["auth_role.id"],
        ),
        sa.ForeignKeyConstraint(
            ("user_id",),
            ["auth_user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "player",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("nickname", sa.String(), nullable=True),
        sa.Column("team_id", sa.Integer(), nullable=True),
        sa.Column("flag", sa.String(), nullable=True),
        sa.Column(
            "role", sa.Enum("baron", "jungle", "mid", "dragon", "sup", name="role"), nullable=True
        ),
        sa.ForeignKeyConstraint(
            ("team_id",),
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "matchup",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("phase", sa.String(), nullable=True),
        sa.Column("datetime", sa.DateTime(), nullable=True),
        sa.Column("mvp_id", sa.Integer(), nullable=True),
        sa.Column("team1_id", sa.Integer(), nullable=True),
        sa.Column("team2_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ("mvp_id",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("team1_id",),
            ["team.id"],
        ),
        sa.ForeignKeyConstraint(
            ("team2_id",),
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    op.create_table(
        "matchup_map",
        sa.Column("uuid", postgresql.UUID(), nullable=True, default=sa.func.uuid_generate_v4()),
        sa.Column("date_created", sa.DateTime(), nullable=True, default=sa.func.now()),
        sa.Column("date_modified", sa.DateTime(), nullable=True),
        sa.Column("extra", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=False, default=True),
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("matchup_id", sa.Integer(), nullable=True),
        sa.Column("map_number", sa.Integer(), nullable=True),
        sa.Column("blue_side", sa.Integer(), nullable=True),
        sa.Column("red_side", sa.Integer(), nullable=True),
        sa.Column("length", sa.String(), nullable=True),
        sa.Column("winner", sa.Integer(), nullable=True),
        sa.Column("winner_side", sa.String(), nullable=True),
        sa.Column("blue_ban_1", sa.Integer(), nullable=True),
        sa.Column("red_ban_1", sa.Integer(), nullable=True),
        sa.Column("blue_ban_2", sa.Integer(), nullable=True),
        sa.Column("red_ban_2", sa.Integer(), nullable=True),
        sa.Column("blue_ban_3", sa.Integer(), nullable=True),
        sa.Column("red_ban_3", sa.Integer(), nullable=True),
        sa.Column("blue_pick_1", sa.Integer(), nullable=True),
        sa.Column("red_pick_1", sa.Integer(), nullable=True),
        sa.Column("red_pick_2", sa.Integer(), nullable=True),
        sa.Column("blue_pick_2", sa.Integer(), nullable=True),
        sa.Column("blue_pick_3", sa.Integer(), nullable=True),
        sa.Column("red_pick_3", sa.Integer(), nullable=True),
        sa.Column("blue_ban_4", sa.Integer(), nullable=True),
        sa.Column("red_ban_4", sa.Integer(), nullable=True),
        sa.Column("blue_ban_5", sa.Integer(), nullable=True),
        sa.Column("red_ban_5", sa.Integer(), nullable=True),
        sa.Column("red_pick_4", sa.Integer(), nullable=True),
        sa.Column("blue_pick_4", sa.Integer(), nullable=True),
        sa.Column("blue_pick_5", sa.Integer(), nullable=True),
        sa.Column("red_pick_5", sa.Integer(), nullable=True),
        sa.Column("blue_baron_pick", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_pick", sa.Integer(), nullable=True),
        sa.Column("blue_mid_pick", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_pick", sa.Integer(), nullable=True),
        sa.Column("blue_sup_pick", sa.Integer(), nullable=True),
        sa.Column("red_baron_pick", sa.Integer(), nullable=True),
        sa.Column("red_jungle_pick", sa.Integer(), nullable=True),
        sa.Column("red_mid_pick", sa.Integer(), nullable=True),
        sa.Column("red_dragon_pick", sa.Integer(), nullable=True),
        sa.Column("red_sup_pick", sa.Integer(), nullable=True),
        sa.Column("blue_baron_player", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_player", sa.Integer(), nullable=True),
        sa.Column("blue_mid_player", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_player", sa.Integer(), nullable=True),
        sa.Column("blue_sup_player", sa.Integer(), nullable=True),
        sa.Column("red_baron_player", sa.Integer(), nullable=True),
        sa.Column("red_mid_player", sa.Integer(), nullable=True),
        sa.Column("red_jungle_player", sa.Integer(), nullable=True),
        sa.Column("red_dragon_player", sa.Integer(), nullable=True),
        sa.Column("red_sup_player", sa.Integer(), nullable=True),
        sa.Column("blue_baron_kills", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_kills", sa.Integer(), nullable=True),
        sa.Column("blue_mid_kills", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_kills", sa.Integer(), nullable=True),
        sa.Column("blue_sup_kills", sa.Integer(), nullable=True),
        sa.Column("red_baron_kills", sa.Integer(), nullable=True),
        sa.Column("red_jungle_kills", sa.Integer(), nullable=True),
        sa.Column("red_mid_kills", sa.Integer(), nullable=True),
        sa.Column("red_dragon_kills", sa.Integer(), nullable=True),
        sa.Column("red_sup_kills", sa.Integer(), nullable=True),
        sa.Column("blue_baron_deaths", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_deaths", sa.Integer(), nullable=True),
        sa.Column("blue_mid_deaths", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_deaths", sa.Integer(), nullable=True),
        sa.Column("blue_sup_deaths", sa.Integer(), nullable=True),
        sa.Column("red_baron_deaths", sa.Integer(), nullable=True),
        sa.Column("red_jungle_deaths", sa.Integer(), nullable=True),
        sa.Column("red_mid_deaths", sa.Integer(), nullable=True),
        sa.Column("red_dragon_deaths", sa.Integer(), nullable=True),
        sa.Column("red_sup_deaths", sa.Integer(), nullable=True),
        sa.Column("blue_baron_assists", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_assists", sa.Integer(), nullable=True),
        sa.Column("blue_mid_assists", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_assists", sa.Integer(), nullable=True),
        sa.Column("blue_sup_assists", sa.Integer(), nullable=True),
        sa.Column("red_baron_assists", sa.Integer(), nullable=True),
        sa.Column("red_jungle_assists", sa.Integer(), nullable=True),
        sa.Column("red_mid_assists", sa.Integer(), nullable=True),
        sa.Column("red_dragon_assists", sa.Integer(), nullable=True),
        sa.Column("red_sup_assists", sa.Integer(), nullable=True),
        sa.Column("blue_baron_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("blue_mid_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("blue_sup_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("red_baron_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("red_jungle_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("red_mid_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("red_dragon_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("red_sup_dmg_taken", sa.Integer(), nullable=True),
        sa.Column("blue_baron_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("blue_mid_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("blue_sup_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("red_baron_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("red_jungle_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("red_mid_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("red_dragon_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("red_sup_dmg_dealt", sa.Integer(), nullable=True),
        sa.Column("blue_baron_total_gold", sa.Integer(), nullable=True),
        sa.Column("blue_jungle_total_gold", sa.Integer(), nullable=True),
        sa.Column("blue_mid_total_gold", sa.Integer(), nullable=True),
        sa.Column("blue_dragon_total_gold", sa.Integer(), nullable=True),
        sa.Column("blue_sup_total_gold", sa.Integer(), nullable=True),
        sa.Column("red_baron_total_gold", sa.Integer(), nullable=True),
        sa.Column("red_jungle_total_gold", sa.Integer(), nullable=True),
        sa.Column("red_mid_total_gold", sa.Integer(), nullable=True),
        sa.Column("red_dragon_total_gold", sa.Integer(), nullable=True),
        sa.Column("red_sup_total_gold", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ("blue_ban_1",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_ban_2",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_ban_3",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_ban_4",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_ban_5",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_baron_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_baron_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_dragon_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_dragon_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_jungle_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_jungle_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_mid_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_mid_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_pick_1",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_pick_2",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_pick_3",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_pick_4",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_pick_5",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_side",),
            ["team.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_sup_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("blue_sup_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("matchup_id",),
            ["matchup.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_ban_1",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_ban_2",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_ban_3",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_ban_4",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_ban_5",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_baron_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_baron_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_dragon_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_dragon_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_jungle_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_jungle_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_mid_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_mid_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_pick_1",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_pick_2",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_pick_3",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_pick_4",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_pick_5",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_side",),
            ["team.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_sup_pick",),
            ["champion.id"],
        ),
        sa.ForeignKeyConstraint(
            ("red_sup_player",),
            ["player.id"],
        ),
        sa.ForeignKeyConstraint(
            ("winner",),
            ["team.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("uuid"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("matchup_map")
    op.drop_table("matchup")
    op.drop_table("player")
    op.drop_table("auth_role_user")
    op.drop_table("team")
    op.drop_table("champion")
    op.drop_table("auth_user")
    op.drop_table("auth_role")
    op.execute("""DROP TYPE role""")
    # ### end Alembic commands ###
