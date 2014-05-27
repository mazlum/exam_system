from django import template


register = template.Library()
from exam.models import *


#Get user answer for user_exam_question template
def true_answer(value, user):
    true = QuestionUserAnswer.objects.get(question=value, user=user).answer.answer
    return true

register.filter("true_answer",true_answer)