from django.core.management.base import BaseCommand, CommandError
from app.models import *
from faker import Faker
from random import randint

my_tags_list = ['Python', 'C++', 'Java', 'Go']


class Command(BaseCommand):
    help = 'Create tags'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of tags')

    def handle(self, *args, **options):
        fake = Faker()
        total = options['total']
        for i in range(total):
            t = Tag(title=my_tags_list[i])
            t.save()
