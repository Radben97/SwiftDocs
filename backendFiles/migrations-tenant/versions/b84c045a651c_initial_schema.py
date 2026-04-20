"""initial schema

Revision ID: b84c045a651c
Revises: 
Create Date: 2026-03-01 00:02:10.919349

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'b84c045a651c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ----------------------------
    # Document_table
    # ----------------------------
    op.create_table(
        "Document_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("title", sa.String(50)),
        sa.Column("owner_id", sa.Integer, unique=True),
        sa.Column("is_locked", sa.Boolean),
        sa.Column("locked_by_id", sa.Integer, unique=True),
        sa.Column("current_version_id", sa.Integer),
    )
    op.create_index("ix_Document_table_id", "Document_table", ["id"])

    # ----------------------------
    # Document_version_table
    # ----------------------------
    op.create_table(
        "Document_version_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("document_id", sa.Integer),
        sa.Column("version_number", sa.Integer),
        sa.Column("s3_path", sa.String(50)),
        sa.Column("file_hash", sa.String(50)),
        sa.Column("change_note", sa.String(50)),
        sa.Column("size_bytes", sa.Integer),
        sa.Column("created_at", sa.Date, server_default=sa.func.current_date()),
    )
    op.create_index(
        "ix_Document_version_table_id",
        "Document_version_table",
        ["id"],
    )

    # ----------------------------
    # document_permission_table
    # ----------------------------
    op.create_table(
        "document_permission_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("document_id", sa.Integer),
        sa.Column("use_type", sa.String(50)),
        sa.Column("use_id", sa.Integer),
        sa.Column(
            "permissions",
            postgresql.ARRAY(sa.String(), dimensions=1),
        ),
    )
    op.create_index(
        "ix_document_permission_table_id",
        "document_permission_table",
        ["id"],
    )

    # ----------------------------
    # Audit_table
    # ----------------------------
    op.create_table(
        "Audit_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_name", sa.String(50)),
        sa.Column("action", sa.String(50)),
        sa.Column("doc_id", sa.Integer),
        sa.Column("ip_address", sa.String(50)),
        sa.Column("timestamp", sa.Date, server_default=sa.func.now()),
    )
    op.create_index("ix_Audit_table_id", "Audit_table", ["id"])
    op.create_table(
        "Trash_table",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("document_id", sa.Integer),
        sa.Column("deleted_by_id", sa.Integer, unique=True),
    )
    op.create_index("ix_Trash_table_id", "Trash_table", ["id"])

    # ----------------------------
    # Foreign keys (added AFTER)
    # ----------------------------
    op.create_foreign_key(
        "fk_doc_current_version",
        "Document_table",
        "Document_version_table",
        ["current_version_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_version_document",
        "Document_version_table",
        "Document_table",
        ["document_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_permission_document",
        "document_permission_table",
        "Document_table",
        ["document_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_audit_document",
        "Audit_table",
        "Document_table",
        ["doc_id"],
        ["id"],
    )

    op.create_foreign_key(
        "fk_trash_document",
        "Trash_table",
        "Document_table",
        ["document_id"],
        ["id"],
    )


def downgrade() -> None:
    def downgrade():
    # ----------------------------
    # Drop foreign keys
    # ----------------------------
     op.drop_constraint("fk_trash_document", "Trash_table", type_="foreignkey")
    op.drop_constraint("fk_audit_document", "Audit_table", type_="foreignkey")
    op.drop_constraint(
        "fk_permission_document",
        "document_permission_table",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_version_document",
        "Document_version_table",
        type_="foreignkey",
    )
    op.drop_constraint(
        "fk_doc_current_version",
        "Document_table",
        type_="foreignkey",
    )

    # ----------------------------
    # Drop tables
    # ----------------------------
    op.drop_table("Trash_table")
    op.drop_table("Audit_table")
    op.drop_table("document_permission_table")
    op.drop_table("Document_version_table")
    op.drop_table("Document_table")
