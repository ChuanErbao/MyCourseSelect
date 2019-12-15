[![simpleui](https://img.shields.io/badge/developing%20with-Simpleui-2077ff.svg)](https://github.com/newpanjing/simpleui)
# MyCourseSelect
中国科学院大学高级软件工程课程设计

# 使用说明
```shell
# 克隆仓库
git clone git@github.com:ChuanErbao/MyCourseSelect.git
cd MyCourseSelect
pip install virtualenv
# 搭建虚拟环境
virtualenv --no-site-packages venv
# 激活虚拟环境
source venv/bin/activate
# 安装项目所需的包
pip install -r requirements.txt

# 数据库迁移
cd mysite/
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser

# 启动
python manage.py runserver

```
## url
用户:127.0.0.1:8000

管理员:127.0.0.1:8000/admin

