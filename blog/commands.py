# -*- coding: utf-8 -*-

import click

from blog import app, db
from blog.models import User, Movie



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
		click.echo('Update admin...')
		user.username = username
		user.set_password(password)
	else:
		click.echo('Create admin...')
		user = User(username = username, name = 'Admin')
		user.set_password(password)
		db.session.add(user)
	db.session.commit()
	click.echo('Done')
