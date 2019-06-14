from flask import Flask
from flask_script import Manager
from ext import db

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SECRET_KEY'] = '123'
manager=Manager(app)

from App.view import bbs
app.register_blueprint(bbs)


app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@127.0.0.1:3306/bbs"
db.init_app(app)
manager=Manager(app)

if __name__ == '__main__':
    manager.run()
