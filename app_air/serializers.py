# myapp/serializers.py
from rest_framework import serializers

from . import models
from .models import City, WhyCityAirport, AboutAirportCity, AboutCity


class HeroSubHeadlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HeroSubHeadline
        fields = '__all__'


class HeroHeroSectionSerializer(serializers.ModelSerializer):
    section_hero_subheading = HeroSubHeadlineSerializer(many=True)

    class Meta:
        model = models.HeroSection
        fields = '__all__'


#
# class HeroHeroSectionSerializer(serializers.ModelSerializer):
#     # cover_image_url = serializers.SerializerMethodField()
#     class Meta:
#         model = models.HeroSection
#         fields = '__all__'  # , 'cover_image_url'
#
# def get_cover_image_url(self, obj):
#     request = self.context.get('request')
#     cover_image_url = obj.image_hero_url_jpg
#     return request.build_absolute_uri(cover_image_url)


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


class BodySubSectionDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BodySubSectionDescription
        fields = '__all__'


class BodySubSectionSerializer(serializers.HyperlinkedModelSerializer):
    subsection_body_description = BodySubSectionDescriptionSerializer(many=True)

    class Meta:
        model = models.BodySubSection
        fields = '__all__'


class BodySectionSerializer(serializers.HyperlinkedModelSerializer):
    subsection_body = BodySubSectionSerializer(many=True)

    class Meta:
        model = models.BodySection
        fields = '__all__'


class AudienceSubSectionDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AudienceSubSectionDescription
        fields = '__all__'


class AudienceSubSectionSerializer(serializers.HyperlinkedModelSerializer):
    audience_subsection_descriptions = AudienceSubSectionDescriptionSerializer(many=True)

    class Meta:
        model = models.AudienceSubSection
        fields = '__all__'


class AudienceSectionSerializer(serializers.HyperlinkedModelSerializer):
    audience_subsection = AudienceSubSectionSerializer(many=True)

    class Meta:
        model = models.AudienceSection
        fields = '__all__'


class CitySerializer(serializers.HyperlinkedModelSerializer):
    section_hero = HeroHeroSectionSerializer(many=True)
    section_body = BodySectionSerializer(many=True)
    section_audience = AudienceSectionSerializer(many=True)

    class Meta:
        model = models.City
        fields = '__all__'

    def update(self, instance, validated_data):
        print('')
        section_hero = validated_data.pop('section_hero')
        section_body = validated_data.pop('section_body')
        section_audience = validated_data.pop('section_audience')

        return super().update(instance, validated_data)
