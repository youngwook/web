from __future__ import with_statement
import time
from contextlib import closing
from sqlite3 import dbapi2 as sqlite3
from datetime import datetime
from flask import Flask, g, render_template, request, session, url_for, redirect, abort, flash

#configuration
DATABASE = 'test.db'
PER_PAGE = 10
SECRET_KEY = 'hello'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    """Return a new connection to the database."""
    return sqlite3.connect(DATABASE)

def format_datetime(date):
    '''format a times for display'''
    return datetime.utcfromtimestamp(date).strftime('%Y-%m-%d | %H:%M')

def query_db(query, args=(), one=False):
    '''query the database and returns a list of dictionaries'''
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]

    return (rv[0] if rv else None) if one else rv

def get_u_id(username):
    rv = g.db.execute('select u_id from user where username = ?', [username]).fetchone()
    return rv[0] if rv else None

@app.before_request
def before_request():
    '''
    make sure we are connected to the database each request and look up
    the current user so that we know he is there
    '''
    g.db = connect_db()
    g.user = None
    if 'u_id' in session:
        g.user = query_db('select * from user where u_id = ?', [session['u_id']], one=True)

@app.teardown_request
def teardown_request(exception):
    '''closes the database at eht end of request'''
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
@app.route('/public')
def public():

    return render_template('public.html', messages = query_db('''select blog.*, user.* from blog, user
    where blog.u_id = user.u_id order by blog.time desc limit ?''', [PER_PAGE]))

@app.route('/edit', methods=['GET','POST'])
def edit():
    error = None
    if 'u_id' not in session:
        abort(401)
    if request.method == 'POST':

        if not request.form['title']:
            error = "you have enter title"
        elif not request.form['content']:
            error = "you have enter content"
        else:
            g.db.execute('''insert into blog (title, content, u_id, time) values (?,?,?,?)''',
                     (request.form['title'], request.form['content'], session['u_id'], time.time()))
            g.db.commit()
            flash("successfuly recorded!")
            return redirect(url_for('public'))
        return render_template('edit.html', error = error)
    return render_template('edit.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user:
        return redirect(url_for('public'))
    error = None
    if request.method == 'POST':
        user = query_db('select * from user where username = ?', [request.form['username']], one=True)

        if user is None:
            error = 'Invalid username'
        elif user['pwd'] != request.form['pwd']:
            error = 'Invalid password'
        else:
            flash('log in successful!')
            session['u_id'] = user['u_id']
            return redirect(url_for('public'))

    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if g.user:
        return redirect(url_for('public'))
    error = None
    if request.method == 'POST':

        if not request.form['username']:
            error = 'you have enter username'
        elif not request.form['pwd']:
            error = 'you have enter password'
        elif get_u_id(request.form['username']) is not None:
            error = 'the username is exist'
        else:
            g.db.execute('''insert into user (username, pwd) values (?,?)''', (request.form['username'],request.form['pwd']))
            g.db.commit()
            flash('sign up successful!')
            return redirect(url_for('login'))
    return render_template('register.html', error=error)

@app.route('/logout')
def logout():
    flash('you were logged out')
    session.pop('u_id', None)
    return redirect(url_for('public'))

@app.route('/<int:id>')
def blog(id):
    return render_template('user.html', message =query_db('select * from blog where b_id = ?',[id], one=True))

app.jinja_env.filters['timeformat'] = format_datetime





















'''
def init_db():
    """create the database tables"""
    with closing(connect_db()) as db:
        with app.open_resource('test.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


@app.before_first_request
def first_request():
    init_db()
'''