from sqlalchemy import String, Integer, ForeignKey, DateTime, func, Table, Column
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class AbstractBase(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

permissions_role = Table(
    "permissions_role", AbstractBase.metadata,
    Column("permission_id", Integer, ForeignKey("permissions.id"), primary_key=True),
    Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True)
)


class User(AbstractBase):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("roles.id"))
    
    role = relationship("Role", back_populates="users")
    
    def __repr__(self):
        return self.username


class Role(AbstractBase):
    __tablename__ = "roles"
    title: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    
    users = relationship(User, back_populates="role")
    permissions = relationship("Permission", back_populates="role", secondary=permissions_role)
    
    def __repr__(self):
        return self.title
    
class Permission(AbstractBase):
    __tablename__ = "permissions"
    title: Mapped[str] = mapped_column(String(100), unique=True)
    
    role = relationship("Role", back_populates="permissions", secondary=permissions_role)
    
    def __repr__(self):
        return self.title
    
    
    




