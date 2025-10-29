from django_filters import rest_framework as filters
from .models import Note

class NoteFilter(filters.FilterSet):
    user = filters.NumberFilter()
    category = filters.CharFilter(field_name='category__title', lookup_expr='iexact')
    created_after = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_before = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    
    ordering = filters.OrderingFilter(
        fields={
            ('category', 'category'),
            ('created_at', 'created_at')
        }
    )
    
    class Meta:
        model = Note
        fields = ['is_published', 'user', 'category']