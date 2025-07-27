from sqlmodel import Session, select
from app.models import User, Blog
from app.schemas import UserCreate, BlogCreate

def create_user(user: UserCreate, db: Session):
    db_user = User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(user_id: int, db: Session):
    return db.exec(select(User).where(User.id == user_id)).first()

def create_blog(blog: BlogCreate, db: Session):
    db_blog = Blog(title=blog.title, content=blog.content, author_id=blog.author_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def get_blogs(db: Session):
    return db.exec(select(Blog)).all()
