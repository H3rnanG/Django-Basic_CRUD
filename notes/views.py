from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, DjangoModelPermissions, SAFE_METHODS
from django_filters import rest_framework as filters
from django.db.models import Q
from .serializers import NoteSerializer, CategorySerializer
from .permissions import IsOwnerOrAdmin
from .models import Note, Category
from .filters import NoteFilter


class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsOwnerOrAdmin]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = NoteFilter

    def get_queryset(self):
        user = self.request.user
        
        if self.action == 'list':
            if user.is_authenticated:
                return Note.objects.filter(Q(user=user) | Q(is_published=True))
            return Note.objects.filter(is_published=True)
        
        return Note.objects.all()

    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS:
    #         return [AllowAny()]
    #     elif self.request.method == 'POST':
    #         return [IsAuthenticated()]
    #     return [IsOwnerOrAdmin()]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    @action(detail=False, methods=['get'], url_name='my-notes', url_path='my-notes')
    def my_notes(self, request):
        user = request.user
        
        if not user.is_authenticated:
            return Response({'detail': 'You do not have permission to perform this action.'}, status=401)
        
        notes = Note.objects.filter(user=user)
        serializer = self.get_serializer(notes, many=True)
        return Response(serializer.data)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [DjangoModelPermissions()]