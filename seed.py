"""Seed file for sample data"""

from user import db
from app import app

# Create all tables
db.drop_all()
db.create_all()