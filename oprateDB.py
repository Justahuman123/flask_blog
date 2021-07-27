import app


def Add_user(use, pwd, gen, pho, ema):  # 用户注册
    u = app.User(username=use, password=pwd, gender=gen, phone=pho, e_mail=ema)
    app.db.session.add(u)
    app.db.session.commit()


def find_pwd(use, pwd):  # 用户登录
    u = app.User.query.filter(app.User.username == use).first()
    if u is None:
        return False
    elif pwd == u.password:
        return True
    else:
        return False


def find_id(use):  # 获取用户id
    u = app.User.query.filter(app.User.username == use).first()
    return u.id


def Add_content(tit, con, i):  # 添加博客的内容
    c = app.Content(title=tit, content_information=con, user_id=i)
    app.db.session.add(c)
    app.db.session.commit()


def find_title(i):  # 根据用户id获取用户博客的标题
    t = app.User.query.get(i)
    list_title = []
    for i in t.contents:
        list_title.append(i.title)
    return list_title


def find_content(i):  # 根据用户id 获取用户微博的内容
    c = app.User.query.get(i)
    list_content = []
    for i in c.contents:
        list_content.append(i.content_information)
    return list_content


def find_blog_id(i):  # 根据用户id获取用户微博的id
    c = app.User.query.get(i)
    list_id = []
    for i in c.contents:
        list_id.append(i.id)
    return list_id


def find_blog_all(i):  # 根据文章id获取文章的全部内容
    c = app.Content.query.get(i)
    return c


def chang_blog_all(i, tit, con):
    app.Content.query.filter(app.Content.id == i).update({"title": tit, "content_information": con})
    app.db.session.commit()


def del_blog(i):
    app.Content.query.filter(app.Content.id == i).delete()
    app.db.session.commit()


def show_all_blog():
    c = app.Content.query.all()
    list_id = []
    list_title = []
    for i in c:
        list_id.append(i.id)
        list_title.append(i.title)
    b = dict(zip(list_id, list_title))
    return b


def find_writer(i):
    c = app.Content.query.filter(app.Content.id == i).first()
    return c.user_id
