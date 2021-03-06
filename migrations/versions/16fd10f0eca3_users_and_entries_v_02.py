"""users and entries v 02

Revision ID: 16fd10f0eca3
Revises: ff86b50c2173
Create Date: 2020-09-19 17:23:38.458659

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '16fd10f0eca3'
down_revision = 'ff86b50c2173'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_user_email', table_name='users')
    op.drop_index('ix_user_username', table_name='users')
    
    op.create_foreign_key(None, 'entries', 'users', ['created_by_id'], ['id'])
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('users', 'password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=True)
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    op.create_index(op.f('ix_users_created_at'), 'users', ['created_at'], unique=False)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
   
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('ix_user_username', 'users', ['username'], unique=False)
    op.create_index('ix_user_email', 'users', ['email'], unique=True)
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_created_at'), table_name='users')
    op.alter_column('users', 'username',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.alter_column('users', 'password_hash',
               existing_type=mysql.VARCHAR(length=255),
               nullable=False)
    op.alter_column('users', 'email',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.drop_constraint(None, 'entries', type_='foreignkey')
    # ### end Alembic commands ###
