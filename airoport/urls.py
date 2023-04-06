from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter

from app_air import views
from django.conf import settings
from django.conf.urls.static import static

from app_air.views import CityView, CityListAPIView, CityDetail

router = DefaultRouter()
router.register(r'cities', CityListAPIView, basename='city')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('city/<str:city_name>/', CityView.as_view(), name='city'),
    path('city-list/', CityListAPIView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
