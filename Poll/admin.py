from operator import mod
from pyexpat import model
from django.contrib import admin
from django.test import tag
from numpy import extract
from .models import Question, Choice, Tags

# Register your models here.

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class TagInLine(admin.TabularInline):
    model = Tags
    extra = 2
    
class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Tags)