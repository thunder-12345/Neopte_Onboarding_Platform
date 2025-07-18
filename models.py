import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
Migrate(app,db)

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique = True)
    role: Mapped[str] = mapped_column()
    hours: Mapped[List["Hours"]] = relationship()

    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role

    def __repr__(self):
        return f"This is {self.name} - {self.role} with the email {self.email}"


class Hours(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    date: Mapped[str] = mapped_column() 
    amount: Mapped[str] = mapped_column() 
    description: Mapped[str] = mapped_column()
    user: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __init__(self, date, amount, description):
        self.date = date
        self.amount = amount
        self.description = description


class Document(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    filename: Mapped[str] = mapped_column() 
    doctype: Mapped[str] = mapped_column() 
    status: Mapped[str] = mapped_column()
    user: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __init__(self, filename, doctype, status):
        self.filename = filename
        self.doctype = doctype
        self.status = status







    




