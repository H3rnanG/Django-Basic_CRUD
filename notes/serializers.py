from .models import Note, Category
from rest_framework import serializers


class NoteSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Note
        # fields = ['url', 'title', 'description', 'category', 'created_at', 'updated_at']
        fields = '__all__'

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        # fields = ['url', 'title', 'description', 'created_at', 'updated_at']
        fields = '__all__'
        