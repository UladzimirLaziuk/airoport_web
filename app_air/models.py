import os
import shutil

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse

from airoport import settings
from app_air.utils_copy_file import copy_and_rename_file, parse_file_compile, replace_static_urls_in_html_file
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site



###########################################################################################################
"""Section Title: Hero

    1. Page Title: 
    2. Hero Image (austin_airport_advertising_hero_main)
    3. Hero Headline: title
    4. Hero Sub Headline: description"""


class City(models.Model):
    name_city = models.CharField(max_length=255, verbose_name='name_city')
    code_city = models.CharField(max_length=255, verbose_name='code_city')
    page_title = models.CharField(max_length=255, verbose_name='Page Title')

    def __str__(self):
        return f'{self.name_city}'


class HeroSection(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_hero')
    hero_image_name = models.CharField(max_length=255, verbose_name='hero image name')
    # title = models.CharField(max_length=255, verbose_name='Hero Headline: title')


class HeroSubHeadline(models.Model):
    section_hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='section_hero_subheading')
    description = models.TextField()


'''
Section: Body

    5. Why Airport? (title and body fields)
    6. Airport (title and body fields)
    7. City (title and body fields)
    8. Main Body Image (austin_airport_aus_advertising_body_image)

'''


class BodySection(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_body')
    body_image_name = models.CharField(max_length=255, verbose_name='main body image name')
    title = models.CharField(max_length=255, verbose_name='WhyAirport?', default='WhyAirport?')


class BodySubSection(models.Model):
    section_body = models.ForeignKey(BodySection, on_delete=models.CASCADE, related_name='subsection_body')
    title = models.CharField(max_length=255, verbose_name='subsection body title')


class BodySubSectionDescription(models.Model):
    description = models.TextField()
    subsection_body = models.ForeignKey(BodySubSection, on_delete=models.CASCADE,
                                        related_name='subsection_body_description')


"""
Section: Audience (*titles stay the same)

    9. Section Title 
    10. Business Decision Makers (body) *title stays the same
    11. Business Decision Makers Image (austin_airport_aus_advertising_business_image)
    12. Affluent Travelers (body) *title stays the same
    13. Affluent Travelers Image (austin_airport_aus_advertising_affluent_image)
    14. Early Tech Adopters (body) *title stays the same
    15. Early Tech Adopters Image (austin_airport_aus_advertising_tech_image)
    16. Leisure Travelers (body) *title stays the same
    17. Leisure Travelers Image (austin_airport_aus_advertising_leisure_image)
    18. Families (body) *title stays the same
    19. Families Image (austin_airport_aus_advertising_families_image)
    20. Students and Alumni (body) *title stays the same
    21. Students and Alumni Image (austin_airport_aus_advertising_students_image)
"""


class AudienceSection(models.Model):
    section_body = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_audience')
    title = models.CharField(max_length=255, verbose_name='subsection body title',
                             default='An audience for any campaign')


class AudienceSubSection(models.Model):
    audience_subsection_image_name = models.CharField(max_length=255, verbose_name='audience subsection image name')
    audience_body = models.ForeignKey(AudienceSection, on_delete=models.CASCADE,
                                      related_name='audience_subsection')


class AudienceSubSectionDescription(models.Model):
    description = models.TextField()
    audience_subsection_model = models.ForeignKey(AudienceSubSection, on_delete=models.CASCADE,
                                                  related_name='audience_subsection_descriptions')


"""
Section: Campaign Types (*tabs stay the same)

    22. Section Title
    23. B2B (title and body) *tabs stay the same
    24. B2B Image (austin_airport_aus_advertising_b2b_image)
    25. Conference Participants (title and body) *not tab
    26. Conference Participants Image (austin_airport_aus_advertising_conference_image)
    27. B2C (title and body) *not tab
    28. B2C Image (austin_airport_aus_advertising_b2c_image)
    29. Education (title and body) *not tab
    30. Education Image (austin_airport_aus_advertising_education_image)
    31. Tourism (title and body) *not tab
    32. Tourism Image (austin_airport_aus_advertising_tourism_image)
    33. Government (title and body) *not tab
    34. Government Image (austin_airport_aus_advertising_government_image)
    35. Luxury (title and body) *not tab
    36. Luxury Image (austin_airport_aus_advertising_luxury_image)
    37. Events (title and body) *not tab
    38. Events Image (austin_airport_aus_advertising_events_image)
    39. Entertainment (title and body) *not tab
    40. Entertainment Image (austin_airport_aus_advertising_entertainment_image)
    41. Financial and Crypto (title and body) *not tab
    42. Financial and Crypto Image (austin_airport_aus_advertising_financial_image)
    43. PSA & Non-Profits (title and body) *not tab
    44. PSA & Non-Profits Image (austin_airport_aus_advertising_psa_image)
    45. Healthcare (title and body) *not tab
    46. Healthcare Image (austin_airport_aus_advertising_healthcare_image)

"""


class CampaignTypesSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='campaign_types')
    title = models.CharField(max_length=255, verbose_name='section CampaignTypes title',
                             default='Airport Campaign Types')


class CampaignTypesHeroSection(models.Model):
    city_model = models.ForeignKey(CampaignTypesSection, on_delete=models.CASCADE,
                                   related_name='section_campaign_types')
    title = models.CharField(max_length=255)


class CampaignTypesSubSection(models.Model):
    subsection_body = models.ForeignKey(CampaignTypesHeroSection, on_delete=models.CASCADE,
                                        related_name='subsection_campaign_types')
    title = models.CharField(max_length=255, verbose_name='subsection campaign types title')
    image_name = models.CharField(max_length=255)


class CampaignTypesSubSectionDescription(models.Model):
    description = models.TextField()
    subsection_model = models.ForeignKey(CampaignTypesSubSection, on_delete=models.CASCADE,
                                         related_name='subsection_campaign_types_description')


"""

Section: Media Solutions

    47. Digital Spectaculars Image (austin_airport_aus_advertising_digital_spectacular_image)
    48. Digital Large Format Image (austin_airport_aus_advertising_digital_large_format_image)

"""


class MediaSolutionsSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='media_solutions')


class MediaSolutionsTabSection(models.Model):
    model_city = models.ForeignKey(MediaSolutionsSection, on_delete=models.CASCADE, related_name='media_solutions_tab')
    image_name = models.CharField(max_length=255)

################################################################################################################
class SectionHeroModel(models.Model):
    image_hero_url_jpg = models.URLField(blank=True)
    image_hero_url_webp = models.URLField(blank=True)
    hero_headline = models.CharField(max_length=255, verbose_name='Hero Headline: title')
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_hero_model')
    description = models.TextField()


class WhyAirport(models.Model):
    title = models.CharField(max_length=255, verbose_name='WhyAirport?')
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='why_airport')


class WhyAirportDescription(models.Model):
    description = models.TextField()
    why_airport = models.ForeignKey(WhyAirport, on_delete=models.CASCADE,
                                    related_name='why_airport_description')


class AboutAirport(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, )
    title = models.CharField(max_length=255, verbose_name='About City Airport?')


class AboutAirportDescription(models.Model):
    description = models.TextField()
    about_airport = models.ForeignKey(AboutAirport, on_delete=models.CASCADE,
                                      related_name='description_about_airport')

#
# class AboutCity(models.Model):
#     city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='about_city')
#     title = models.CharField(max_length=255, verbose_name='About City Airport?')
#
#
# class AboutCityDescription(models.Model):
#     description = models.TextField()
#     about_airport = models.ForeignKey(AboutCity, on_delete=models.CASCADE,
#                                       related_name='description_about_city')


