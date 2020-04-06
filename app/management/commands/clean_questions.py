from django.core.management.base import BaseCommand, CommandError
from app.models import *


class Command(BaseCommand):
    help = 'Delete all questions'

    def handle(self, *args, **options):
        Question.objects.filter().delete()
