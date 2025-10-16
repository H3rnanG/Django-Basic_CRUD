from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all(), required=False)
    password = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'first_name', 'last_name', 'password', 'permissions', 'groups', 'is_active', 'date_joined']
        read_only_fields = ['date_joined']
        
        # With `ModelSerializer`
        # fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'date_joined']
        # read_only_fields = ['id', 'date_joined']
        
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        groups = validated_data.pop('groups', None)
        permissions = validated_data.pop('permissions', None)
        user = User(**validated_data)
        
        if password:
            user.set_password(password)
        user.save()
        
        if groups:
            user.groups.set(groups)
        if permissions:
            user.user_permissions.set(permissions)
            
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        permissions = validated_data.pop('permissions', None)
        groups = validated_data.pop('groups', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)
        instance.save()

        if groups is not None:
            instance.groups.set(groups)
        if permissions is not None:
            instance.user_permissions.set(permissions)

        return instance
    

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(many=True, queryset=Permission.objects.all(), required=False)
    
    class Meta:
        model = Group
        fields = ['url', 'name', 'permissions']

        # With `ModelSerializer`
        # fields = ['id', 'name']
        # read_only_fields = ['id']

        
class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']
        read_only_fields = ['id']