from sqlalchemy import Integer,Boolean,String,Date,DateTime,ForeignKey,func,LargeBinary
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, MappedColumn
from src.database import public_base,schema_base
from datetime import date
# Public schema
class Tenant(public_base):
    __tablename__ = "tenant"
    __table_args__ = {"schema": "public"}
    id:Mapped[int] = MappedColumn(Integer,primary_key=True,index=True)
    name: Mapped[str] = MappedColumn(String(50),unique=True)
    schema_name:Mapped[str] = MappedColumn(String(50))
    created_at:Mapped[date] = MappedColumn(Date, default= date.today())

class User_table(public_base):
    __tablename__ = "users"
    __table_args__ = {"schema": "public"}
    user_id = MappedColumn(Integer,primary_key=True,index=True)
    tenant_id = MappedColumn(Integer,ForeignKey('public.tenant.id'))
    first_name = MappedColumn(String(50))
    last_name = MappedColumn(String(50))
    email_id = MappedColumn(String(50),unique=True)
    hashed_pwd = MappedColumn(String(256))
    role = MappedColumn(String(50))
    is_active = MappedColumn(Boolean)

class User_session_table(public_base):
    __tablename__ = "user_session"
    __table_args__ = {"schema":"public"}
    session_id = MappedColumn(Integer,primary_key=True,index=True)
    user_id = MappedColumn(Integer,ForeignKey("public.users.user_id",ondelete="CASCADE"),nullable=False)
    refresh_token = MappedColumn(LargeBinary(32),nullable=True)
    expiry_date = MappedColumn(DateTime,nullable=False)
    revoked = MappedColumn(Boolean,nullable=False)

# private schemas


class document_identity_table(schema_base):
    __tablename__ = "Document_table"
    id = MappedColumn(Integer,primary_key=True,index=True)
    title = MappedColumn(String(50))
    owner_id = MappedColumn(Integer,unique=True)
    permissions = MappedColumn(ARRAY(String,dimensions=1))
    is_locked = MappedColumn(Boolean)
    locked_by_id = MappedColumn(Integer,unique=True)
    current_version_id = MappedColumn(Integer,ForeignKey('Document_version_table.id',use_alter=True))

class document_permission_table(schema_base):
    __tablename__ = "document_permission_table"
    id = MappedColumn(Integer,primary_key=True,index=True)
    document_id = MappedColumn(Integer,ForeignKey("Document_table.id",use_alter=True))
    permissions = MappedColumn(ARRAY(String,dimensions=1))
    active = MappedColumn(Boolean)

class document_version_table(schema_base):
    __tablename__ = "Document_version_table"

    id = MappedColumn(Integer,primary_key=True,index=True)
    document_id = MappedColumn(Integer,ForeignKey('Document_table.id',use_alter=True))
    version_number = MappedColumn(Integer)
    s3_path = MappedColumn(String(50))
    file_hash = MappedColumn(String(50))
    change_note = MappedColumn(String(50))
    size_bytes = MappedColumn(Integer)
    created_at = MappedColumn(Date, default= date.today())

# Audit schema

class audit_table(schema_base):
    __tablename__ = "Audit_table"
    id = MappedColumn(Integer,primary_key=True,index=True)
    user_name = MappedColumn(String(50))
    action = MappedColumn(String(50))
    doc_id = MappedColumn(Integer,ForeignKey('Document_table.id',use_alter=True))
    ip_address = MappedColumn(String(50))
    timestamp = MappedColumn(Date,server_default=func.now())

# trash table

class trash_table(schema_base):
    __tablename__ = "Trash_table"
    id = MappedColumn(Integer,primary_key=True,index=True)
    document_id = MappedColumn(Integer,ForeignKey('Document_table.id',use_alter=True))
    deleted_by_id = MappedColumn(Integer,unique=True)