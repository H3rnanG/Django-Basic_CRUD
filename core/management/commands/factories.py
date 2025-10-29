from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from notes.factories import NoteFactory, CategoryFactory
from notes.models import Note, Category
from accounts.factories import UserFactory


class Command(BaseCommand):
    help = "Create test data using factories"

    def add_arguments(self, parser):
        parser.add_argument("--users", type=int, nargs="?", const=5, default=None,
                            help="Number of users to create (default: 5)")
        parser.add_argument("--categories", type=int, nargs="?", const=5, default=None,
                            help="Number of categories to create (default: 5)")
        parser.add_argument("--notes", type=int, nargs="?", const=5, default=None,
                            help="Number of notes to create (default: 5)")
        parser.add_argument("--fresh", action='store_true',
                            help="Whether to truncate existing data first")
        parser.add_argument("--all", action='store_true',
                            help="Create all models.")

    def handle(self, *args, **options):
        users = options['users']
        categories = options['categories']
        notes = options['notes']
        fresh = options['fresh']
        all = options['all']

        if fresh:
            Note.objects.all().delete()
            Category.objects.all().delete()
            get_user_model().objects.exclude(username='root').delete()
            self.stdout.write(self.style.WARNING("Fresh flag is set. Truncating data..."))
        
        if all:
            UserFactory.create_batch(5)
            CategoryFactory.create_batch(5)
            NoteFactory.create_batch(10)
            return
        
        if users:
            self.stdout.write(self.style.SUCCESS(f"Creating {users} users"))
            UserFactory.create_batch(users)
            
        if categories:
            self.stdout.write(self.style.SUCCESS(f"Creating {categories} categories"))
            CategoryFactory.create_batch(categories)

        if notes:
            self.stdout.write(self.style.SUCCESS(f"Creating {notes} notes"))
            NoteFactory.create_batch(notes)
