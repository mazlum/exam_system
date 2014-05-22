# -*- coding: utf-8 -*-
from django.contrib import admin
from exam.models import *


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'start')


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    max_num = 5

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'exam', 'point')
    inlines = [
        AnswerInline,
    ]
    search_fields = ('question', )
    list_filter = ('exam', )


class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'true')
    search_fields = ('answer', )
    list_filter = ('question', )


class QuestionUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer')
    list_filter = ('user', 'question', 'answer')


admin.site.register(Exam, ExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionUserAnswer)