# class City(models.Model):
#     name_city = models.CharField(max_length=255, verbose_name='name_city')
#     page_title = models.CharField(max_length=255, verbose_name='page_title')
#
#     def __str__(self):
#         return f'{self.name_city}'

#
# class HeroModel(models.Model):
#     hero_title = models.CharField(max_length=255, verbose_name='hero_title')
#     image_hero_url_webp = models.URLField(blank=True)
#     image_hero_url_jpg = models.URLField(blank=True)
#     city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hero_obj')
#
#     def save(self, force_insert=False, force_update=False,
#              using=None, update_fields=None):
#         list_image_file = 'home-hero3.jpg', 'home-hero3.webp'
#         list_name = []
#         for file in list_image_file:
#             basename = os.path.basename(file)
#             name, extension = os.path.splitext(basename)
#             new_basename_url = '/static/img/home/' + f"{name}_{self.city_model.name_city.lower()}{extension}"
#             list_name.append(new_basename_url)
#             # copy_and_rename_file(filename=file, arg=self.city_model.name_city.lower())
#         self.image_hero_url_jpg, self.image_hero_url_webp = list_name
#
#         # instance.save()
#         return super().save(force_insert=False, force_update=False, using=None, update_fields=None)


# class WhyAirport(models.Model):
#     city_model = models.ForeignKey(City, on_delete=models.CASCADE)
#     # description_city = models.TextField()


class WhyCityAirport(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='why_city_obj')
    why_title = models.CharField(max_length=255, verbose_name='Why City Airport?')
    description = models.TextField()


class AboutAirportCity(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='about_airport')
    about_title = models.CharField(max_length=255, verbose_name='About City Airport?')
    description = models.TextField()


class AboutCity(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='about_city_obj')
    about_title = models.CharField(max_length=255, verbose_name='About City')
    description = models.TextField()


# class DescriptionModelWhyAirport(models.Model):
#     object_model = models.ForeignKey(WhyAirport, on_delete=models.CASCADE, related_name='why_airports')
#
#
# class AirportAbstractModel(models.Model):
#     # title = models.CharField(max_length=255, default="Why Airport?")
#     page_title = models.ForeignKey(PageTitleModel, on_delete=models.CASCADE, default=11)
#
#     def __str__(self):
#         return '%s' % self.title


