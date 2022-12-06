"""fields for global ban implementation

Revision ID: 807aa834b4bd
Revises: 2a66f52f49d4
Create Date: 2022-12-06 16:20:23.750114

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "807aa834b4bd"
down_revision = "2a66f52f49d4"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("matchup", schema=None) as batch_op:
        batch_op.add_column(sa.Column("bo_size", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("with_global_ban", sa.Boolean(), nullable=True))
        batch_op.add_column(sa.Column("last_no_global_ban", sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("matchup", schema=None) as batch_op:
        batch_op.drop_column("last_no_global_ban")
        batch_op.drop_column("with_global_ban")
        batch_op.drop_column("bo_size")
    # ### end Alembic commands ###