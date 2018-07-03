from django.db import models
from django.contrib import admin
# Create your models here.

class Bank(models.Model):
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=200)
    num = models.IntegerField(default=0)
    is_available = models.BooleanField()

    def __str__(self):
        return self.name

class QuestionAnswer(models.Model):
    question = models.CharField(max_length=150)
    keywords = models.CharField(max_length=150, null=True)
    answer = models.TextField()
    url = models.CharField(max_length=200, null=True)
    bank = models.ForeignKey(Bank)
    like = models.IntegerField(default=0)
    dislike = models.IntegerField(default=0)


class QuestionClient(models.Model):
    question = models.CharField(max_length=150)


class QuestionAnswerAdmin(object):
    list_display = ['question', 'answer']
    search_fields = ['question']

class BankAdmin(object):
    list_display = ['name', 'url', 'is_available']
    search_fields = ['name']