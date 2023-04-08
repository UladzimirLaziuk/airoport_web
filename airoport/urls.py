from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from app_air import views
from django.conf import settings
from django.conf.urls.static import static

from app_air.views import CityView, CityListAPIView, CityDetail, BodyDetail, BodySubSectionDetail, \
    BodySubSectionDescriptionDetail, AudienceSectionDetail, AudienceSubSectionDescriptionDetail, \
    AudienceSubSectionDetail
from django.contrib.auth.views import LogoutView
# router = DefaultRouter()
# router.register(r'cities', CityListAPIView, basename='city')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.home, name='home'),
    path('city/<str:city_name>/', CityView.as_view(), name='city'),
    path('city-list/', CityListAPIView.as_view(), name='city-list'),
    path('cities/<int:pk>/', CityDetail.as_view(), name='city-detail'),
    path('bodies/<int:pk>/', BodyDetail.as_view(), name='bodysection-detail'),
    path('bodysubsection/<int:pk>/', BodySubSectionDetail.as_view(), name='bodysubsection-detail'),
    path('bodysubsection/<int:pk>/', BodySubSectionDescriptionDetail.as_view(), name='bodysubsectiondescription-detail'),
    path('audiencesection/<int:pk>/', AudienceSectionDetail.as_view(), name='audiencesection-detail'),
    path('audiencesection-subsection/<int:pk>/', AudienceSubSectionDetail.as_view(), name='audiencesubsection-detail'),
    path('audience-subsection-descriptions/<int:pk>/', AudienceSubSectionDescriptionDetail.as_view(), name='audiencesubsectiondescription-detail'),




]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
