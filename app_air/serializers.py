# myapp/serializers.py
from rest_framework import serializers
from .models import City, HeroModel, WhyCityAirport, AboutAirportCity, AboutCity


class HeroModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroModel
        fields = 'hero_title',


class WhyCityAirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyCityAirport
        fields = 'why_title', 'description'


class AboutAirportCitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AboutAirportCity
        fields = 'about_title', 'description'


class AboutCitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AboutCity
        fields = 'about_title', 'description'


class CitySerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='city-detail'
    )
    hero_obj = HeroModelSerializer(many=True)
    why_city_obj = WhyCityAirportSerializer(many=True)
    about_airport = AboutAirportCitySerializer(many=True)
    about_city_obj = AboutCitySerializer(many=True, read_only=True)

    class Meta:
        model = City
        fields = 'url', 'name_city', 'page_title', 'hero_obj', 'why_city_obj', 'about_airport', 'about_city_obj'
