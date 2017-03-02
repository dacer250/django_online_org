# django_test
django_test

##项目遇坑
####  django.db.utils.OperationalError: (1060, "Duplicate column name

在做model设置外键时由于多设置一个default参数。做了makemigration后报错。一直找不到原因。
卡住很久
如果遇到这个报错，需要先找到生成表的app下的migrations文档下的py文件，该文件是记录每次变更表格的记录，
因为migration每次都会先遍历文件里的所有记录再生成新的数据表。
所以只要到出错的那次记录，把对应生成的py文件删除就可以了。
如果实在不行就把所有表格删掉，再drop掉mysql里的对应数据表，重新生成。但愿永远不会用到这种方法！