# -*- coding:utf-8 -*-

# 导入flask
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('blog/index.html')