from django_filters import rest_framework as filters
from .models import Note

class NoteFilter(filters.FilterSet):
    
    class Meta:
        model = Note
        fields = ['category', 'is_published', 'created_at']