from flask import Blueprint, render_template, sessions, session, Response
from .VerfiCode import VerfiCode
from App.model import Category

bbs=Blueprint('bbs',__name__)

# @bbs.route('/')
# def index():
#     return render_template('index.html')
@bbs.route('/')
@bbs.route('/<int:cid>')
@bbs.route('/<int:cid>/<int:xid>')#php技术交流/程序人生
def index (cid=0,xid=0):
    if xid == 0:
        if cid == 0:
            bz = Category.query.filter(Category.parentid == cid).all()
        else:
            bz = Category.query.filter(Category.cid == cid).all()
        # 所有大版块
        allBk = Category.query.filter(Category.parentid == 0).all()
        # 小版块
        smallbz = Category.query.filter(Category.parentid != 0).all()
        return render_template('index.html', **{
            'category': bz,
            'allBk': allBk,
            'smalls': smallbz,
            'iid':cid,
            'id':xid
        })
    else :

        allBK = Category.query.filter(Category.parentid == 0).all()
        smallbz = Category.query.filter(Category.parentid != 0).all()
        BK = Category.query.filter(Category.parentid == cid).all() #allBK
        data = Category.query.filter(Category.cid==xid).all()
        # for n in range(3):
        #     print(allBK[n].classname)
        list=[]
        for ank in allBK:
            if ank.cid == cid:
                list.append(ank)
                for ak in smallbz:
                    if ak.cid == xid:
                        list.append(ak)
        return render_template('index.html',**{
            'allBk': allBK,
            'smalls': smallbz,
            'bk':BK,
            'da':data,
            'iid':cid,
            'id':xid,
            'li':list
        })





@bbs.route('/set')
def set_session():
    session['username']='admin'
    return 'session'




@bbs.route('/yanzhengma')
def yzm():
    vc= VerfiCode()
    res = vc.output()
    session['yzm']=vc.code
    response = Response()
    response.status_code = 200
    response.headers['content-type']='image/jpeg'
    response.data = res
    return response

@bbs.route('/showyzm')
def show_yzm():
    return render_template('yzm.html')

@bbs.route('/check')
def check_yzm():
    pass