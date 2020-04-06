from django.core.management.base import BaseCommand, CommandError
from app.models import *
from django.utils.crypto import get_random_string
from faker import Faker

class Command(BaseCommand):
    help = 'Create users'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users')

    def handle(self, *args, **options):
        fake = Faker()
        total = options['total']
        for i in range(total):
            u = User(username=fake.name(), email=fake.email(), password=get_random_string())
            u.save()
            p = Profile(user=u, avatar="../../../static/img/64x64.png")
            p.save()
