# django_online_org
 - python == '2.7.10' 
 - django == '1.9.8' #由于xadmin不支持2.0以上版本
 - xadmin == '0.5.0' #用于替换原生后台，样式与功能得以提升
 - django-pure-pagination  #用于django换页功能，此插件比原生更容易定义逻辑
 - django-simple-captcha #用于登录时验证码插件
 - Mysql 
## 功能 
#### 功能介绍如图：
    ![image](https://github.com/koeelio/django_online_org/blob/master/media/WechatIMG5097.jpeg)
## 项目遇坑 
####  django.db.utils.OperationalError: (1060, "Duplicate column name

在做model设置外键时由于多设置一个default参数。做了makemigration后报错。一直找不到原因。
卡住很久
如果遇到这个报错，需要先找到生成表的app下的migrations文档下的py文件，该文件是记录每次变更表格的记录，
因为migration每次都会先遍历文件里的所有记录再生成新的数据表。
所以只要到出错的那次记录，把对应生成的py文件删除就可以了。
如果实在不行就把所有表格删掉，再drop掉mysql里的对应数据表，重新生成。但愿永远不会用到这种方法！


#### django.core.context_processors is deprecated in favor of django.template.context_processors.
  __import__(name)
  
遇到关于template的报错，使用chrome的DevTool，观察Console报错。确定bug位置，由于ajax不熟练，遇到不少次js代码报错！


#### 部署需要设置static路径
部署上线时需要在setting中添加STATIC_ROOT路径。
#### xadmin
使用xadmin注册model时，需要重新自定义一个文件用于注册xadmin。注册方式与django的注册后台数据是类似的。可根据指定的参数定义后台样式，头部信息，页尾信息。
#### 上传文件。
 需要先定义一个接受的文件夹，并在setting中配置media的路径。让django记录上传的路径，跟template和static的原理相识。这是功能不同
#### model向外键取值
 会用到一个set_xxx__的方法
#### 邮件功能
 django是自带邮件功能的，这点不需要用第三方插件，但是需要自定义生成一些验证信息就需要自己编写逻辑。
 以下这段是在网上找到的验证码生成函数：

``` 
def random_str(random_length=8):
    str_code = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str_code += chars[random.randint(0, length)]
    return str_code
    
 ```
 
 #### 表单
 djang自带是有form模块的，如果是form与定义的model是相同字段的，可以用到modelform， 非常方便
 
 #### url
 用到include 这个方法一定要使用namespace参数，不然找对应的url非常麻烦
 
 
