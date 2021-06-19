"""create cliente

Revision ID: 49a5c4b162b9
Revises: 
Create Date: 2021-06-13 04:03:39.515877

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '49a5c4b162b9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("cliente",
                    sa.Column("cpf", sa.String(11), primary_key=True, autoincrement=False),
                    sa.Column("nome", sa.String(100), nullable=False),
                    sa.Column("email", sa.String(200), nullable=False),
                    sa.Column("data_nasc", sa.DateTime, nullable=False),
                    sa.Column("telefone", sa.String(13), nullable=False))


def downgrade():
    op.drop_table('cliente')

