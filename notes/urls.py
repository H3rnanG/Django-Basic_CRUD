from rest_framework import routers
from .views import NoteViewSet, CategoryViewSet


router = routers.DefaultRouter()
router.register('notes', NoteViewSet)
router.register('categories', CategoryViewSet)

urlpatterns = router.urls