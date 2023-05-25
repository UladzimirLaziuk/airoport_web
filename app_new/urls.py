from django.urls import path
from .views import ExampleView, CityDetailView

urlpatterns = [
    path('', ExampleView.as_view(), name='example'),
    path('city/<str:name_city>/', CityDetailView.as_view(), name='city_detail'),
]