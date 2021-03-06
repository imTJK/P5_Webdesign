"""updated_users

Revision ID: c72755003741
Revises: 2dfff6ba3dc7
Create Date: 2020-09-27 14:32:05.225502

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'c72755003741'
down_revision = '2dfff6ba3dc7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('security_question', sa.Integer(), nullable=False))
    op.add_column('users', sa.Column('otp_secret', sa.String(length=10), nullable=False))
    op.add_column('users', sa.Column('hashed_security_answer', sa.String(length=255), nullable=False))
    op.add_column('users', sa.Column('is_active', mysql.TINYINT(display_width=1), server_default=sa.text('0'), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('has_2fa', mysql.TINYINT(display_width=1), server_default=sa.text('0'), autoincrement=False, nullable=False))
    op.alter_column('imgs', 'img_1',
               existing_type=mysql.MEDIUMBLOB(),
               nullable=False)
    op.alter_column('imgs', 'filetypes_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('filetypes', 'ft_1',
               existing_type=mysql.VARCHAR(length=5),
               nullable=False)
    
    op.alter_column('entries', 'title',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('entries', 'imgs_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('entries', 'created_by_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'security_question')
    op.drop_column('users', 'hashed_security_answer')
    op.alter_column('entries', 'created_by_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('entries', 'imgs_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('entries', 'title',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.create_index(op.f('ix_entries_created_at'), 'entries', ['created_at'], unique=False)
    op.drop_index('ix_entry_created_at', table_name='entries')
    op.drop_index('ix_entry_created_by', table_name='entries')
    op.alter_column('filetypes', 'ft_1',
               existing_type=mysql.VARCHAR(length=5),
               nullable=True)
    op.alter_column('imgs', 'filetypes_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('imgs', 'img_1',
               existing_type=mysql.MEDIUMBLOB(),
               nullable=True)
    op.drop_index('ix_users_created_at', table_name='users')
    op.drop_column('users', 'is_active')
    # ### end Alembic commands ###
