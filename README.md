<h1 align="center">
	Flask 实战
</h1>

### 准备工作
创建项目目录
```
$ mkdir my-blog
$ cd my-blog
```

### 创建虚拟环境
虚拟环境是独立于 Python 全局环境的 Python 解释器环境，使用它的好处如下：
保持全局环境的干净
指定不同的依赖版本
方便记录和管理依赖

我们将使用 Pipenv 来创建和管理虚拟环境、以及在虚拟环境中安装和卸载依赖包。它集成了 pip 和 virtualenv，可以替代这两个工具的惯常用法。另外，它还集成了 Pipfile，它是新的依赖记录标准，使用 Pipfile 文件记录项目依赖，使用 Pipfile.lock 文件记录固定版本的依赖列表。这两个文件替代了手动通过 requirements.txt 文件记录依赖的方式
```
$ pip install pipenv
```

使用 Pipenv 创建虚拟环境非常简单，使用 pipenv install 命令即可为当前项目创建一个虚拟环境：
```
$ pipenv install
```
这个命令执行的过程包含下面的行为：
为当前目录创建一个 Python 解释器环境，按照 pip、setuptool、virtualenv 等工具库。
如果当前目录有 Pipfile 文件或 requirements.txt 文件，那么从中读取依赖列表并安装。
如果没有发现 Pipfile 文件，就自动创建。
创建虚拟环境后，我们可以使用 pipenv shell 命令来激活虚拟环境，如下所示（执行 exit 可以退出虚拟环境）：
```
$ pipenv shell
```
>**注意** 除了 pipenv install 命令和 Git 相关命令外，除非特别说明，后续的所有命令均需要在激活虚拟环境后执行。如果你不想每次都激活虚拟环境，可以在命令前添加 pipenv run 前缀，比如 pipenv run pip list 即表示在虚拟环境内执行 pip list 命令。

### 安装Flask
无论是否已经激活虚拟环境，你都可以使用下面的命令来安装 Flask：
```
$ pipenv install flask
```
这会把 Flask 以及相关的一些依赖包安装到对应的虚拟环境，同时 Pipenv 会自动更新依赖文件。

Flask 是典型的微框架，作为 Web 框架来说，它仅保留了核心功能：请求响应处理和模板渲染。这两类功能分别由 Werkzeug（WSGI 工具库）完成和 Jinja（模板渲染库）完成。

app.py: 程序主页
```
from flask import Flask 

app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello flask'
```

### Installation
```
$ git clone https://github.com/liuchunhuicanfly/my-blog
$ cd my-blog
$ pipenv install --dev
$ pipenv shell
$ flask forge
$ flask run
* Running on http://127.0.0.1:5000/

# 账号密码
richard
123456
```


>**参考**：
[watchList](https://github.com/greyli/watchlist)
[hello, flask](https://read.helloflask.com/)