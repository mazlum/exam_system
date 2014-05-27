# -*- coding: utf-8 -*-
from django.contrib import admin
from exam.models import *
from django.contrib.auth.forms import *


class QuestionInline(admin.TabularInline):
    model = Question


class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'time', 'start','see')
    prepopulated_fields = {"name_slug": ("name",)}
    list_editable = ('start', 'see')
    inlines = [
        QuestionInline,
    ]

class UserExamAdmin(admin.ModelAdmin):
    list_display = ["user", "exam", "point"]
    list_filter = ["user", "exam"]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 4
    max_num = 5


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'exam', 'get_true_answer')
    inlines = [
        AnswerInline,
    ]
    search_fields = ('question', )
    list_filter = ('exam', )

    def get_true_answer(self, obj):
        return Answer.objects.get(question=obj, true=True).answer

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'true')
    search_fields = ('answer', )
    list_filter = ('question', )


class QuestionUserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'exam', 'question', 'answer')
    list_filter = ('user', 'exam', 'question')

class GroupExamForm(forms.ModelForm):
    def clean_group(self):
        group = self.cleaned_data.get('group')
        if group and GroupExam.objects.filter(group=group).exclude(id=self.instance.id).count():
            raise forms.ValidationError(u'Group must bu unique')
        return group


class GroupExamAdmin(admin.ModelAdmin):
    list_display = ['group', 'get_exam']

    def get_exam(self, obj):
        return ",".join(exam.name for exam in obj.exam.all())

    form = GroupExamForm
    list_filter = ['group', 'exam']
    filter_horizontal = ('exam', )



admin.site.register(Exam, ExamAdmin)
admin.site.register(UserExam, UserExamAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(QuestionUserAnswer, QuestionUserAnswerAdmin)
admin.site.register(GroupExam, GroupExamAdmin)