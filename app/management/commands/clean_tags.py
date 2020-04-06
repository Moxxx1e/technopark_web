from django.core.management.base import BaseCommand, CommandError
from app.models import *


class Command(BaseCommand):
    help = 'Delete all tags'

    def handle(self, *args, **options):
        Tag.objects.filter().delete()
