"""Add roles

Revision ID: 47bba2649ee8
Revises: 0a843abd9712
Create Date: 2025-03-30 17:22:54.755836

"""

from typing import Sequence, Union

from sqlalchemy import Integer, String, column, table

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "47bba2649ee8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    roles_table = table(
        "roles", column("role_id", Integer), column("name", String)
    )

    try:
        op.bulk_insert(
            roles_table,
            [
                {"role_id": 0, "name": "default"},
                {"role_id": 1, "name": "superuser"},
            ],
        )
    except Exception as e:
        pass


def downgrade():
    pass
