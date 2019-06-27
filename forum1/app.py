import os
from flask import Flask
from flask_script import Manager
from ext import db,photos
from flask_uploads import configure_uploads,patch_request_class,IMAGES

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SECRET_KEY'] = '123'
manager=Manager(app)
app.config['MAX_CONTENT_LENGTH']=5*1024*1024
app.config['UPLOAD_FOLDER']=os.path.join(os.getcwd(),'static/upload')
app.config['UPLOADED_PHOTOS_DEST']=os.path.join(os.getcwd(),'static/upload')

configure_uploads(app,photos)
patch_request_class(app,size=None)


from App.view import bbs
app.register_blueprint(bbs)

from Admin.admin_view import admin
app.register_blueprint(admin)


app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:123456@127.0.0.1:3306/bbs"
db.init_app(app)
manager=Manager(app)

if __name__ == '__main__':
    manager.run()
