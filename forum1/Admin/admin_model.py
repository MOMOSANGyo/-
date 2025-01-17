from Admin.admin_ext import db

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

class Detail_t(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    tid = db.Column(db.Integer,nullable=False)
    authorid = db.Column(db.Integer,nullable=False)
    title = db.Column(db.String(600),nullable=False)
    content = db.Column(db.String(1000),nullable=False)
    addtime = db.Column(db.Integer,nullable=False)
    addip = db.Column(db.String(12),nullable=False)
    classid = db.Column(db.Integer,nullable=False)
    replycount = db.Column(db.Integer)
    hits = db.Column(db.Integer)
    lstop = db.Column(db.SmallInteger)
    elite = db.Column(db.SmallInteger)
    ishot = db.Column(db.SmallInteger)
    rate = db.Column(db.SmallInteger)
    attchment = db.Column(db.SmallInteger)
    isdel = db.Column(db.Integer)
    style = db.Column(db.String(10))
    Isdisplay = db.Column(db.Integer)
    __tablename__ = 'bbs_details_t'

class Link(db.Model):
    lid=db.Column(db.Integer,primary_key=True)
    displayorder=db.Column(db.SmallInteger)
    name=db.Column(db.String(30),nullable=False)
    url=db.Column(db.String(255),nullable=False)
    description=db.Column(db.String(255))
    logo=db.Column(db.String(255))
    addtime=db.Column(db.String(255))
    __tablename__ = 'bbs_link'

