from ext import db

class Category(db.Model):
    cid = db.Column(db.Integer,primary_key=True)
    classname = db.Column(db.String(60),nullable=False)
    parentid = db.Column(db.Integer,nullable=False)
    replycount = db.Column(db.Integer,nullable=False)
    compere = db.Column(db.String(10))
    description = db.Column(db.String(100))
    orderby = db.Column(db.Integer,nullable=False)
    lastpost = db.Column(db.String(600))
    namestyle = db.Column(db.String(10))
    ispass = db.Column(db.SmallInteger,nullable=False)
    classpic = db.Column(db.String(200))
    __tablename__ = 'bbs_category'

class User(db.Model):
    uid = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(16),nullable=False)
    password = db.Column(db.String(32),nullable=False)
    email = db.Column(db.String(30),nullable=False)
    udertype = db.Column(db.SmallInteger,nullable=False)
    regtime = db.Column(db.Integer,nullable=False)
    lasttime = db.Column(db.Integer,nullable=False)
    regip = db.Column(db.Integer,nullable=False)
    picture = db.Column(db.String(255),nullable=False)
    grade = db.Column(db.Integer)
    problem = db.Column(db.String(200))
    result = db.Column(db.String(200))
    realname = db.Column(db.String(50))
    sex = db.Column(db.SmallInteger)
    birthday = db.Column(db.String(20))
    place = db.Column(db.String(50))
    qq = db.Column(db.String(13))
    autograph = db.Column(db.String(500))
    allowlogin = db.Column(db.SmallInteger,nullable=False)
    __tablename__ = 'bbs_user'

# class Closeip(db.Model):
#     id =