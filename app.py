from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import oprateDB

app = Flask(__name__)
app.secret_key = 'xxx'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:25574201Abc/@127.0.0.1:3306/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
app.config['JSON_AS_ASCII'] = False


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    gender = db.Column(db.Enum("男", "女"), nullable=False)
    phone = db.Column(db.String(11))
    e_mail = db.Column(db.String(30))
    contents = db.relationship("Content", backref="user")


class Content(db.Model):
    __tablename__ = "content"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    content_information = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


db.create_all()
#  db.drop_all()


@app.route('/login', methods=['GET', 'POST'])  # 登录界面
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.form['submit_button'] == 'register':
        return redirect('/register')
    else:
        user = request.form.get('username')
        pwd = request.form.get('pwd')
        if oprateDB.find_pwd(user, pwd):
            session['user_info'] = user
            return redirect('/show_blog')
        else:
            return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])  # 注册界面
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = request.form.get('username')
    pwd = request.form.get('pwd')
    gender = request.form.get('gender')
    phone = request.form.get('phone')
    e_mail = request.form.get('e_mail')
    oprateDB.Add_user(user, pwd, gender, phone, e_mail)
    return redirect('/login')


@app.route('/write_content', methods=['GET', 'POST'])  # 写博客界面
def write_content():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('write_content.html')
    title = request.form.get('title')
    contents = request.form.get('contents')
    oprateDB.Add_content(title, contents, oprateDB.find_id(user_info))
    return redirect('/show_blog')


@app.route('/show_title', methods=['GET', 'POST'])  # 展示个人blog标题界面
def show_title():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    t = oprateDB.find_title(oprateDB.find_id(user_info))
    i = oprateDB.find_blog_id(oprateDB.find_id(user_info))
    r = dict(zip(i, t))
    return render_template('show_title.html', title_infomation=r)


@app.route('/show_content/<title_id>', methods=['GET', 'POST'])  # 展示blog内容界面
def show_content(title_id):
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    all_b = oprateDB.find_blog_all(title_id)
    if request.method == 'GET':
        return render_template('read_content.html', title=all_b.title, content=all_b.content_information)
    if request.form['submit_btn'] == 'SAVE':  # 修改保存
        title = request.form.get('title')
        contents = request.form.get('contents')
        oprateDB.chang_blog_all(title_id, title, contents)
        return render_template('read_content.html', title=all_b.title, content=all_b.content_information)
    elif request.form['submit_btn'] == 'DEL':  # 删除
        oprateDB.del_blog(title_id)
        return redirect('/show_title')


@app.route('/show_blog')
def show_blog():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    b = oprateDB.show_all_blog()
    return render_template('base_blog.html', blog=b)


@app.route('/base_show/<title_id>', methods=['GET', 'POST'])
def base_show(title_id):
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    print(title_id)
    all_b = oprateDB.find_blog_all(title_id)
    if request.method == 'GET':
        if oprateDB.find_id(user_info) == oprateDB.find_writer(title_id):
            return render_template('read_content.html', title=all_b.title, content=all_b.content_information)
        return render_template('common_show.html', title=all_b.title, content=all_b.content_information)
    if request.form['submit_btn'] == 'SAVE':  # 修改保存
        title = request.form.get('title')
        contents = request.form.get('contents')
        oprateDB.chang_blog_all(title_id, title, contents)
        return render_template('read_content.html', title=all_b.title, content=all_b.content_information)
    elif request.form['submit_btn'] == 'DEL':  # 删除
        oprateDB.del_blog(title_id)
        return redirect('/show_title')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


if __name__ == '__main__':
    app.run()
