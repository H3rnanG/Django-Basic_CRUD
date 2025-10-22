import factory
import random
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from .models import Category, Note


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('title', 'description')
        
    title = factory.Sequence(lambda n: 'Category %d' % n)
    description = factory.Faker('sentence', nb_words=10)
    
    @factory.post_generation
    def timestamps(obj, create, extracted, **kwargs):
        if not create:
            return
        
        days_ago = random.randint(0, 365)
        created = timezone.now() - timedelta(days=days_ago)
        updated = created + timedelta(days=random.randint(1, 182))
        
        type(obj).objects.filter(pk=obj.pk).update(
            created_at = created,
            updated_at = updated
        )
        
        obj.refresh_from_db(fields=['created_at', 'updated_at'])
        

class NoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Note
        django_get_or_create = ('title', 'description', 'user', 'category', 'is_published')

    title = factory.Sequence(lambda n: 'Note %d' % n)
    description = factory.Faker('sentence', nb_words=10)
    is_published = factory.Faker('boolean')
    user = factory.LazyFunction(lambda: random.choice(list(get_user_model().objects.all())))
    category = factory.LazyFunction(lambda: random.choice(list(Category.objects.all())))

    @factory.post_generation
    def timestamps(obj, create, extracted, **kwargs):
        if not create:
            return
        
        days_ago = random.randint(0, 365)
        created = timezone.now() - timedelta(days=days_ago)
        updated = created + timedelta(days=random.randint(1, 182))
        
        type(obj).objects.filter(pk=obj.pk).update(
            created_at = created,
            updated_at = updated
        )
        
        obj.refresh_from_db(fields=['created_at', 'updated_at'])