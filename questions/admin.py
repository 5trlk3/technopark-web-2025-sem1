from django.contrib import admin

from questions.models import Question, Answer, Tag, QuestionTag, User_profile, QuestionLike, AnswerLike

@admin.register(Question)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'text', 'rating', 'profile_id']
    search_fields = ['title', 'profile_id']

@admin.register(Answer)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ['text', 'is_correct', 'rating', 'profile_id', 'question_id']

@admin.register(User_profile)
class User_profileAdmin(admin.ModelAdmin):
    list_display = ['nickname', 'about']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name']

