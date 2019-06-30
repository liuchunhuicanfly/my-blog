# -*- coding: utf-8 -*-

import unittest

from blog import app, db
from blog.models import User, Movie
from blog.commands import forge, initdb

class BlogTestCase(unittest.TestCase):

	def setUp(self):
		# 更新配置
		app.config.update(
			TESTING = True,
			SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
		)

		# 创建数据库和表
		db.create_all()

		# 创建测试数据
		user = User(name = 'Test1', username = 'test1')
		user.set_password('123456')
		movie = Movie(title = 'Test Movie Title', year = '2019')
		# 使用add_all()方法一次添加多个模型类实例，传入列表
		db.session.add_all([user, movie])
		db.session.commit()

		# 创建测试客户端
		self.client = app.test_client()
		# 创建测试命令运行器
		self.runner = app.test_cli_runner()


	def tearDown(self):
		# 清除数据库会话
		db.session.remove()
		# 删除数据表
		db.drop_all()


	def test_app_exist(self):
		self.assertIsNotNone(app)


	def test_app_is_testing(self):
		self.assertTrue(app.config['TESTING'])


	# 测试404页面
	def test_404_page(self):
		# 传入目标URL
		response = self.client.get('/nothing')
		# 获取Unicode格式的响应主体
		data = response.get_data(as_text = True)
		# 判断响应主体中是否包含预期的内容
		self.assertIn('Page Not Found - 404', data)
		self.assertIn('Go Back', data)
		# 判断响应状态码
		self.assertEqual(response.status_code, 404)


	# 测试主页面
	def test_index_page(self):
		response = self.client.get('/')
		data = response.get_data(as_text = True)
		self.assertIn('Test Movie Title', data)
		self.assertEqual(response.status_code, 200)


	# 辅助方法，用于登录用户
	def login(self):
		self.client.post('/login', data = dict(
				username = 'test1',
				password = '123456'
			), follow_redirects = True) # 设置follow_redirects参数为True可以跟随重定向，最终返回的是重定向后的响应


	# 测试创建条目数
	def test_create_item(self):
		self.login()

		# 测试创建条目操作
		response = self.client.post('/', data = dict(
				title = 'A new movie title',
				year = '2019'
			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertIn('Item created.', data)
		self.assertIn('A new movie title', data)


		# 测试创建条目操作，但电影标题为空
		response = self.client.post('/', data = dict(
				title = '',
				year = '2019'
			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertNotIn('Item created.', data)
		self.assertIn('Invalid input.', data)

		# 测试创建条目操作，但电影年份为空
		response = self.client.post('/', data = dict(
				title = 'new Movie',
				year = ''
			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertNotIn('Item created.', data)
		self.assertIn('Invalid input.', data)


	# 测试更新条目
	def test_update_item(self):
		self.login()

		# 测试更新页面
		response = self.client.get('/movie/edit/1')
		data = response.get_data(as_text = True)
		self.assertIn('Test Movie Title', data)
		self.assertIn('2019', data)

		# 测试更新操作
		response = self.client.post('/movie/edit/1', data = dict(
				title = 'Update Test Title',
				year = '2019'
			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertIn('Edit item.', data)
		self.assertIn('Update Test Title', data)


	# 测试删除条目
	def test_delete_item(self):
		self.login()

		response = self.client.post('/movie/delete/1', follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertIn('Delete item.', data)
		self.assertNotIn('Test Movie Title', data)


	# 测试登录保护
	def test_login_protect(self):
		response = self.client.get('/')
		data = response.get_data(as_text = True)
		self.assertNotIn('Logout', data)
		self.assertNotIn('Settings', data)
		self.assertNotIn('<form method="post">', data)
		self.assertNotIn('Edit', data)
		self.assertNotIn('Delete', data)


	# 测试登录
	def test_login(self):
		response = self.client.post('/login', data = dict(
				username = 'test1',
				password = '123456'

			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertIn('Login Success.', data)
		self.assertIn('Logout', data)
		self.assertIn('Settings', data)
		self.assertIn('<form method="post">', data)
		self.assertIn('Edit', data)
		self.assertIn('Delete', data)

		# 测试使用错误的密码登录
		response = self.client.post('/login', data = dict(
				username = 'test1',
				password = '456'

			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertNotIn('Login Success.', data)
		self.assertIn('Invalid username or password.', data)

		# 测试使用错误的账户名
		response = self.client.post('/login', data = dict(
				username = 'test12143',
				password = '123456'
			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertNotIn('Login Success.', data)
		self.assertIn('Invalid username or password.', data)

		# 测试使用空密码
		response = self.client.post('/login', data = dict(
				username = 'test12143',
				password = ''
			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertNotIn('Login Success.', data)
		self.assertIn('Invalid input.', data)

		# 测试使用空账户名
		response = self.client.post('/login', data = dict(
				username = '',
				password = '123456'
			), follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertNotIn('Login Success.', data)
		self.assertIn('Invalid input.', data)


	# 测试登出
	def test_logout(self):
		self.login()

		response = self.client.get('/logout', follow_redirects = True)
		data = response.get_data(as_text = True)
		self.assertIn('has logout.', data)
		self.assertNotIn('Logout', data)
		self.assertNotIn('Settings', data)
		self.assertNotIn('<form method="post">', data)
		self.assertNotIn('Edit', data)
		self.assertNotIn('Delete', data)


	# -- 测试自定义命令行命令 --
	
	# 测试虚拟数据
	def test_forge_command(self):
		result = self.runner.invoke(forge)
		self.assertIn('Done', result.output)
		self.assertNotEqual(Movie.query.count(), 0)


	# 测试初始化数据库
	def test_initdb_command(self):
		result = self.runner.invoke(initdb)
		self.assertIn('Initialized database', result.output)


	# 测试创建admin
	def test_create_admin(self):
		db.drop_all()
		db.create_all()
		result = self.runner.invoke(args = ['admin', '--username', 'test2', '--password', '123456'])
		self.assertIn('Create admin...', result.output)
		self.assertIn('Done', result.output)
		self.assertEqual(User.query.count(), 1)
		self.assertEqual(User.query.first().username, 'test2')
		self.assertTrue(User.query.first().validate_password('123456'))


	# 测试更新admin
	def test_update_admin(self):
		result = self.runner.invoke(args = ['admin', '--username', 'test3', '--password', '12345678'])
		self.assertIn('Update admin...', result.output)
		self.assertIn('Done', result.output)
		self.assertEqual(User.query.first().username, 'test3')
		self.assertTrue(User.query.first().validate_password('12345678'))

if __name__ == '__main__':
	unittest.main()
















