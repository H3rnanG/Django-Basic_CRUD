from django_filters import rest_framework as filters
from django.contrib.postgres.search import SearchVector, SearchQuery
from .models import Note

class NoteFilter(filters.FilterSet):
    user = filters.NumberFilter()
    category = filters.CharFilter(field_name='category__title', lookup_expr='iexact')
    created_after = filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    search = filters.CharFilter(field_name='description', method='search_fulltext')
    
    ordering = filters.OrderingFilter(
        fields={
            ('category', 'category'),
            ('created_at', 'created_at')
        }
    )

    def search_fulltext(self, queryset, field_name, value):
        if not value:
            return queryset
        return queryset.annotate(
            search=SearchVector('title', 'description')
        ).filter(search=SearchQuery(value))
    
    class Meta:
        model = Note
        fields = ['is_published', 'user', 'category']