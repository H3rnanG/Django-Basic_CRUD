from .models import Note, Category
from rest_framework.serializers import HyperlinkedModelSerializer


class NoteSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Note
        # fields = ['url', 'title', 'description', 'category', 'created_at', 'updated_at']
        fields = '__all__'

class CategorySerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Category
        # fields = ['url', 'title', 'description', 'created_at', 'updated_at']
        fields = '__all__'
        