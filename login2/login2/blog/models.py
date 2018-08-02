from django.db import models
from django.contrib.auth.models import User


class Anthology(models.Model):
    class Meta:#元选项
        ordering = ['-last_updated', 'date_created']
        verbose_name = '文集'
        verbose_name_plural = verbose_name
    """文集"""
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    name = models.CharField('名称', max_length=30, null=False)
    last_updated = models.DateTimeField('最后更新时间', auto_now=True)
    date_created = models.DateTimeField('创建时间', auto_now_add=True)


class Article(models.Model):
    """文章"""
    title = models.CharField('标题', max_length=30, null=False)
    content = models.TextField('内容', null=False)
    anthology = models.ForeignKey(Anthology, on_delete=models.CASCADE,default=1)
    last_updated = models.DateTimeField('最后更新时间', auto_now=True)
    date_created = models.DateTimeField('创建时间', auto_now_add=True)
    def __str__(self):
        return "ID: %s, 标题：%s"  % (self.id, self.title)

