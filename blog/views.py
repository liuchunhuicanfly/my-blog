# -*- coding: utf-8 -*-

from flask import render_template, request, url_for, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user

from blog import app, db
from blog.models import User, Movie


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
			flash('Invalid input.')
			return redirect(url_for('index'))

		movie = Movie(title = title, year = year)
		db.session.add(movie)
		db.session.commit()
		flash('Item created.')
		return redirect(url_for('index'))

	movies = Movie.query.all()
	return render_template('blog/index.html', active_page = 'home', movies = movies)


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
			flash('Invalid input.')
			return redirect(url_for('movie_edit', movie_id = movie_id))

		movie.title = title
		movie.year = year

		db.session.commit()
		flash('Edit item.')
		return redirect(url_for('index'))

	return render_template('blog/edit.html', active_page = 'about', movie = movie)

@app.route('/movie/delete/<int:movie_id>', methods = ['POST'])
@login_required # 用于视图保护
def movie_delete(movie_id):
	movie = Movie.query.get_or_404(movie_id)
	db.session.delete(movie)
	db.session.commit()
	flash('Delete item.')
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


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		if not username or not password:
			flash('Invalid input.')
			return redirect(url_for('login'))

		user = User.query.first()

		if username == user.username and user.validate_password(password):
			login_user(user)
			flash('Login Success.')
			return redirect(url_for('index'))

		flash('Invalid username or password.')
		return redirect(url_for('login'))

	return render_template('auth/login.html')

@app.route('/logout')
@login_required # 用于视图保护
def logout():
	logout_user() # 登出用户
	flash('has logout.')
	return redirect(url_for('index'))