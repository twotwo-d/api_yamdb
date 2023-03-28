from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, get_jwt_token, signup

app_name = 'users'

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('/api/v1/auth/token/', get_jwt_token, name='token'),
    path('/api/v1/auth/signup/', signup),
    path('/api/v1/', include(router.urls)),
]
