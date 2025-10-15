from django.contrib.auth.models import User, Group, Permission
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, GroupSerializer, PermissionSerializer

# Create your views here.
class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class GroupViewSet(ModelViewSet):
    serializer_class = GroupSerializer
    queryset = Group.objects.all().order_by('name')
    permission_classes = [IsAuthenticated, IsAdminUser]
    
class PermissionViewSet(ModelViewSet):
    serializer_class = PermissionSerializer
    queryset = Permission.objects.all().order_by('content_type__app_label', 'codename')
    permission_classes = [IsAuthenticated]