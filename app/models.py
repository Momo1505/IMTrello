from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    projects = db.relationship('Project', secondary='projects_user', back_populates='users_project')
    assigned_tasks = db.relationship('Task', secondary='tasks_user', back_populates='assigned_users')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role', lazy='dynamic')


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.String())
    deadline = db.Column(db.DateTime)
    tasks = db.relationship('Task', backref='project')
    users_project = db.relationship('User', back_populates='projects', secondary='projects_user')


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(64), nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    description = db.Column(db.String())
    is_new = db.Column(db.Boolean, default=True, nullable=False)
    comment = db.Column(db.String(), nullable=False)
    priority = db.Column(db.String())
    deadline = db.Column(db.Date)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    assigned_users = db.relationship('User', secondary='tasks_user', back_populates='assigned_tasks')


tasks_user = db.Table(
    'tasks_user',
    db.Column('developer_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'))
)

projects_user = db.Table(
    'projects_user',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'))
)
