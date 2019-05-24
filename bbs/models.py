import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.html import mark_safe
from markdown import markdown

class Question(models.Model):
    question_text = models.CharField('问题', max_length=200)
    # author = models.CharField(max_length=50, default="de8ug")
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE, verbose_name = '作者')
    pub_date = models.DateTimeField('时间', auto_now_add=True)
    picture = models.FileField(blank=True, null=True)
    question_desc = models.CharField(max_length=800, null=True)
    
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = '问题'

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='问题')
    choice_text = models.TextField('回复',max_length=2000)
    # author = models.CharField(max_length=50, default="de8ug")
    author = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    picture = models.FileField(blank=True, null=True)

    def get_choice_text_md(self):
        return mark_safe(markdown(self.choice_text))

    def __str__(self):
        return self.choice_text

    class Meta:
        verbose_name = '回复'
        verbose_name_plural = '回复'