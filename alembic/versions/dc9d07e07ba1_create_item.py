"""create item

Revision ID: dc9d07e07ba1
Revises: 49a5c4b162b9
Create Date: 2021-06-13 04:24:29.621405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dc9d07e07ba1'
down_revision = '49a5c4b162b9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("item",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("cliente_cpf", sa.String(11), sa.ForeignKey("cliente.cpf"), nullable=False),
                    sa.Column("codigo_produto", sa.String(200), nullable=False),
                    sa.Column("nome", sa.String(100), nullable=False),
                    sa.Column("quantidade", sa.Integer, nullable=False))


def downgrade():
    op.drop_table('item')
