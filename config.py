import os

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'postgres://uwmpennjucjmvr:3fcf1bce75c0dd80c993cdb7430199005b0ee03dd41c00cf0ae60cb00ff82d85@ec2-54-224-194-214.compute-1.amazonaws.com:5432/d2it6mc05df5a2'
SQLALCHEMY_TRACK_MODIFICATIONS = False