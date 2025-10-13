from rest_framework.viewsets import ModelViewSet
from .serializers import NoteSerializer, CategorySerializer
from .models import Note, Category


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer