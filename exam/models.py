# -*- coding: utf-8 -*-/1sinav/
from django.db import models
from django.contrib.auth.models import User, Group


class Exam(models.Model):
    name = models.CharField(max_length=100, verbose_name="Exam Name ")
    name_slug = models.CharField(max_length=100, verbose_name="Exam Slug ")
    time = models.IntegerField(verbose_name="Exam Time ")
    start = models.BooleanField(verbose_name="Exam Started ")
    see = models.BooleanField(verbose_name="User see result ")

    def __unicode__(self):
        return self.name



class UserExam(models.Model):
    user = models.ForeignKey(User, verbose_name="User ")
    exam = models.ForeignKey(Exam, verbose_name="Exam ")
    point = models.IntegerField(verbose_name="User Point")

    def __unicode__(self):
        return "%s - %s" % (self.user.username, self.exam.name)

    class Meta:
        verbose_name = "Users and Exam"

class Question(models.Model):
    question = models.TextField(verbose_name="Question Title ")
    exam = models.ForeignKey(Exam, verbose_name="Question Exam ")

    def get_true_answer(self):
        try:
            return Answer.objects.get(question=self, true=True).answer
        except Answer.DoesNotExist:
            return "Answer does not exist"

    def __unicode__(self):
        return self.question


class Answer(models.Model):
    answer = models.CharField(max_length=300, verbose_name="Question answer ")
    question = models.ForeignKey(Question, verbose_name="Answer Question ")
    true = models.BooleanField(verbose_name="True Answer ")


    def __unicode__(self):
        return self.answer


class QuestionUserAnswer(models.Model):
    user = models.ForeignKey(User, verbose_name="User ")
    exam = models.ForeignKey(Exam, verbose_name="Exam ")
    question = models.ForeignKey(Question, verbose_name="Question ")
    answer = models.ForeignKey(Answer, verbose_name="Answer ")

    def __str__(self):
        return "%s,%s,%s"%(self.user,self.question,self.answer)

    class Meta:
        verbose_name = "Question, User, Exam and Answer"

class GroupExam(models.Model):
    group = models.ForeignKey(Group, verbose_name="Group ")
    exam = models.ManyToManyField(Exam, verbose_name="Exam ")

    def __str__(self):
        return "%s,%s"%(self.group,self.exam)

    class Meta:
        verbose_name = "Groups and Exam"