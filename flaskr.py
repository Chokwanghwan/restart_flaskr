import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort,\
                  render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
	DATABASE = os.path.join(app.root_path, 'flaskr.db'),
	DEBUG = True,
	SECRET_KEY = 'developement key',
	USERNAME = 'admin',
	PASSWORD = 'dafault'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
	rv = sqlite3.connect(app.config['DATABASE'])
	rv.row_factory = sqlite3.Row
	return rv

def get_db():
	if not hasattr(g, 'sqlite_db'):
		g.sqlite_db = connect_db()
		return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

def init_db():
	with app.app_context():
		db = get_db()
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()
@app.route('/')
def show_entries():
	db = get_db()
	cur = db.execute('select title, text from entries order by id desc')
	entries = cur.fetchall()
	return render_template('show_entries.html')		

@app.route('/add', methods=['POST'])
def add_entry():
	if not session.get('logged_in'):
		abort(401)
	db = get_db()
	db.execute('insert into entries (title, text) value (?, ?)',
		       [request.form['title'], request.form['text']])
	db.commit()
	flash('New entry was successfully posted')
	return redirect(url_for('show_entries'))

if __name__ == '__main__':
	app.run()














