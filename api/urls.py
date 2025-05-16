from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from rest_framework.routers import DefaultRouter
from api.views import TitleViewSet, UserAdminViewSet, send_verification_code, check_verification_code, UserGetPatchView
user_router = DefaultRouter()
user_router.register(r'users', UserAdminViewSet, basename='user')
title_router = DefaultRouter()
title_router.register(r'titles', TitleViewSet, basename='title')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email/', send_verification_code),
    path('auth/token/', check_verification_code),
    path('users/me/', UserGetPatchView.as_view(), name="user_get_patch"),
    path('', include(user_router.urls)),
    path('', include(title_router.urls)),

]
