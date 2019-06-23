# -*- coding:utf-8 -*-

import os
import sys
import click

# 导入flask
from flask import Flask, render_template, request, flash, redirect, url_for
# 导入Werkzeug
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
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
login_manager = LoginManager(app) # 实例化拓展类

login_manager.login_view = 'login'

#  配置数据库连接地址
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
# 关闭对模型修改的监控
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev'


# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

# 创建数据库模型
class User(db.Model, UserMixin): # 表名将会是 user（自动生成，小写处理）
	id = db.Column(db.Integer, primary_key = True) # 主键
	name = db.Column(db.String(20)) # 名字
	username = db.Column(db.String(20))
	password_hash = db.Column(db.String(128)) # 密码散列值

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def validate_password(self, password):
		return check_password_hash(self.password_hash, password)

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

@app.cli.command()
@click.option('--username', prompt = True, help = 'The username used to login.')
@click.option('--password', prompt = True, hide_input = True, confirmation_prompt = True, help = 'The password used to login.')
def admin(username, password):
	""" Create User """
	db.create_all()

	user = User.query.first()

	if user is not None:
		user.username = username
		user.set_password(password)
	else:
		user = User(username = username, name = 'Admin')
		user.set_password(password)
		db.session.add(user)
	db.session.commit()
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
@app.route('/', methods = ['GET', 'POST'])
def index():

	if request.method == 'POST':
		print(current_user.is_authenticated)
		if not current_user.is_authenticated: # 如果当前用户未认证
			return redirect(url_for('index'))
		# 获取表单信息
		title = request.form.get('title')
		year = request.form.get('year')

		if not title or not year or len(year) > 4 or len(title) > 60:
			flash('Invoid input')
			return redirect(url_for('index'))

		movie = Movie(title = title, year = year)
		db.session.add(movie)
		db.session.commit()
		flash('Success')
		return redirect(url_for('index'))

	movies = Movie.query.all()
	return render_template('blog/index.html', active_page = 'home', movies = movies)

@login_manager.user_loader
def load_user(user_id): # 创建用户加载回调函数，接受用户ID 作为参数
	user = User.query.get(int(user_id)) # 用ID作为User 模型的主键查询对应的用户
	return user # 返回用户对象

@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if not username or not password:
			flash('Invalid input')
			return redirect(usr_for('login'))

		user = User.query.first()


		if username == user.username and user.validate_password(password):
			print('验证成功')
			login_user(user)
			flash('Login Success')
			return redirect(url_for('index'))

		flash('Invalid username or password')
		return redirect(url_for('login'))

	return render_template('auth/login.html')

@app.route('/logout')
@login_required # 用于视图保护
def logout():
	logout_user() # 登出用户
	flash('Goodbye')
	return redirect(url_for('index'))


@app.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
	if request.method == 'POST':
		name = request.form['name']

		if not name or len(name) > 20:
			flash('Invalid input')
			return redirect(url_for('settings'))

		current_user.name = name
		db.session.commit()
		flash('settings update')
		return redirect(url_for('index'))

	return render_template('auth/settings.html')

@app.route('/about')
def about():
	return render_template('blog/about.html', active_page = 'about')

@app.route('/movie/edit/<int:movie_id>', methods = ['GET', 'POST'])
@login_required # 用于视图保护
def movie_edit(movie_id):
	movie = Movie.query.get_or_404(movie_id)

	if request.method == 'POST':
		title = request.form['title']
		year = request.form['year']

		if not title or not year or len(year) > 4 or len(title) > 60: 
			flash('Invoid input')
			return redirect(url_for('movie_edit', movie_id = movie_id))

		movie.title = title
		movie.year = year

		db.session.commit()
		flash('Success')
		return redirect(url_for('index'))

	return render_template('blog/edit.html', active_page = 'about', movie = movie)

@app.route('/movie/delete/<int:movie_id>', methods = ['POST'])
@login_required # 用于视图保护
def movie_delete(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	db.session.delete(movie)
	db.session.commit()
	flash('Delete Success')
	return redirect(url_for('index'))








