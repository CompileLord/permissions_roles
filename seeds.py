from database import get_db
from sqlalchemy.orm import Session
from models import User, Permission, Role, AbstractBase
from utils import get_password, verify_password
from fastapi import Depends


def create_user(user: User, db: Session):
    username = db.query(User).where(User.username==user.username).one_or_none()
    if username:
        print(f"User {user.username} already exists\t->Skip")
    
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"User {user.username} successfully added!")

def create_permission(permission: Permission, db: Session):
    title = db.query(Permission).where(Permission.title==permission.title).one_or_none()
    if title:
        print(f"Permission {permission.title} already exists\t-> Skip")
    db.add(permission)
    db.commit()
    db.refresh(permission)
    print(f'Permission: {permission.title} successfully added')

def create_role(role:Role, db: Session):
    check_role = db.query(Role).where(Role.title==role.title).one_or_none()
    if check_role:
        print(f"Role {role.title} already exists")
    db.add(role)
    db.commit()
    db.refresh(role)
    print(f"Role {role.title} successfully added")


    


CRUD_OPERATION = ["read", "create", "delete", "update"]



def create_all_permissions(db: Session, role: Role):
    for model in AbstractBase.__subclasses__():
        for operation in CRUD_OPERATION:
            title_str = f"{operation}_{model.__name__.lower()}"
            
            permission = db.query(Permission).filter_by(title=title_str).first()
            if not permission:
                permission = Permission(title=title_str)
                db.add(permission)
                db.flush() 
            
            if permission not in role.permissions:
                role.permissions.append(permission)
    
    db.commit() 



admin_role = Role(title="admin")

session_0 = next(get_db())

create_all_permissions(db=session_0, role=admin_role)

session_1 = next(get_db())

user_admin = User(username="admin", password=get_password("admin123"), role=admin_role)
create_user(user=user_admin, db=session_1)
            


create_all_permissions(db=get_db, role=admin_role)

for i in AbstractBase.__subclasses__():
    print(i.__name__)


