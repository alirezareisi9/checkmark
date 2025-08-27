# lib
# third-party
from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
# local
from . import views

app_name = 'authentication'

router = routers.DefaultRouter()  # parent router
router.register('user', views.UserInfoViewSet, basename='user')

authtoken_url = [
    path('login/', TokenObtainPairView.as_view(), name='login'),  # name='token_obtain_pair'
    path('login/refresh/', TokenRefreshView.as_view(), name='login_refresh')  # name='token_refresh
]


urlpatterns = router.urls + authtoken_url
