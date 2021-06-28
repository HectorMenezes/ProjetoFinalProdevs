"""create operacoes

Revision ID: fa08bf8caf08
Revises: dc9d07e07ba1
Create Date: 2021-06-24 17:56:09.647986

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa08bf8caf08'
down_revision = '49a5c4b162b9'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("operacao",
                    sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
                    sa.Column("cpf", sa.String(11), sa.ForeignKey("cliente.cpf"), nullable=False),
                    sa.Column('pedido', sa.String(100), nullable=False),
                    sa.Column("codigo_produto", sa.String(200), nullable=False),
                    sa.Column("quantidade", sa.Integer, nullable=False),
                    sa.Column("tipo", sa.Boolean, nullable=False))


def downgrade():
    op.drop_table('operacao')
