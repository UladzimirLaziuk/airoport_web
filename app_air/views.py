from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from app_air.models import City, BodySection, BodySubSection, BodySubSectionDescription, AudienceSection, \
    AudienceSubSectionDescription, AudienceSubSection
from app_air.serializers import CitySerializer, HeroHeroSectionSerializer, BodySectionSerializer, \
    BodySubSectionSerializer, BodySubSectionDescriptionSerializer, AudienceSectionSerializer, \
    AudienceSubSectionSerializer, AudienceSubSectionDescriptionSerializer


# Create your views here.
def home(request):
    return render(request, 'app_air/index.html', {})


def home_title(context=None, name_html=None):
    return render(name_html, context=context)


class CityListAPIView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [IsAuthenticated]


class CityView(TemplateView):
    template_name = 'app_air/{}.html'

    def get(self, request, *args, **kwargs):
        city_name = kwargs.get('city_name')
        self.template_name = self.template_name.format(city_name)
        return super().get(request, *args, **kwargs)


class BodyDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BodySection.objects.all()
    serializer_class = BodySectionSerializer
    permission_classes = [IsAuthenticated]


class BodySubSectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BodySubSection.objects.all()
    serializer_class = BodySubSectionSerializer
    permission_classes = [IsAuthenticated]


class BodySubSectionDescriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = BodySubSectionDescription.objects.all()
    serializer_class = BodySubSectionDescriptionSerializer
    permission_classes = [IsAuthenticated]


class AudienceSectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudienceSection.objects.all()
    serializer_class = AudienceSectionSerializer
    permission_classes = [IsAuthenticated]


class AudienceSubSectionDescriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudienceSubSectionDescription.objects.all()
    serializer_class = AudienceSubSectionDescriptionSerializer
    permission_classes = [IsAuthenticated]


class AudienceSubSectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = AudienceSubSection.objects.all()
    serializer_class = AudienceSubSectionSerializer
    permission_classes = [IsAuthenticated]
