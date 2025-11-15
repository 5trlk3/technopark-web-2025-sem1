from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.urls import reverse

class QuestionManager(models.Manager):
    def with_annotations(self):
        return self.annotate(
        answer_count=Count(
            'answer'
        )
    ).prefetch_related('questiontag_set__tag_id')

    def recent(self):
        return self.with_annotations().order_by('-created_at')
    
    def hot(self):
        return self.with_annotations().order_by('-answer_count')
    
    def by_tag(self, tag_name):
        return self.with_annotations().filter(questiontag__tag_id__name=tag_name).distinct()

    def by_user(self, user_profile):
        return self.with_annotations().filter(profile_id=user_profile)

class AnswerManager(models.Manager):
    def for_question(self, cur_question):
        return self.filter(question_id=cur_question).order_by('-created_at')

class User_profileManager(models.Manager):
    def popular(self, limit=30):
        return self.annotate(
            unique_answerers=Count(
                'question__answer__profile_id',
                distinct=True
            )
        ).order_by('-unique_answerers')[:limit]

class TagManager(models.Manager):
    def popular(self, limit=30):
        return self.annotate(
            questions_count=Count(
            'questiontag',
            distinct=True
            )
        ).order_by('-questions_count')[:limit]

class Question(models.Model):
    title = models.CharField(max_length=256)
    text = models.TextField(null=False)
    rating = models.IntegerField(default=0)
    profile_id = models.ForeignKey('questions.User_profile', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    @property
    def tags(self):
        return [qt.tag_id for qt in self.questiontag_set.all()]
    
    def get_absolute_url(self):
        return reverse('conc_question', kwargs={'id': self.id})
    
    class Meta:
        db_table = "questions_question"
        ordering = ["-created_at"]

class Answer(models.Model):
    text = models.TextField(null=False)
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    profile_id = models.ForeignKey('questions.User_profile', on_delete=models.CASCADE, null=False)
    question_id = models.ForeignKey('questions.Question', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    class Meta:
        db_table = "questions_answer"
        ordering = ["-created_at"]

class AnswerLike(models.Model):
    VALID_CHOICES = [
        (1, "Лайк"),
        (-1, "Дизлайк")
    ]
    value = models.IntegerField(choices=VALID_CHOICES, null=False)
    profile_id = models.ForeignKey('questions.User_profile', on_delete=models.CASCADE, null=False)
    answer_id = models.ForeignKey('questions.Answer', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('profile_id', 'answer_id')

class QuestionLike(models.Model):
    VALID_CHOICES = [
        (1, "Лайк"),
        (-1, "Дизлайк")
    ]
    value = models.IntegerField(choices=VALID_CHOICES, null=False)
    profile_id = models.ForeignKey('questions.User_profile', on_delete=models.CASCADE, null=False)
    question_id = models.ForeignKey('questions.Question', on_delete=models.CASCADE, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('profile_id', 'question_id')

class User_profile(models.Model):
    nickname = models.CharField(max_length=128)
    user_id = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=False)
    image = models.ImageField()
    about = models.TextField()

    objects = User_profileManager()

    def get_absolute_url(self):
        return reverse('user_profile', kwargs={'user': self.nickname})

    class Meta:
        db_table = "questions_user_profile"

class Tag(models.Model):
    name = models.CharField(max_length=64)

    objects = TagManager()

    def get_absolute_url(self):
        return reverse('tag', kwargs={'name': self.name})

    class Meta:
        db_table = "questions_tag"

class QuestionTag(models.Model):
    question_id = models.ForeignKey('questions.Question', on_delete=models.CASCADE, null=True)
    tag_id = models.ForeignKey('questions.Tag', on_delete=models.CASCADE, null=True)

