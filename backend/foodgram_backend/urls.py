from api.views import (AllUserViewSet, IngridientsViewSet, RecipesViewSet,
                       TagsViewSet)
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()

router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngridientsViewSet, basename='ingredients')
router.register(r'recipes', RecipesViewSet, basename='recipes')
router.register(r'users', AllUserViewSet, basename='users')
urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls.authtoken')),
    path('api/', include('djoser.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
