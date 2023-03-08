"""add users, queries

Revision ID: 9da6dd615d34
Revises: 
Create Date: 2023-03-08 18:48:20.131561

"""
from alembic import op
import sqlalchemy as sa
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.core.settings import settings
from src.services.utils.secure import SecureService


# revision identifiers, used by Alembic.
revision = '9da6dd615d34'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(sa.schema.CreateSchema(settings.db_schema))
    
    users = op.create_table('users',
        sa.Column('guid', GUID, nullable=False),
        sa.Column('login', sa.String(), nullable=False),
        sa.Column('password_hashed', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('guid'),
        sa.UniqueConstraint('login'),
        schema='server'
    )
    op.bulk_insert(users, [{
        'guid': GUID_DEFAULT_SQLITE(),
        'login': settings.admin_login,
        'password_hashed': SecureService.hash_password(settings.admin_password),
    }])
    
    op.create_table('queries',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('method', sa.Enum('GET', 'POST', 'PUT', 'DELETE', name='methods_enum', schema='server'), nullable=False),
        sa.Column('url', sa.String(), nullable=False),
        sa.Column('user_guid', GUID, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='server'
    )


def downgrade() -> None:
    op.drop_table('queries', schema='server')
    op.drop_table('users', schema='server')
    op.execute('drop type server.methods_enum')
    op.execute(sa.schema.DropSchema(settings.db_schema))
