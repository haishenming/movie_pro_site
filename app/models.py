from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://movie:movie_pro@101.201.68.4:3306/flask_movie"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


class User(db.Model):
    """ 会员 """
    __tablename__ = "user"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 姓名
    name = db.Column(db.String(100), unique=True)
    # 密码
    pwd = db.Column(db.String(100))
    # email
    email = db.Column(db.String(100), unique=True)
    # 电话
    phone = db.Column(db.String(11), unique=True)
    # 个人简介
    info = db.Column(db.Text)
    # 头像
    face = db.Column(db.String(255), unique=True)
    # 创建时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # 用户ID，唯一标识符
    uuid = db.Column(db.String(255), unique=True)
    # 与会员登录日志的外键关系
    user_logs = db.relationship("UserLog", backref="user")

    def __repr__(self):
        return "<User {}>".format(self.name)


class UserLog(db.Model):
    """ 会员登录日志 """
    __table__ = "user_log"
    # 编号
    id = db.Column(db.Integer, primary_key=True)
    # 会员ID
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    # 登录IP
    ip = db.Column(db.String(100))
    # 登录时间
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<UserLog {}>".format(self.id)
