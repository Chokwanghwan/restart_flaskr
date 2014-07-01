import os
import sqlite3
from flask import Flask, g

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
def close_db():
	if hasattr(g, 'sqlite_db'):
		g.sqlite_db.close()

if __name__ == '__main__':
	app.run()