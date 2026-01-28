from project import db, login_manager 
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from typing import List
from sqlalchemy import Date, DateTime, func, text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import date, datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    address: Mapped[str] = mapped_column(default="None Provided")
    password_hash: Mapped[str] = mapped_column(db.String(128))
    date_created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    total_hours: Mapped[float] = mapped_column(default=0.0)
    picture: Mapped[str] = mapped_column(default="default.jpeg")
    role: Mapped[str] = mapped_column(default="user")  # "user", "volunteer", " intern", "board"

    hours: Mapped[List["Hours"]] = relationship("Hours", back_populates="user", cascade="all, delete-orphan")
    documents: Mapped[List["Document"]] = relationship("Document", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, name, email, password, picture, role="user"):
        self.name = name
        self.email = email
        self.password_hash = generate_password_hash(password, method = "pbkdf2:sha256")
        self.date_created = func.now()
        self.picture = picture
        self.role = role

    def check_password(self, input_password):
        return check_password_hash(self.password_hash, input_password)

    def __repr__(self):
        return f"This is {self.name} with the email {self.email} and role {self.role}"


class Hours(db.Model):

    __tablename__ = 'hours'

    id: Mapped[int] = mapped_column(primary_key=True)
    activity_name: Mapped[str] = mapped_column()
    date: Mapped[datetime.date] = mapped_column(Date)
    start_time: Mapped[datetime.time] = mapped_column(db.Time)
    end_time: Mapped[datetime.time] = mapped_column(db.Time)
    amount: Mapped[float] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(server_default=text("'Pending'"))  # "pending", "approved", "denied"
    user: Mapped["User"] = relationship("User", back_populates="hours")

    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), name="fk_hours_user_id")

    def __init__(self, activity_name, date, start_time, end_time, amount, description, user, status="Pending"):
        self.activity_name = activity_name
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.amount = amount
        self.description = description
        self.user = user
        self.status = status

    def __repr__(self):     
        return f"Activity: {self.activity_name} on {self.date} for {self.amount} hours. Status: {self.status}"


class Document(db.Model):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)
    filename: Mapped[str] = mapped_column()
    doctype: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default=("Pending"))  # "pending", "approved", "denied"
    description: Mapped[str] = mapped_column(default="No description provided")
    user: Mapped["User"] = relationship("User", back_populates="documents")

    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), name="fk_documents_user_id")

    def __init__(self, filename, doctype, user, description = "No description provided",status = "Pending"):
        self.filename = filename
        self.doctype = doctype
        self.user = user
        self.description = description
        self.status = status 

class ActivityLog(db.Model):
    __tablename__ = "activity_logs"

    id: Mapped[int] = mapped_column(primary_key=True)

    # WHO caused the action
    actor_id: Mapped[int] = mapped_column(db.ForeignKey("users.id"))
    actor = relationship("User")

    # WHAT happened
    action: Mapped[str] = mapped_column()

    # WHAT was affected (generic target)
    target_type: Mapped[str] = mapped_column()
    target_id: Mapped[int] = mapped_column()

    # WHEN it happened
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    # OPTIONAL structured context
    details: Mapped[dict] = mapped_column(JSON, nullable=True)

    def __repr__(self):
        return (
            f"<ActivityLog {self.action} "
            f"on {self.target_type}:{self.target_id}>"
        )

class Task(db.Model):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(primary_key=True)
    classification: Mapped[str] = mapped_column()  # "project" or "reminder"
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    assigned_role: Mapped[str] = mapped_column(nullable=True)  # e.g., "intern" for reminders
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    created_by_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), nullable=True)
    created_by: Mapped["User"] = relationship("User", foreign_keys=[created_by_id])
    # Relationship to TaskAssignment
    assignments: Mapped[List["TaskAssignment"]] = relationship(
        "TaskAssignment", back_populates="task", cascade="all, delete-orphan"
    )

    def __init__(self, classification, title, description, created_by, assigned_role=None):
        self.classification = classification
        self.title = title
        self.description = description
        self.created_by = created_by
        self.assigned_role = assigned_role
        self.created_at = func.now()

    def __repr__(self):
        return f"Task: {self.title} ({self.classification})"


class TaskAssignment(db.Model):
    __tablename__ = 'task_assignments'

    id: Mapped[int] = mapped_column(primary_key=True)
    task_id: Mapped[int] = mapped_column(db.ForeignKey('tasks.id'), name="fk_taskassign_task_id")
    user_id: Mapped[int] = mapped_column(db.ForeignKey('users.id'), name="fk_taskassign_user_id")

    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=False) 
    status: Mapped[str] = mapped_column(default="pending")  # "pending" or "done" or "graded"
    upload: Mapped[bool] = mapped_column(default=False) 
    filename: Mapped[str] = mapped_column(nullable=True) # can be used if upload is True
    score: Mapped[float] = mapped_column(nullable=True)
    comments: Mapped[str] = mapped_column(default="")

    # Relationships
    task: Mapped["Task"] = relationship("Task", back_populates="assignments")
    user: Mapped["User"] = relationship("User")

    def __init__(self, task, user, due_date, status="pending", upload=None, score=None, comments=""):
        self.task = task
        self.user = user
        self.status = status
        self.upload = upload
        self.score = score
        self.comments = comments
        self.due_date = due_date

    def __repr__(self):
        return f"TaskAssignment: {self.task.title} -> {self.user.name} ({self.status})"





