
# 注册蓝图
from flask import Flask

app = Flask(__name__)
app.debug = True

from app.home import home as home_blieprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blieprint)
app.register_blueprint(admin_blueprint, url_prefix="/admin")