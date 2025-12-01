from django.contrib import admin
from .models import Exam,  Question, Option, Result

admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Result)
