# web框架

## app
* models.py 数据库
* static 资源
* templates html页面

## migrations
数据库迁移
+ python manage.py db init 创建迁移仓库
+ python manage.py db migrate -m "initial migration" 创建迁移脚步
+ python manage.py db upgrade 迁移

## requirements
依赖包
- common.txt 公共依赖包
- dev.txt 开发环境 pip install -r dev.txt
- prod.txt 生产环境 pip install -r prod.txt

## tests
单元测试

## config.py
配置文件

## manage.py
启动文件

