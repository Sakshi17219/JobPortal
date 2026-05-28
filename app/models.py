from .extensions import db, login_manager
from flask_login import UserMixin
from datetime import datetime
import json

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='seeker')  # 'admin' or 'seeker'
    skills = db.Column(db.Text, default='[]')  # JSON list of skills
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('Application', backref='user', lazy=True)

    def get_skills(self):
        return json.loads(self.skills or '[]')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    company = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    job_type = db.Column(db.String(30), default='Full-time')
    salary_min = db.Column(db.Integer)
    salary_max = db.Column(db.Integer)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text, default='[]')  # JSON list
    tags = db.Column(db.Text, default='[]')  # JSON list
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    applications = db.relationship('Application', backref='job', lazy=True)

    def get_tags(self):
        return json.loads(self.tags or '[]')

    def get_requirements(self):
        return json.loads(self.requirements or '[]')

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.String(30), default='applied')  # applied, interview, hired, rejected
    match_score = db.Column(db.Float, default=0.0)
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    cover_letter = db.Column(db.Text)
