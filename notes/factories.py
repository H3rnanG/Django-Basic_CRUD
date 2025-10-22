import factory
import random
from django.utils import timezone
from datetime import timedelta


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'notes.Category'
        django_get_or_create = ('title', 'description')
        
    title = factory.Sequence(lambda n: 'Category %d' % n)
    description = factory.Faker('sentence', nb_words=10)