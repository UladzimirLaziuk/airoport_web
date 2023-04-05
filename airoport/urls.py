from django.contrib import admin
from django.urls import path
from app_air import views
from django.conf import settings
from django.conf.urls.static import static

from app_air.views import CityView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('city/<str:city_name>/', CityView.as_view(), name='city'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
