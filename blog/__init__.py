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

# SQLite系统兼容性处理
WIN = sys.platform.startwith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = 'sqlite:///'

# 创建Flask应用程序实例
# 需要传入__name__，作用是为了确定资源所在的路径
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')











