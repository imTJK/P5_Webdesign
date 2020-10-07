"""users

Revision ID: 1d0a26ab6b9f
Revises: 
Create Date: 2020-09-19 13:22:39.481997

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1d0a26ab6b9f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
        sa.Column('user_id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
        sa.Column('created_at', mysql.DATETIME(), server_default=sa.text('current_timestamp()'), nullable=True),
        sa.Column('username', mysql.VARCHAR(length=30), nullable=False),
        sa.Column('email', mysql.VARCHAR(length=100), nullable=False),
        sa.Column('password_hash', mysql.VARCHAR(length=255), nullable=False),
        sa.PrimaryKeyConstraint('user_id'),
        mysql_default_charset='utf8mb4',
        mysql_engine='InnoDB'
    )

    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_entry_created_at'), table_name='entry')
    op.drop_index(op.f('ix_entry_created_by'), table_name='entry')
    op.drop_table('entry')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    
    op.create_table('entry',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(length=30), nullable=True),
        sa.Column('email', sa.String(length=255), nullable=True),
        sa.Column('password', sa.String(length=255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    # ### end Alembic commands ###