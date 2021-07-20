from flask import Flask, render_template, request, redirect, session, jsonify
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


@app.route('/login', methods=['GET', 'POST'])
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
            return redirect('/content')
        else:
            return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
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


@app.route('/content', methods=['GET', 'POST'])
def content():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('write_content.html')
    title = request.form.get('title')
    contents = request.form.get('contents')
    oprateDB.Add_content(title, contents, oprateDB.find_id(user_info))
    return render_template('write_content.html')


@app.route('/show')
def show():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/login')
    t = oprateDB.find_title(oprateDB.find_id(user_info))
    c = oprateDB.find_content(oprateDB.find_id(user_info))
    print(oprateDB.find_blog_id(oprateDB.find_id(user_info)))
    return jsonify(c)


if __name__ == '__main__':
    app.run()
