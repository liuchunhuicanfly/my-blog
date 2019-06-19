# -*- coding:utf-8 -*-

import os
import sys
import click

# 导入flask
from flask import Flask, render_template, request
# 导入Flask-SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy

# 系统兼容性处理
WIN = sys.platform.startswith('win')
if WIN:
	prefix = 'sqlite:///'
else:
	prefix = 'sqlite:////'

# 创建Flask应用程序实例
# 需要传入__name__，作用是为了确定资源所在的路径
app = Flask(__name__)

#  配置数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

# 创建数据库模型
class User(db.Model): # 表名将会是 user（自动生成，小写处理）
	id = db.Column(db.Integer, primary_key = True) # 主键
	name = db.Column(db.String(20)) # 名字

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key = True) # 主键
	title = db.Column(db.String(60)) # 电影名
	year = db.Column(db.String(4)) # 年份

# 命令行初始化数据表
@app.cli.command()
# 设置选项
@click.option('--drop', is_flag = True, help = 'Create after drop')
def initdb(drop):
	"""Initialize the database."""
	if drop:
		db.drop_all()
	db.create_all()
	# 输出提示信息
	click.echo('Initialized database')

# 命令行创建数据表
@app.cli.command()
def forge():
	db.create_all()
	name = 'Richard'
	movies = [
		{'title': 'My Neighbor Totoro', 'year': '1988'},
		{'title': 'Dead Poets Society', 'year': '1989'},
		{'title': 'A Perfect World', 'year': '1993'},
		{'title': 'Leon', 'year': '1994'},
		{'title': 'Mahjong', 'year': '1996'},
		{'title': 'Swallowtail Butterfly', 'year': '1996'},
		{'title': 'King of Comedy', 'year': '1999'},
		{'title': 'Devils on the Doorstep', 'year': '1999'},
		{'title': 'WALL-E', 'year': '2008'},
		{'title': 'The Pork of Music', 'year': '2012'},
	]
	user = User(name=name)
	db.session.add(user)

	for m in movies:
		movie = Movie(title=m['title'], year=m['year'])
		db.session.add(movie)
	db.session.commit()
	# 输出提示信息
	click.echo('Done')

# 定义上下文参数
@app.context_processor
def inject_user():
	user = User.query.first()
	# 函数返回的变量（以字典键值对的形式）将会统一注入到每一个模板的上下文环境中，因此可以直接在模板中使用
	return dict(user = user)

# 404错误处理
# 传入要处理的错误代码
@app.errorhandler(404)
def page_not_found(e): # 接受异常对象作为参数
	print(type(e)) # class 'werkzeug.exceptions.NotFound'>
	return render_template('errors/404.html'), 404

# 定义路由及视图函数
@app.route('/')
def index():
	movies = Movie.query.all()
	return render_template('blog/index.html', movies = movies)








