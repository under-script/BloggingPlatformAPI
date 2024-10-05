from django.core.management.base import BaseCommand
from django.db import connection
from api.models import Tag

class Command(BaseCommand):
    help = 'Reset the sequence of the Tag model in the database'

    def handle(self, *args, **kwargs):
        # Delete all existing tags
        Tag.objects.all().delete()

        # Get the current database engine
        db_engine = connection.vendor

        with connection.cursor() as cursor:
            if db_engine == 'sqlite':
                # For SQLite
                cursor.execute("DELETE FROM sqlite_sequence WHERE name='api_tag';")

        self.stdout.write(self.style.SUCCESS('Successfully reset the Tag model sequence.'))
