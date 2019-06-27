import hashlib
import re

from flask import Blueprint, render_template, request, redirect, url_for, session
from .admin_model  import *

admin = Blueprint('admin',__name__,url_prefix='/admin')

# @admin.before_app_request
# def is_login():
#     if request.path.rstrip('/') == '/admin/login':
#         return None
#     if not session.get('username'):
#         return redirect(url_for('admin.login'))
@admin.route('/login/')
def login():

    return render_template('admin/admin_login.html')


@admin.route('/',methods=['GET','POST'])
def index():
    name = request.form.get('admin_username')
    password = request.form.get('admin_password')
    print(name,password)

    md5_obj = hashlib.md5()
    md5_obj.update(str(password).encode('utf-8'))
    passwd = md5_obj.hexdigest()
    session['password'] = passwd
    use = User.query.filter(User.username == name).first()
    print(use,"-------------------")
    if str(passwd) == str(use.password):
        session['username'] = name
        return  render_template('admin/admin_index.html')
    else:
        return redirect('/admin/login')

# 版块管理
# @admin.route('/category/',methods=["GET","POST"])
# def category():
#     # 大版块
#     bigs = Category.query.filter(Category.parentid == 0).order_by(Category.orderby).all()
#     # 小版块
#     smalls = Category.query.filter(Category.parentid != 0).order_by(Category.orderby).all()
#     # print(bigs, type(bigs[0]))
#     if request.method == 'POST':
#         for name in request.form:
#             record = request.form.getlist(name)
#             # 保存大版块信息
#             for big in bigs:
#                 # print(big.compere,type(big.compere))
#                 if int(record[0]) == big.id:
#                     # print(type(big.id), '---', type(record[1]))
#                     big.classname = record[2]
#                     big.orderby = record[1]
#                     big.save()
#                     # print(big)
#                     break
#             # 保存小版块信息
#             for small in smalls:
#                 if int(record[0]) == small.id:
#                     small.orderby = record[1]
#                     small.classname = record[2]
#                     small.compere = record[3]
#                     small.save()
#                     break
#     bigs.sort(key=lambda elem:elem.orderby)
#     smalls.sort(key=lambda elem:elem.orderby)
#     #get
#     return render_template('admin/admin_category.html', **{
#         'title': '版块管理',
#         'bigs': bigs,
#         'smalls': smalls
#     })
#
# @admin.route('/member/')
# def member():
#     return  render_template('admin/admin_member.html')
@admin.route('/detail/',methods=['GET','POST'])
def detail():
    if request.method == 'POST':
        jiashanchu = request.form.getlist('tid')
        for i in jiashanchu:
            tiezi=Detail_t.query.filter(Detail_t.id==int(i)).first()
            print(tiezi.id)
            tiezi.isdel=1
            db.session.add(tiezi)
            db.session.commit()
        # print(data)
        # for tid in data:
        #     forum = Detail_t.query.get(tid)
        #     if forum.isdel == 0:
        #         forum.isdel = 1
        #         forum.save()
    page = int(request.args.get('page',1))
    data = db.session.query(Detail_t.id,Detail_t.title,User.username,Detail_t.replycount,Detail_t.hits,Detail_t.addtime,Category.classname,Category.cid,Category.parentid).filter(User.uid==Detail_t.authorid,Detail_t.classid==Category.cid,Detail_t.isdel==0).paginate(page,100)
    print(data.items)
    num=len(data.items)
    # pagination = Detail_t.query.filter(Detail_t.isdel==0).paginate(page,15)
    return  render_template('admin/admin_detail.html',pagination=data,num=num)
    # return  "hello"

@admin.route('/deletepost/',methods=['GET','POST'])
def deletepost():
    shanchu=request.form.get('delsubmit')
    huifu=request.form.get('undelsubmit')
    if request.method == 'POST':
        jiashanchu = request.form.getlist('tid')
        if huifu:
            for i in jiashanchu:
                tiezi=Detail_t.query.filter(Detail_t.id==int(i)).first()
                tiezi.isdel=0
                db.session.add(tiezi)
                db.session.commit()
        elif shanchu:
            for i in jiashanchu:
                tiezi=Detail_t.query.get(int(i))
                print(tiezi,"--------------------------------")
                db.session.delete(tiezi)
                db.session.commit()
        # print(data)
        # for tid in data:
        #     forum = Detail_t.query.get(tid)
        #     if forum.isdel == 0:
        #         forum.isdel = 1
        #         forum.save()
    page = int(request.args.get('page',1))
    data = db.session.query(Detail_t.id,Detail_t.title,User.username,Detail_t.replycount,Detail_t.hits,Detail_t.addtime,Category.classname,Category.cid,Category.parentid).filter(User.uid==Detail_t.authorid,Detail_t.classid==Category.cid,Detail_t.isdel==1).paginate(page,100)
    # print(data.items)
    num=len(data.items)
    return  render_template('admin/admin_detail_del.html',pagination=data,num=num)

@admin.route('/reply/')
def reply():
    return  render_template('admin/admin_detail_hf.html')


@admin.route('/site/')
def site():

    return  render_template('admin/admin_main.html')
@admin.route('/link/')
def link():
    link = Link.query.order_by(Link.displayorder).all()

    return  render_template('admin/admin_link.html',**{
        'link':link
    })
@admin.route('/linkcheck/',methods=['GET','POST'])
def linkcheck():
    delete=request.form.getlist('delete')
    displayorder=request.form.getlist('displayorder')
    name=request.form.getlist('name')
    url=request.form.getlist('url')
    description=request.form.getlist('description')
    logo=request.form.getlist('logo')
    lid=request.form.getlist('lid')
    xiugai=request.form.get('editlink')
    shanchu=request.form.get('dellink')
    tianjia=request.form.get('addlink')

    newdisplayorder=request.form.get('displayorder')
    newname=request.form.get('name')
    newurl=request.form.get('url')
    newdescription=request.form.get('description')
    newlogo=request.form.get('logo')

    n=0
    if xiugai:
        for i in lid:
            link=Link.query.filter(Link.lid==int(i)).first()
            link.displayorder = displayorder[n]
            link.name = name[n]
            link.url = url[n]
            link.description = description[n]
            link.logo = logo[n]
            db.session.add(link)
            db.session.commit()
            n=n+1
    elif shanchu:
        for i in delete:
            a=int(i)
            link = Link.query.get(a)
            db.session.delete(link)
            db.session.commit()

    elif tianjia:
        l=Link(
            displayorder=newdisplayorder,
            name=newname,
            url=newurl,
            description=newdescription,
            logo=newlogo
        )
        db.session.add(l)
        db.session.commit()
    return redirect('/admin/link')


# @admin.route('/lockip/')
# def lockip():
#     return  render_template('admin/admin_lock_ip.html')
# @admin.route('/addcategory/')
# def addcategory():
#     return  render_template('admin/admin_category_add.html')
#


# @admin.route('/recyle/')
# def recyle():
#     return  render_template('admin/admin_detail_hf_del.html')

@admin.route("/adminstrate/")
def adminstrate():



    return render_template('admin/admin_main.html')
@admin.route('/logout/')
def logout():
    return redirect('/admin/login')
#
# @admin.route('/dolink/')
# def dolink():
#     return  '退出登录'
