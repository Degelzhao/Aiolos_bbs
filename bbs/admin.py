from django.contrib import admin

# Register your models here.
from .models import Question, Choice


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'author', 'question_desc','pub_date')
    list_filter = ('question_text', 'author', 'pub_date')
    search_fields = ('question_text',)
    # list_editable = ( 'author',)
    list_editable = ('question_text', 'author','question_desc')
    list_display_links = None
    list_per_page = 10


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question',  'author')
    list_filter = ('choice_text', 'question',  'author')
    search_fields = ('choice_text',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
