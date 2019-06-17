import time

from flask import Blueprint, render_template, sessions, session, Response, request, redirect
from .VerfiCode import VerfiCode
from App.model import *
import hashlib
import re

bbs=Blueprint('bbs',__name__)

# @bbs.route('/')
# def index():
#     return render_template('index.html')
@bbs.route('/')
@bbs.route('/<int:cid>')
@bbs.route('/<int:cid>/<int:xid>')#php技术交流/程序人生
def index (cid=0,xid=0):
    name=request.args.get('username')
    mm=request.args.get('password')
    user=User.query.filter(User.username==name).all()

    md5_obj = hashlib.md5()
    md5_obj.update(str(mm).encode('utf-8'))
    passwd = md5_obj.hexdigest()

    if passwd:
        if len(user)!=0:
            if user[0].password==passwd:
                session['username'] = name

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

@bbs.route('/quit')
def quit():
    session.clear()
    return redirect('/')

@bbs.route('/yzm')
def yzm():
    vc= VerfiCode()
    res = vc.output()
    session['yzm']=vc.code
    response = Response()
    response.status_code = 200
    response.headers['content-type']='image/jpeg'
    response.data = res
    return response


@bbs.route('/register')
def zhuce():
    return render_template('zhuce.html')


@bbs.route('/yanzheng',methods=['GET','POST'])
def yanzheng():
    name=request.form.get('username')
    mm = request.form.get('password')
    mn = request.form.get('repassword')

    md5_obj = hashlib.md5()
    md5_obj.update(str(mm).encode('utf-8'))
    passwd = md5_obj.hexdigest()


    email=request.form.get('mail')
    yzm=request.form.get('yzm')
    na=User.query.filter(User.username==str(name)).all()
    ml=re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',str(email))
    yz=session.get('yzm')

    list=[]
    if len(na)!=0:
        list.append("用户名重复")
    if len(str(name))<3 or len(str(name))>12:
        list.append('用户长度不符合要求')
    if mm != mn:
        list.append("两次输入密码不一致")
    else:
        if len(str(mm))<3 or len(str(mm))>12:
            list.append('密码长度不符合要求')
    if not ml:
        list.append('邮箱格式错误')
    if yz!=yzm:
        list.append("验证码错误")
    length=len(list)
    if length==0 :
        user=User()
        user.username=name
        user.password=passwd
        user.email=email
        user.regtime= time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        user.lasttime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        user.regip= 1
        user.allowlogin = 0
        db.session.add(user)
        db.session.commit()
    session['zhuce']=1
    for n in range(length):
        print(list[n])
    # print(yzm)
    # print(yz)
    # print(mm)
    # print(mn)
    print(length)


    return render_template('notice.html',**{
        'li':list,
        'len':length
    })






    # return render_template('zhuce.html')

@bbs.route('/getpass')
def getpass():
    return render_template('getpass.html')

@bbs.route('/reyanzheng',methods=['GET','POST'])
def reyanzheng():
    name=request.form.get('username')
    email=request.form.get('mail')
    na = User.query.filter(User.username == str(name)).all()
    yzm = request.form.get('yzm')
    yz = session.get('yzm')
    res = User.query.filter(User.username == str(name), User.email == str(email)).first()
    title = ""
    n=0
    if res:
        if yz ==yzm:
            title = "找回密码成功，已发送到您的邮箱"
            n=1
        else:
            title = '验证码输入错误'
    else:
        title = "查询不到用户信息，请查看输入是否有误"
        n=0

    return render_template('notice1.html',**{
        'speak':title,
        'num':n
    })
    # list=[]
    # n=0
    # length=len(list)
    # if len(na)!=0:
    #    if na[0].email == str(email):
    #        if yz==yzm:
    #            n=1
    #            list.append('您的密码已经发送到您的邮箱，请及时查看。')
    #        else:
    #            list.append("验证码错误")
    #    else:
    #         list.append('邮箱输入错误')
    # else:
    #     list.append('无此用户')
    # for n in range(n):
    #     print(list[n])
    # return render_template('notice1.html',**{
    #     'li':list,
    #     'num':n,
    #     'len':length
    # })