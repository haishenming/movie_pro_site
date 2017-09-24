from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://movie:movie_pro@101.201.68.4:3306/flask_movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class User(db.Model):
    """ 会员 """
    __tablename__ = "user"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 姓名
    name = db.Column(db.String(64), unique=True)
    # 密码
    pwd = db.Column(db.String(64))
    # email
    email = db.Column(db.String(64), unique=True)
    # 电话
    phone = db.Column(db.String(11), unique=True)
    # 个人简介
    info = db.Column(db.Text)
    # 头像
    face = db.Column(db.String(128), unique=True)
    # 创建时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 用户ID，唯一标识符
    uuid = db.Column(db.String(128), unique=True)
    # 与会员登录日志的外键关系
    user_logs = db.relationship("UserLog", backref="user")
    # 与评论外键关联
    comments = db.relationship("Comment", backref="user")
    # 外键关联收藏
    moviecols = db.relationship("Moviecol", backref="user")

    def __repr__(self):
        return "<User {}>".format(self.name)


class UserLog(db.Model):
    """ 会员登录日志 """
    __tablename__ = "userlog"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 会员ID
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 登录IP
    ip = db.Column(db.String(64))
    # 登录时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<UserLog {}>".format(self.id)


class Tag(db.Model):
    """ 标签 """
    __tablename__ = "tag"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 名称
    name = db.Column(db.String(64), unique=True)
    # 创建时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 电影外键关系
    movies = db.relationship("Movie", backref="tag")

    def __repr__(self):
        return "<Tag {}>".format(self.name)


class Movie(db.Model):
    """ 电影 """
    __tablename__ = "movie"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(128), unique=True)
    # 地址
    url = db.Column(db.String(128), unique=True)
    # 简介
    info = db.Column(db.Text)
    # 封面
    logo = db.Column(db.String(128), unique=True)
    # 星级
    star = db.Column(db.SmallInteger)
    # 播放量
    playnum = db.Column(db.BigInteger)
    # 评论量
    commentnum = db.Column(db.BigInteger)
    # 标签
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"))
    # 地区
    area = db.Column(db.String(128))
    # 上映时间
    release_time = db.Column(db.Date)
    # 播放时间
    length = db.Column(db.String(64))
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 与评论外键关联
    comments = db.relationship("Comment", backref="movie")
    # 外键关联收藏
    moviecols = db.relationship("Moviecol", backref="movie")

    def __repr__(self):
        return "<Movie {}>".format(self.title)


class Preview(db.Model):
    """ 电影预告 """
    __tablename__ = "preview"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 标题
    title = db.Column(db.String(128), unique=True)
    # 封面
    logo = db.Column(db.String(128), unique=True)
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Preview {}>".format(self.title)


class Comment(db.Model):
    """ 评论 """
    __tablename__ = "comment"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 内容
    content = db.Column(db.Text)
    # 电影
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    # 评论用户
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 评论时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Comment {}>".format(self.id)


class Moviecol(db.Model):
    """ 电影收藏 """
    __tablename__ = "moviecol"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 电影
    movie_id = db.Column(db.Integer, db.ForeignKey("movie.id"))
    # 收藏用户
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 收藏时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Comment {}>".format(self.id)


class Auth(db.Model):
    """ 权限 """
    __tablename__ = "auth"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 权限名称
    name = db.Column(db.String(64), unique=True)
    # 权限路由
    url = db.Column(db.String(128), unique=True)
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Auth {}>".format(self.name)


class Role(db.Model):
    """ 角色 """
    __tablename__ = "role"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 角色名称
    name = db.Column(db.String(64), unique=True)
    # 权限列表
    auths = db.Column(db.String(600))
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Role {}>".format(self.name)


class Admin(db.Model):
    """ 管理员 """
    __tablename__ = "admin"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 管理员账号
    name = db.Column(db.String(64), unique=True)
    # 管理员
    pwd = db.Column(db.String(64))
    # 是否为超级管理员
    is_super = db.Column(db.SmallInteger)
    # 所属角色
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"))
    # 与管理员登录日志的外键关系
    adminlogs = db.relationship("AdminLog", backref="admin")
    # 与管理员操作日志的外键关系
    oplogs = db.relationship("OpLog", backref="admin")
    # 添加时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Admin {}>".format(self.name)


class AdminLog(db.Model):
    """ 管理员登录日志 """
    __tablename__ = "adminlog"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 会员ID
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    # 登录IP
    ip = db.Column(db.String(64))
    # 登录时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<AdminLog {}>".format(self.id)


class OpLog(db.Model):
    """ 管理员操作日志 """
    __tablename__ = "oplog"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 会员ID
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    # 登录IP
    ip = db.Column(db.String(64))
    # 操作原因
    reason = db.Column(db.Text)
    # 登录时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<OpLog {}>".format(self.id)

if __name__ == '__main__':
    # db.create_all()
    #
    role = Role(
        name="超级管理员",
        auths=""
    )
    db.session.add(role)
    db.session.commit()