class DescriptionModel(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return '%s' % self.title


#
# class WhyAirport(AirportAbstractModel):
#     pass
#     # description_city = models.TextField()
#
#
# class DescriptionModelWhyAirport(DescriptionModel):
#     object_model = models.ForeignKey(WhyAirport, on_delete=models.CASCADE, related_name='why_airports')
#
#
# class CaseStudies(AirportAbstractModel):
#     pass
#
#
# class DescriptionModelCaseStudies(DescriptionModel):
#     object_model = models.ForeignKey(CaseStudies, on_delete=models.CASCADE, related_name='case_studies_airports')
#
#
# class AirportAudiencesModel(AirportAbstractModel):
#     pass
#
#
# class AirportAudiencesDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(AirportAudiencesModel, on_delete=models.CASCADE, related_name='airport_audiences')
#
#
# class AirportCampaignTypesModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Airport Campaign Types")
#
#
# class AirportCampaignTypesDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(AirportCampaignTypesModel, on_delete=models.CASCADE,
#                                      related_name='campaign_types_obj')
#
#
# class WhoWeAreModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Who We Are")
#
#
# class WhoWeAreModelDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(WhoWeAreModel, on_delete=models.CASCADE, related_name='who_we_are_obj')
#
#
# class AirportServedModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Airport Served")
#
#
# class AirportServedDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(AirportServedModel, on_delete=models.CASCADE, related_name='airport_served_obj')
#
#
# class DigitalSolutionsModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Digital Solutions")
#
#
# class DigitalSolutionsDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(DigitalSolutionsModel, on_delete=models.CASCADE,
#                                      related_name='digital_solutions_obj')
#
#
# class StaticSolutionsModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Static Solutions")
#
#
# class StaticSolutionsDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(StaticSolutionsModel, on_delete=models.CASCADE,
#                                      related_name='static_solutions_obj')
#
#
# class AirlineClubLoungesModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Airline Club Lounges")
#
#
# class AirlineClubLoungesDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(AirlineClubLoungesModel, on_delete=models.CASCADE,
#                                      related_name='airline_club_lounges_obj')
#
#
# class SecurityAreaModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Security Area")
#
#
# class SecurityAreaDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(SecurityAreaModel, on_delete=models.CASCADE,
#                                      related_name='security_area_obj')
#
#
# class WiFiSponsorshipsModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Security Area")
#
#
# class WiFiSponsorshipsDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(WiFiSponsorshipsModel, on_delete=models.CASCADE,
#                                      related_name='wifi_sponsorships_obj')
#
#
# class ExperientialModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Experiential")
#
#
# class ExperientialDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(ExperientialModel, on_delete=models.CASCADE,
#                                      related_name='experiential_obj')
#
#
# class ExteriorsModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="Exteriors")
#
#
# class ExteriorsDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(ExteriorsModel, on_delete=models.CASCADE,
#                                      related_name='exteriors_obj')
#
#
# class InFlightVideoModel(AirportAbstractModel):
#     title = models.CharField(max_length=255, default="In-Flight Video")
#
#
# class InFlightVideoModelDescriptionModel(DescriptionModel):
#     object_model = models.ForeignKey(InFlightVideoModel, on_delete=models.CASCADE,
#                                      related_name='in_flight_video_model_obj')


@receiver(post_save, sender=AboutCity)
def get_create_html(sender, instance, created, **kwargs):
    # list_of_models = ('AboutCity', 'AirportServedModel', 'City')
    # if sender.__name__ in list_of_models:
    #     return
    if created:
        city_model = instance.city_model
        name_city = city_model.name_city.lower()
        object_hero = city_model.hero_obj.first()
        dict_data_template = dict()
        dict_data_template['object_city'] = city_model
        dict_data_template['object_hero'] = object_hero
        dict_data_template['object_why_city_airport'] = city_model.why_city_obj.first()
        dict_data_template['object_about_city_airport'] = city_model.about_airport.first()
        dict_data_template['object_about_city'] = city_model.about_city_obj.first()
        dict_data_template['name_city'] = name_city

        list_image_file = 'home-hero3.jpg', 'home-hero3.webp'
        for file in list_image_file:
            copy_and_rename_file(filename=file, arg=name_city)

        name_template = settings.NAME_TEMPLATE
        from jinja2 import Environment, FileSystemLoader
        path = os.path.dirname(os.path.abspath(__file__))
        dict_fields = {f.name: getattr(instance, f.name) for f in instance._meta.get_fields() if f.name != 'id'}
        path_dir_template = "templates/app_air"
        env = Environment(
            autoescape=False,
            loader=FileSystemLoader(os.path.join(path, path_dir_template)),
            trim_blocks=False)
        # name_file = instance.page_title
        directory = os.path.join(path)
        os.makedirs(directory, exist_ok=True)
        template = env.get_template(name_template)
        output_from_parsed_template = template.render(**dict_data_template)
        # to save the results
        print(f"{directory}")
        path_templates = f"{directory}/templates/app_air/{name_city}.html"
        with open(path_templates, "w") as fh:
            fh.write(output_from_parsed_template)
        with open(f"{directory}/templates/app_air/includes/{name_city}.html", "w") as fh:
            fh.write(output_from_parsed_template)

        with open(path_templates, 'r+') as f:
            lines = f.readlines()
            f.seek(0)
            f.write('{% load static %}\n')
            f.write(''.join(lines))
        parse_file_compile(path_templates)
        replace_static_urls_in_html_file(path_templates)
