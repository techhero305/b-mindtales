"""internal_menu_selection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f"{settings.PREFIX}auth/login/", jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path(f"{settings.PREFIX}auth/token/refresh", jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path(f"{settings.PREFIX}roles/", include('roles.urls'), name='roles'),
    path(f"{settings.PREFIX}users/", include('users.urls'), name='users'),
    path(f"{settings.PREFIX}restaurant/", include('restaurant.urls'), name='restaurant'),
    path(f"{settings.PREFIX}vote/", include('vote.urls'), name='vote'),
]
