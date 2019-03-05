from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
# from django.contrib.contenttypes.models import ContentType
# from django.core.exceptions import ObjectDoesNotExist
# from read_statistics.models import ReadNum
from DjangoUeditor.models import UEditorField  # 头部增加这行代码导入UEditorField
from read_statistics.models import ReadNumExpandMthod


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMthod):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(
        BlogType, on_delete=models.DO_NOTHING)
    # content = models.TextField()
    content = UEditorField(width=800, height=500,
                           toolbars="full", imagePath="upimg/", filePath="upfile/",
                           upload_settings={"imageMaxSize": 1204000},
                           settings={}, command=None, blank=True
                           )
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    readed_num = models.IntegerField(default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    read_details = GenericRelation(ReadDetail)

    def __str__(self):
        return "<Blog: %s>" % self.title

    # 设置信息
    class Meta:
        # 排序
        ordering = ['-created_time']
