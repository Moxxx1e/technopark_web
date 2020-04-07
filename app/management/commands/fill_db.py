from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app.models import *
from random import randint
from faker import *

questions_list = ['How to use Django Templates?',
                  'Where can i find Django tutorials?',
                  'What should I do with ValueError in this code?',
                  'How to make pizza?']
number_of_tags = 8
max_number_of_answers = 5

class Command(BaseCommand):
    help = 'Create questions'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of questions')

    def handle(self, *args, **options):
        fake = Faker()
        total = options['total']

        for i in range(number_of_tags):
            t = Tag(title=fake.word())
            t.save()

        for i in range(total):
            u = User(username=fake.name(), password=fake.password(), email=fake.email())
            u.save()
            p = Profile(user=u, avatar="../../../static/img/64x64.png")
            p.save()

            q = Question(title=questions_list[randint(0, len(questions_list) - 1)],
                         text=fake.text(),
                         author=u,
                         is_active=True,
                         create_date=timezone.now())
            q.save()
            question_number_of_tags = randint(0, number_of_tags/2)
            for j in range(question_number_of_tags):
                q.tags.add(Tag.objects.get(pk=randint(1, number_of_tags)))
            q.save()

            for i in range(randint(1, max_number_of_answers)):
                a = Answer(author=User.objects.get(pk=1),
                           question=q,
                           is_correct=False,
                           create_date=timezone.now(),
                           text=fake.text(),
                           )
                a.save()

            l = LikeDislike(content_object=q, vote=1, user=u)
            l.save()
