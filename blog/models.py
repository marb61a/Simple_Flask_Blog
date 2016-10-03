from flask_blog import db, uploaded_images
from datetime import datetime

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    admin = db.Column(db.Integer, db.ForeignKey('author.id'))
    posts = db.relationship('Post', backref='blog', lazy='dynamic')
    
    def __init__(self, name, admin):
        self.name = name
        self.admin = admin
        
    def __repr__(self):
        return '<Name %r>' % self.name

class Post(db.Model):
    @property
    def imgsrc(self):
        return uploaded_images.url(self.image)
    
class Category(db.Model):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name