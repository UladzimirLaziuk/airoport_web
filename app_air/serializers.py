# myapp/serializers.py
from rest_framework import serializers

from . import models
from .models import City


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


# class WhyCityAirportSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WhyCityAirport
#         fields = 'why_title', 'description'


# class AboutAirportCitySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = AboutAirportCity
#         fields = 'about_title', 'description'


# class AboutCitySerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = AboutCity
#         fields = 'about_title', 'description'


class BodySubSectionDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.BodySubSectionDescription
        fields = '__all__'


class BodySubSectionSerializer(serializers.HyperlinkedModelSerializer):
    paragraphs = BodySubSectionDescriptionSerializer(many=True)

    class Meta:
        model = models.BodySubSection
        fields = '__all__'



class BodySectionSerializer(serializers.HyperlinkedModelSerializer):
    tabs = BodySubSectionSerializer(many=True)

    class Meta:
        model = models.BodySection
        fields = '__all__'




class AudienceSubSectionDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.AudienceSubSectionDescription
        fields = '__all__'


class AudienceSubSectionSerializer(serializers.HyperlinkedModelSerializer):
    paragraphs = AudienceSubSectionDescriptionSerializer(many=True)

    class Meta:
        model = models.AudienceSubSection
        fields = '__all__'


class AudienceSectionSerializer(serializers.HyperlinkedModelSerializer):
    accordions = AudienceSubSectionSerializer(many=True)

    class Meta:
        model = models.AudienceSection
        fields = '__all__'


class CampaignTypesSubSectionDescriptionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.CampaignTypesSubSectionDescription
        fields = '__all__'


class CampaignTypesSubSectionSerializer(serializers.HyperlinkedModelSerializer):
    subsection_campaign_types_description = CampaignTypesSubSectionDescriptionSerializer(many=True)

    class Meta:
        model = models.CampaignTypesSubSection
        fields = '__all__'


class CampaignTypesSectionSerializer(serializers.HyperlinkedModelSerializer):
    subsection_campaign_types = CampaignTypesSubSectionSerializer(many=True)

    class Meta:
        model = models.CampaignTypesSection
        fields = '__all__'


class MediaSolutionsTabSectionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.MediaSolutionsTabSection
        fields = '__all__'


class MediaSolutionsSectionSerializer(serializers.HyperlinkedModelSerializer):
    media_solutions_tab = MediaSolutionsTabSectionSerializer(many=True)

    class Meta:
        model = models.MediaSolutionsSection
        fields = '__all__'



class CitySerializer(serializers.HyperlinkedModelSerializer):
    section_hero = HeroHeroSectionSerializer(many=True)
    section_body = BodySectionSerializer(many=True)
    section_audience = AudienceSectionSerializer(many=True)
    section_media_solutions = MediaSolutionsSectionSerializer(many=True)

    class Meta:
        model = models.City
        fields = '__all__'


