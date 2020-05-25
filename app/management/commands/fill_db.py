from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app.models import *
from random import randint
from faker import *


class Command(BaseCommand):
    help = 'Fill database'

    def add_arguments(self, parser):
        parser.add_argument('users', type=int, help='Indicates the number of users')
        parser.add_argument('tags', type=int, help='Indicates the number of tags')
        parser.add_argument('questions', type=int, help='Indicates the number of questions')
        parser.add_argument('max_answers', type=int, help='Indicates the number of answers')

    def create_tags(self, fake, number_of_tags):
        for i in range(number_of_tags):
            t = Tag(title=fake.word())
            t.save()

    def create_users(self, fake, number_of_users):
        for i in range(number_of_users):
            u = User(username=fake.name(), password=fake.password(), email=fake.email())
            u.save()
            p = Profile(user=u, avatar="../../../static/img/64x64.png")
            p.save()

    def create_questions(self, fake, number_of_questions):
        userIds = User.objects.values_list('id', flat=True)
        tagIds = Tag.objects.values_list('id', flat=True)

        for i in range(number_of_questions):
            q = Question(title=fake.sentence()[:45],
                         text=fake.text(),
                         author=User.objects.get(pk=userIds[randint(0, userIds.count() - 1)]),
                         is_active=True,
                         create_date=timezone.now())
            q.save()

            question_number_of_tags = randint(0, min(10, tagIds.count() - 1))
            for j in range(question_number_of_tags):
                q.tags.add(Tag.objects.get(pk=tagIds[randint(0, tagIds.count() - 1)]))
            q.save()

    def create_answers(self, fake, max_number_of_answers):
        userIds = User.objects.values_list('id', flat=True)
        questionIds = Question.objects.values_list('id', flat=True)
        number_of_questions = questionIds.count() - 1
        number_of_users = userIds.count() - 1

        for i in range(number_of_questions):
            number_of_answers = randint(0, max_number_of_answers)
            for j in range(number_of_answers):
                qid = questionIds[randint(0, number_of_questions)]
                a = Answer(author=User.objects.get(pk=userIds[randint(0, number_of_users)]),
                           question=Question.objects.get(pk=questionIds[randint(0, number_of_questions)]),
                           is_correct=False,
                           create_date=timezone.now(),
                           text=fake.text(),
                           )

                q = Question.objects.get(pk=qid)
                q.answers += 1
                q.save()

                a.save()

    def create_likes(self):
        number_of_questions = Question.objects.count()
        questions = Question.objects.get_queryset()
        users = User.objects.get_queryset()
        number_of_users = users.count()

        for i in range(number_of_users):
            for j in range(number_of_questions):
                if randint(0, 1) == 1:
                    qid = randint(1, number_of_questions)
                    like = LikeDislike(content_object=Question.objects.get(pk=qid),
                                       vote=1,
                                       user=User.objects.get(pk=randint(1, number_of_users)))
                    q = Question.objects.get(pk=qid)
                    q.rating += 1
                    q.save()
                    like.save()

    def handle(self, *args, **options):
        fake = Faker()
        users = options['users']
        tags = options['tags']
        questions = options['questions']
        max_answers = options['max_answers']

        self.create_tags(fake, tags)
        self.create_users(fake, users)
        self.create_questions(fake, questions)
        self.create_answers(fake, max_answers)
        self.create_likes()
