import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import sqlalchemy
from flask.ext.sqlalchemy import SQLAlchemy

from flask_blog import app, db

# need to add all models for db.create_all to work
from author.models import *
from blog.models import *

class UserTest(unittest.TestCase):
    def setUp(self):
        self.db_uri = 'mysql+pymysql://%s:%s@%s/' % (app.config['DB_USERNAME'], app.config['DB_PASSWORD'], app.config['DB_HOST'])
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['BLOG_DATABASE_NAME'] = 'test_blog'
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri + app.config['BLOG_DATABASE_NAME']
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("create database "  + app.config['BLOG_DATABASE_NAME'])
        db.create_all()
        conn.close()
        self.app = app.test_client
    
    def tearDown(self):
        db.session.remove()
        engine = sqlalchemy.create_engine(self.db_uri)
        conn = engine.connect()
        conn.execute("commit")
        conn.execute("drop database "  + app.config['BLOG_DATABASE_NAME'])
        conn.close()
        
    def create_blog(self):
        return self.app.post('/setup', data=dict (
            name='Flask Blog',
            fullname='Joe Bloggs',
            email='joebloggs@example.com',
            username='jorge',
            password='test',
            confirm='test'
            ),
        follow_redirects = True)
    
    def login(self, username, password):
        self.app.post('/login', data=dict (
            username=username,
            password=password
            ), follow_redirects = True)
            
    def logout(self):
        return self.app.get('/logout', follow_redirects=True)
        
    def register_user(self, fullname, email, username, password, confirm):
        return self.app.post('/register', data=dict (
            fullname=fullname,
            email=email,
            username=username,
            password=password,
            confirm=confirm
            ),
        follow_redirects = True)
        
    
        