import uuid
import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, JSON, Integer, Float, Boolean, ARRAY
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import UUID, JSONB

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    github_login = Column(String, unique=True, index=True)
    github_id = Column(String, unique=True, index=True)
    avatar_url = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Session(Base):
    __tablename__ = "sessions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String)
    status = Column(String, default="queued") # queued, processing, completed, failed
    
    runtime_detected = Column(String, nullable=True)
    raw_log = Column(Text)
    parsed_frames = Column(JSONB, nullable=True)
    
    matched_pattern_id = Column(UUID(as_uuid=True), ForeignKey("patterns.id"), nullable=True)
    pattern_confidence = Column(Float, nullable=True)
    
    llm_explanation = Column(Text, nullable=True)
    root_causes = Column(JSONB, nullable=True)
    suggested_fixes = Column(JSONB, nullable=True)
    
    tags = Column(ARRAY(String), default=[])
    
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    github_issue_url = Column(String, nullable=True)

class SessionComment(Base):
    __tablename__ = "session_comments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    text = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Pattern(Base):
    __tablename__ = "patterns"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    runtime = Column(String)
    regexes = Column(ARRAY(String))
    description = Column(Text)
    common_causes = Column(ARRAY(String))
    common_fixes = Column(ARRAY(String))
    references = Column(ARRAY(String))
