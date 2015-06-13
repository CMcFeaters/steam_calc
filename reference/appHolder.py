'''this file will hold our app.  all other files will reference this
when they need to access the db'''

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


path="Users/Chuck/Documents/GitHub/setamProj/steamProj.db"
print(path)

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////'+path
db = SQLAlchemy(app)
app.config.from_envvar('FLASKR_SETTINGS',silent=True)
app.debug=True
CSRF_ENABLED=True
app.secret_key = 'development key'
	
