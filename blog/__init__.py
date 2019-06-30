# -*- coding: utf-8 -*-

# __init__.py 文件的作用是将文件夹变为一个Python模块,
# 在导入一个包时，实际上是导入了它的__init__.py文件。
# 可以在__init__.py文件中批量导入所需要的模块，而不再需要一个一个的导入

# 引入内建包
import os
import sys

# 引入flask
from flask import Flask
# 映入 flask_sqlalchemy
from flask_sqlalchemy  import SQLAlchemy
# 引入flask_login
from flask_login import LoginManager

# 系统兼容性处理
WIN = sys.platform.startswith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = 'sqlite:///'

# 创建Flask应用程序实例
# 需要传入__name__，作用是为了确定资源所在的路径
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
# 数据文件资源定位
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path + 'data.db')
# 关闭对数据模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 实例化拓展类
db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户ID 作为参数
	from blog.models import User
	user = User.query.get(int(user_id)) # 用ID作为User 模型的主键查询对应的用户
	return user # 返回用户对象

# 设置登录视图端点
login_manager.login_view = 'login'

# 定义上下文参数
@app.context_processor
def inject_user():
	from blog.models import User
	user = User.query.first()
	# 函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用
	return dict(user = user)


from blog import views, errors, commands










