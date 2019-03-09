## 个人博客系统

### 1. 简单构建

​	![网站功能模块](C:\Users\ADMINI~1\AppData\Local\Temp\1551103346489.png)
### 2. `python manage.py shell`进入shell模式添加博客
```python
from blog.models import Blog
dir()
Blog.objects.all()
Blog.objects.count()
# Blog.objects.all().count()
blog = Blog()
dir()
blog.title = 'shell 下第1篇'
blog.content = 'aaaaaaaaa'
from blog.models import BlogType
BlogType.objects.all()
blog_type = BlogType.objects.all()[0]
blog.blog_type = blog_type
from django.contrib.auth.models import User
user = User.objects.all()[0]
blog.author = user
blog.save()
Blog.objects.all()

'''[summary]
    批量添加博客
[description]
'''
for i in range(1, 31):
    blog = Blog()
    blog.title = 'for %s' % i
    blog.content = '这是shell命令下的批量添加的博客：%s' % i
    blog.blog_type = blog_type
    blog.author = user
    blog.save()
```
### 3.django分页
```python
from django.core.paginator import Paginator
form blog.models import Blog

paginator = Paginator(blogs, 10)
dir(paginator)
```

### 4.django过滤filter

![1551533822532](C:\Users\ADMINI~1\AppData\Local\Temp\1551533822532.png)

### 5.评论的实现方式

![1551865941670](C:\Users\ADMINI~1\AppData\Local\Temp\1551865941670.png)