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
@app.route('/index/<int:page>')
def index(page=1):
    blog = Blog.query.first()
    posts = Post.query.filter_by(live=True).order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/index.html', blog=blog, posts=posts)
    
@app.route('/admin')
@app.route('/admin/<int:page>')
@login_required
@author_required
def admin(page=1):
    posts = Post.query.order_by(Post.publish_date.desc()).paginate(page, POSTS_PER_PAGE, False)
    return render_template('blog/admin.html', posts=posts)
    
@app.route('/setup', methods=('GET, POST'))
def setup():
    blogs = Blog.query.count()
    if blogs():
        return redirect(url_for('admin'))
    form = SetupForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author = Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            True
        )
    