from project import db, login_manager 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(db.String(128))
    role: Mapped[str] = mapped_column(default="user")  # "user", "volunteer", " intern", "board"

    hours: Mapped[List["Hours"]] = relationship("Hours", back_populates="user", cascade="all, delete-orphan")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, name, email, password, role="user"):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def check_password(self, input_password):
        return check_password_hash(self.password_hash, input_password)

    def __repr__(self):
        return f"This is {self.name} with the email {self.email} and role {self.role}"


class Hours(db.Model):
    __tablename__ = 'hours'

    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[str] = mapped_column()
    amount: Mapped[float] = mapped_column()
    description: Mapped[str] = mapped_column()
    user: Mapped["User"] = relationship("User", back_populates="hours")


    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), name="fk_hours_user_id")

    def __init__(self, date, amount, description, user):
        self.date = date
        self.amount = amount
        self.description = description
        self.user = user


class Document(db.Model):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column()
    doctype: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default=("Pending"))  # "pending", "approved", "rejected"
    user: Mapped["User"] = relationship("User", back_populates="documents")

    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), name="fk_documents_user_id")

    def __init__(self, filename, doctype, user, status = "Pending"):
        self.filename = filename
        self.doctype = doctype
        self.user = user
        self.status = status 







    




