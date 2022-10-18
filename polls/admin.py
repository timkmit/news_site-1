from django.contrib import admin

from .models import Choice, Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id',"question_text",'pub_date')
    list_display_links = ('id',"question_text")
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id','choice_text')
    list_display_links = ('id', 'choice_text')

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice,ChoiceAdmin)