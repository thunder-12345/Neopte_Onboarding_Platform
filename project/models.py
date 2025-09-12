from project import db, login_manager 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from typing import List
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique = True)
    #role: Mapped[str] = mapped_column()
    password_hash: Mapped[str] = mapped_column(db.String(128))

    # hours: Mapped[List["Hours"]] = relationship(back_populates="user")
    # document: Mapped[List["Document"]] = relationship(back_populates="user")

    def __init__(self, name, email, password): ## do smth about the role to view dif dashboards
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, input_password):
        return check_password_hash(self.password_hash, input_password)

    def __repr__(self):
        return f"This is {self.name} with the email {self.email}"


class Hours(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    date: Mapped[str] = mapped_column() 
    amount: Mapped[str] = mapped_column() 
    description: Mapped[str] = mapped_column()
    # user: Mapped[int] = relationship(back_populates="hours")

    def __init__(self, date, amount, description):
        self.date = date
        self.amount = amount
        self.description = description


class Document(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    filename: Mapped[str] = mapped_column() 
    doctype: Mapped[str] = mapped_column() 
    status: Mapped[str] = mapped_column()
    # user: Mapped[int] = relationship(back_populates="document")

    def __init__(self, filename, doctype, status):
        self.filename = filename
        self.doctype = doctype
        self.status = status







    




