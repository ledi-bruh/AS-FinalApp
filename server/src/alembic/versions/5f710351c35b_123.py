"""123

Revision ID: 5f710351c35b
Revises: 
Create Date: 2023-03-08 13:19:11.589034

"""
from alembic import op
import sqlalchemy as sa
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from src.core.settings import settings
from src.services.utils.secure import SecureService


# revision identifiers, used by Alembic.
revision = '5f710351c35b'
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


def downgrade() -> None:
    op.drop_table('users', schema='server')
    op.execute(sa.schema.DropSchema(settings.db_schema))
