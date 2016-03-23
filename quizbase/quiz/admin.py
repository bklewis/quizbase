from django.contrib import admin

# Register your models here.
from .models import Quiz
from .models import Question
from .models import Answer
from .models import Quiz_attempt
from .models import Answer_attempt

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Quiz_attempt)
admin.site.register(Answer_attempt)

#class QuizAdmin(admin.modelAdmin):
#	fields: ['name']

#admin.site.register(Quiz, QuizAdmin)
