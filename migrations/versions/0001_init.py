"""init

Revision ID: 0001
Revises: 
Create Date: 2024-03-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table('patterns',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('runtime', sa.String(), nullable=True),
        sa.Column('regexes', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('common_causes', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('common_fixes', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('references', sa.ARRAY(sa.String()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table('users',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('github_login', sa.String(), nullable=True),
        sa.Column('github_id', sa.String(), nullable=True),
        sa.Column('avatar_url', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_github_id'), 'users', ['github_id'], unique=True)
    op.create_index(op.f('ix_users_github_login'), 'users', ['github_login'], unique=True)
    
    op.create_table('sessions',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('title', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('runtime_detected', sa.String(), nullable=True),
        sa.Column('raw_log', sa.Text(), nullable=True),
        sa.Column('parsed_frames', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('matched_pattern_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('pattern_confidence', sa.Float(), nullable=True),
        sa.Column('llm_explanation', sa.Text(), nullable=True),
        sa.Column('root_causes', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('suggested_fixes', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('tags', sa.ARRAY(sa.String()), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('resolved_at', sa.DateTime(), nullable=True),
        sa.Column('github_issue_url', sa.String(), nullable=True),
        sa.ForeignKeyConstraint(['matched_pattern_id'], ['patterns.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('session_comments',
        sa.Column('id', sa.UUID(as_uuid=True), nullable=False),
        sa.Column('session_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('user_id', sa.UUID(as_uuid=True), nullable=True),
        sa.Column('text', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['session_id'], ['sessions.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade() -> None:
    op.drop_table('session_comments')
    op.drop_table('sessions')
    op.drop_index(op.f('ix_users_github_login'), table_name='users')
    op.drop_index(op.f('ix_users_github_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('patterns')
