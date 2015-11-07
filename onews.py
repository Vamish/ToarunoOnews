# -*- coding: utf-8 -*-
import os
from flask import Flask, render_template, session, request, redirect, url_for
from flask.ext.pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import date

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I AM A LOSER'
app.config['WTF_CSRF_ENABLED'] = False
app.config['UPLOAD_FOLDER'] = '/static/uploads/'

wd = os.path.dirname(__file__)

ALLOWED_IMG_EXTENSIONS = set(['jpg', 'png'])
mongo = PyMongo(app)


# 路由处理
@app.route('/')
def index():
    # 在这里面查询数据库,
    # 返回 OnewsList
    onewsList = mongo.db.onews.find().sort("time", -1)
    return render_template('index.html', onewsList=onewsList)


# 查看ONEWS - 查
@app.route('/onews/<oid>', methods=['GET'])
def get_news(oid):
    onews = mongo.db.onews.find_one_or_404({'_id': ObjectId(oid)})
    if 'view' in onews.keys():
        mongo.db.onews.update({'_id': ObjectId(oid)}, {'$inc': {'view': 1}})
    else:
        print('in')
        mongo.db.onews.update({'_id': ObjectId(oid)}, {'$set': {'view': 2}})
    return render_template('news.html', onews=onews)


# 删除ONEWS - 删
@app.route('/onews/<oid>', methods=['DELETE'])
def del_onews(oid):
    print(oid)
    mongo.db.onews.remove({'_id': ObjectId(oid)})


# 添加ONEWS - 增
@app.route('/onews', methods=['POST'])
def add_news():
    form = OnewsForm()
    if request.method == 'POST':
        # 接收到的字段值
        title = form.title.data
        title_img = request.files['title_img']
        content_img = request.files['content_img']
        news_type = form.news_type.data
        cpright = form.cpright.data
        cp_remark = form.cp_remark.data
        pub_time = form.pub_time.data

        # 上传图片处理
        title_img_set = create_file_dir(pub_time.replace('/', ''))
        dire = title_img_set['dire']
        filename = title_img_set['filename']
        if title_img and allowed_img_file(title_img.filename):
            if not os.path.exists(dire):
                os.mkdir(dire)
            title_filename = title_img.filename.replace(title_img.filename.rsplit('.', 1)[0], filename)
            title_img_path = os.path.join(dire, title_filename)
            title_img.save(title_img_path)
            print('头图上传成功')
        else:
            print('头图上传失败')

        if content_img and allowed_img_file(content_img.filename):
            content_filename = content_img.filename.replace(content_img.filename.rsplit('.', 1)[0], filename + 'c')
            content_img_path = os.path.join(dire, content_filename)
            content_img.save(content_img_path)
            print('内容图上传成功')
        else:
            print("内容图上传失败")

        onews = {"title": title,
                 "title_img": app.config['UPLOAD_FOLDER'] + filename + '/' + title_filename,
                 "content_img": app.config['UPLOAD_FOLDER'] + filename + '/' + content_filename,
                 "time": filename,
                 "type": news_type,
                 "is_authorized": cpright,
                 "cp_remark": cp_remark,
                 "view": 1}

        mongo.db.onews.insert(onews)

    return redirect(url_for('index'))


# 更新ONEWS - 改
@app.route('/onews/<oid>', methods=['POST'])
def upd_news(oid):
    form = OnewsForm()
    title = form.title.data
    news_type = form.news_type.data
    cpright = form.cpright.data
    cp_remark = form.cp_remark.data
    pub_time = form.pub_time.data

    # # 上传图片处理
    # title_img_set = create_file_dir(pub_time.replace('/', ''))
    # dire = title_img_set['dire']
    # filename = title_img_set['filename']
    # if title_img and allowed_img_file(title_img.filename):
    #     if not os.path.exists(dire):
    #         os.mkdir(dire)
    #     title_filename = title_img.filename.replace(title_img.filename.rsplit('.', 1)[0], filename)
    #     title_img_path = os.path.join(dire, title_filename)
    #     title_img.save(title_img_path)
    #     print('头图上传成功')
    # else:
    #     print('头图上传失败')
    #
    # if content_img and allowed_img_file(content_img.filename):
    #     content_filename = content_img.filename.replace(content_img.filename.rsplit('.', 1)[0], filename + 'c')
    #     content_img_path = os.path.join(dire, content_filename)
    #     content_img.save(content_img_path)
    #     print('内容图上传成功')
    # else:
    #     print("内容图上传失败")
    #
    onews = {"title": title,
             "time": pub_time,
             "type": news_type,
             "is_authorized": cpright,
             "cp_remark": cp_remark
             }

    mongo.db.onews.update({'_id': ObjectId(oid)}, {'$set': onews})

    return redirect(url_for('fun_upd_list'))


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard/dashboard.html')


# 菜单 - 新建
@app.route('/dashboard/add')
def fun_add():
    form = OnewsForm()
    return render_template('dashboard/add.html', form=form)


# 菜单 - 删除
@app.route('/dashboard/del')
def fun_del():
    onewsList = mongo.db.onews.find().sort("time", -1)
    return render_template('dashboard/del.html', onewsList=onewsList)


# 菜单 - 更新
@app.route('/dashboard/update')
def fun_upd_list():
    onewsList = mongo.db.onews.find().sort("time", -1)
    return render_template('dashboard/upd-list.html', onewsList=onewsList)


@app.route('/dashboard/update/<oid>')
def fun_upd(oid):
    onews = mongo.db.onews.find_one({'_id': ObjectId(oid)})
    form = OnewsForm()
    return render_template('dashboard/upd.html', form=form, onews=onews)


# 错误处理
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500


from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, FileField, SelectField
from wtforms.validators import Required


class OnewsForm(Form):
    title = StringField("标题：", validators=[Required()])
    title_img = FileField("标题图片：", validators=[Required()])
    content_img = FileField("内容图片：", validators=[Required()])
    news_type = SelectField("选择类型", choices=[('0', '普通内容'), ('1', '特殊内容'), ('2', '广告')])
    cpright = SelectField("版权信息", choices=[('0', '原创'), ('1', '授权转载')])
    pub_time = StringField()
    cp_remark = StringField()
    submit = SubmitField('提交')


def allowed_img_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_IMG_EXTENSIONS


def create_file_dir(t):
    if not t:
        d = date.today().strftime('%y%m%d')
    else:
        d = t
    dire = os.path.join(wd + app.config['UPLOAD_FOLDER'] + d)
    return {'dire': dire, 'filename': d}


if __name__ == '__main__':
    app.run(debug=True)
