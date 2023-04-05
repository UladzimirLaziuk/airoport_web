import os
import shutil

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from airoport import settings
from app_air.utils_copy_file import copy_and_rename_file, parse_file_compile, replace_static_urls_in_html_file
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site




class City(models.Model):
    name_city = models.CharField(max_length=255, verbose_name='name_city')
    page_title = models.CharField(max_length=255, verbose_name='page_title')


class HeroModel(models.Model):
    hero_title = models.CharField(max_length=255, verbose_name='hero_title')
    # hero_image_name = models.CharField(max_length=255, verbose_name='hero_image_name')
    city_model = models.ForeignKey(City, on_delete=models.CASCADE)


# class WhyAirport(models.Model):
#     city_model = models.ForeignKey(City, on_delete=models.CASCADE)
#     # description_city = models.TextField()


class WhyCityAirport(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE)
    why_title = models.CharField(max_length=255, verbose_name='Why City Airport?')
    description = models.TextField()


class AboutAirportCity(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE)
    about_title = models.CharField(max_length=255, verbose_name='About City Airport?')
    description = models.TextField()


class AboutCity(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE)
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

    city_model = instance.city_model
    name_city = city_model.name_city.lower()
    object_hero = city_model.heromodel_set.first()
    dict_data_template = dict()
    dict_data_template['object_city'] = city_model
    dict_data_template['object_hero'] = object_hero
    dict_data_template['object_why_city_airport'] = city_model.whycityairport_set.first()
    dict_data_template['object_about_city_airport'] = city_model.aboutairportcity_set.first()
    dict_data_template['object_about_city'] = city_model.aboutcity_set.first()
    dict_data_template['name_city'] = name_city

    list_image_file = 'home-hero3.jpg', 'home-hero3.webp'
    for file in list_image_file:
        copy_and_rename_file(filename=file, arg=name_city)
    # current_site = get_current_site(None)
    # messages.add_message(None, messages.SUCCESS, f"Объект успешно создан на сайте {current_site.name}")
    if created:
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

