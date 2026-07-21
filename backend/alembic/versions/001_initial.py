"""Initial migration: pgvector extension and core tables

Revision ID: 001_initial
Revises: 
Create Date: 2026-07-16 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    dialect = op.get_bind().dialect.name

    if dialect == "postgresql":
        # 1. Create pgvector extension (PostgreSQL only)
        op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        from pgvector.sqlalchemy import Vector
        uuid_type = postgresql.UUID(as_uuid=True)
        array_text_type = postgresql.ARRAY(sa.Text())
        jsonb_type = postgresql.JSONB(astext_type=sa.Text())
        embedding_col = sa.Column('embedding', Vector(384), nullable=True)
    else:
        # SQLite-compatible fallbacks for local development
        uuid_type = sa.String(36)
        array_text_type = sa.Text()   # stored as comma-separated or JSON string
        jsonb_type = sa.Text()         # stored as JSON string
        embedding_col = sa.Column('embedding', sa.Text(), nullable=True)

    # 2. Create documents table
    op.create_table(
        'documents',
        sa.Column('id', uuid_type, primary_key=True),
        sa.Column('filename', sa.Text(), nullable=False),
        sa.Column('document_type', sa.Text(), nullable=True),
        sa.Column('uploaded_by', sa.Text(), nullable=True),
        sa.Column('uploaded_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.Text(), server_default='pending', nullable=False),
        sa.Column('graph_node_ids', array_text_type, nullable=True)
    )

    # 3. Create document_chunks table
    op.create_table(
        'document_chunks',
        sa.Column('id', uuid_type, primary_key=True),
        sa.Column('document_id', uuid_type, sa.ForeignKey('documents.id', ondelete='CASCADE'), nullable=False),
        sa.Column('chunk_text', sa.Text(), nullable=True),
        embedding_col
    )

    # 4. Create alerts table
    op.create_table(
        'alerts',
        sa.Column('id', uuid_type, primary_key=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('related_equipment_tags', array_text_type, nullable=True),
        sa.Column('severity', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('acknowledged', sa.Boolean(), server_default=sa.text('false'), nullable=False)
    )

    # 5. Create audit_log table
    op.create_table(
        'audit_log',
        sa.Column('id', uuid_type, primary_key=True),
        sa.Column('action', sa.Text(), nullable=True),
        sa.Column('actor', sa.Text(), nullable=True),
        sa.Column('details', jsonb_type, nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('audit_log')
    op.drop_table('alerts')
    op.drop_table('document_chunks')
    op.drop_table('documents')

