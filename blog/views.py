from flask_blog import app
from flask import render_template, redirect, flash, url_for, session, request
from blog.form import SetupForm, PostForm
from flask_blog import db, uploaded_images
from author.models import Author
from blog.models import Blog, Post, Category
from author.decorators import login_required, author_required
import bcrypt
from slugify import slugify
from flask_uploads import UploadNotAllowed

POSTS_PER_PAGE = 5

@app.route('/')
@app.route('/index')

def index():
    return "Hello World"