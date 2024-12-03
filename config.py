import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///household_services.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False