from flask_blog import app, db
from flask import render_template, redirect, session, request, url_for, flash
from author.form import RegisterForm, LoginForm
from author.models import Author
from author.decorators import login_required
import bcrypt

@app.route('/login', methods=('GET', 'POST'))
def login() :
    form = LoginForm
    error = None
    
    if request.method == 'GET' and request.args.get('next'):
        session['next'] = request.args.get('next', None)
    
    if form.validate_on_submit():
        author = Author.query.filter_by(
            username=form.username.data
        ).first()
        if author:
            if bcrypt.hashpw(form.password.data, author.password) == author.password:
                session['username'] = form.username.data
                session['is_author'] = author.is_author
                flash ("User %s logged in" % author.username)
                if 'next' in session:
                    next = session.get('next')
                    session.pop('next')
                    return redirect(next)
                else:
                    return redirect(url_for('index'))
            else:
                error = 'Incorrect Password'
        else:
            error = 'Author not found'
    return render_template('author/login.html', form=form, error=error)