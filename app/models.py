from django.db import models
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AbstractUser, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from datetime import datetime


class Profile(models.Model):
    profile = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='uploads/%Y/%m/%d/')

    def __str__(self):
        return self.user


class Tag(models.Model):
    tag = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name=u"Имя тэга")

    def __str__(self):
        return self.title


class LikeDislikeManager(models.Manager):
    use_for_related_fields = True

    def sum_rating(self):
        return self.get_queryset().aggregate(Sum('vote')).get('vote__sum') or 0


class LikeDislike(models.Model):
    like_dislike = models.AutoField(primary_key=True)

    LIKE = 1
    DISLIKE = -1

    votes = ((LIKE, 'Like'), (DISLIKE, 'Dislike'))
    vote = models.SmallIntegerField(choices=votes, verbose_name=u'Выбор пользователя (Лайк/Дизлайк)')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    objects = LikeDislikeManager()


class QuestionManager(models.Manager):
    def new_questions(self):
        return self.order_by('-create_date')

    def hot_questions(self):
       return self.order_by('rating')

    def tag_questions(self, search_tag):
        return self.filter(tags__title__in=[search_tag]).distinct()

    def one_question(self, qid):
        question_ = Question.objects.get(question=qid)
        answers = Answer.objects.filter(question=question_.question)
        ans_count = answers.count()
        return question_, answers, ans_count


class Question(models.Model):
    question = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Описание вопроса")

    create_date = models.DateTimeField(default=datetime.now, auto_now=False, auto_now_add=False,
                                       verbose_name=u"Время создания вопроса")
    tags = models.ManyToManyField(Tag, blank=True)

    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    rating = GenericRelation(to=LikeDislike, related_query_name="question")

    objects = QuestionManager()

    def __str__(self):
        return self.title


class Answer(models.Model):
    answer = models.AutoField(primary_key=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False, verbose_name=u"Правильность ответа")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания ответа")
    text = models.TextField(verbose_name=u"Текст ответа")
    rating = GenericRelation(to=LikeDislike, related_query_name="answer")
