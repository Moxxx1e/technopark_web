from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone
from app.models import *
from random import randint
from faker import *

questions_list = ['How to use Django Templates?',
                  'Where can i find Django tutorials?',
                  'What should I do with ValueError in this code?',
                  'How to make pizza?']


class Command(BaseCommand):
    help = 'Create questions'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of questions')

    def handle(self, *args, **options):
        fake = Faker()
        total = options['total']
        number_of_tags = randint(0, 3)
        tags_generated = []
        for i in range(number_of_tags):
            tags_generated.append(Tag.objects.get(pk=randint(0, Tag.objects.count())))

        for i in range(total):
            q = Question(title=questions_list[randint(0, 3)], text=fake.text(),
                         author=User.objects.get(pk=2),
                         is_active=True)
            q.create_date =timezone.now()
            q.save()
            q.tags.set(tags_generated)
            q.save()
