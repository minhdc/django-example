from django.contrib import admin

from .models import Question
# Register your models here.
#admin.site.register(Question)
	
class QuestionAdmin(admin.ModelAdmin):
	"""docstring for QuestionAdmin"admin.ModelAdmin"""
	fieldsets = [
		(None,				 {'fields':['question_text']}),
		('Date information', {'fields':['pub_date']}),
	]

admin.site.register(Question,QuestionAdmin)

