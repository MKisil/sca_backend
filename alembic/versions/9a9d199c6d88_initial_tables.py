"""Initial tables

Revision ID: 9a9d199c6d88
Revises: 
Create Date: 2025-05-15 14:05:11.911714

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a9d199c6d88'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cats',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('experience', sa.Integer(), nullable=False),
    sa.Column('breed', sa.String(), nullable=False),
    sa.Column('salary', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_cats_id'), 'cats', ['id'], unique=False)
    op.create_table('missions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cat_id', sa.Integer(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['cat_id'], ['cats.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_missions_id'), 'missions', ['id'], unique=False)
    op.create_table('targets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('mission_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('country', sa.String(length=255), nullable=False),
    sa.Column('notes', sa.String(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['mission_id'], ['missions.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_targets_id'), 'targets', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_targets_id'), table_name='targets')
    op.drop_table('targets')
    op.drop_index(op.f('ix_missions_id'), table_name='missions')
    op.drop_table('missions')
    op.drop_index(op.f('ix_cats_id'), table_name='cats')
    op.drop_table('cats')
    # ### end Alembic commands ###
