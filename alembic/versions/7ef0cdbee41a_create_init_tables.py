"""create init tables

Revision ID: 7ef0cdbee41a
Revises:
Create Date: 2022-02-05 16:15:15.246831

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7ef0cdbee41a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "document",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("processing_status", sa.String(), nullable=False),
        sa.Column("pages_count", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "processed_image",
        sa.Column("document_id", sa.Integer(), nullable=False),
        sa.Column("page_number", sa.Integer(), nullable=False),
        sa.Column("file_path", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(
            ["document_id"],
            ["document.id"],
        ),
        sa.PrimaryKeyConstraint("document_id", "page_number"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("processed_image")
    op.drop_table("document")
    # ### end Alembic commands ###