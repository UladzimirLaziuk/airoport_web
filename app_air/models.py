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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    def __str__(self):
        return f'{self.name_city}'


class HeroSection(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_hero')
    hero_image_name = models.CharField(max_length=255, verbose_name='hero image name')
    title = models.CharField(max_length=255, verbose_name='Hero Headline: title')

    def __str__(self):
        return f"HeroHeadline - {self.city_model.name_city}"
class HeroSubHeadline(models.Model):
    section_hero = models.ForeignKey(HeroSection, on_delete=models.CASCADE, related_name='section_hero_subheading')
    description = models.TextField()

    def __str__(self):
        return f"HeroSubHeadline - {self.section_hero.city_model.name_city}"
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
    section_name = models.CharField(max_length=255, verbose_name='WhyAirport?', default='WhyAirport?')

    def __str__(self):
        return f"BodySection - {self.city_model.name_city}"


class BodySubSection(models.Model):
    section_body = models.ForeignKey(BodySection, on_delete=models.CASCADE, related_name='tabs')
    title = models.CharField(max_length=255, verbose_name='subsection body title')

    def __str__(self):
        return f"BodySubSection - {self.section_body.city_model.name_city}"


class BodySubSectionDescription(models.Model):
    text = models.TextField()
    subsection_body = models.ForeignKey(BodySubSection, on_delete=models.CASCADE,
                                        related_name='paragraphs')

    def __str__(self):
        return f"BodySubSectionDescription - {self.subsection_body.section_body.city_model.name_city}"


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

    def __str__(self):
        return f"AudienceSection- {self.section_body.name_city}"


class AudienceSubSection(models.Model):
    image_name = models.CharField(max_length=255, verbose_name='audience subsection image name')
    audience_body = models.ForeignKey(AudienceSection, on_delete=models.CASCADE,
                                      related_name='accordions')

    def __str__(self):
        return f"AudienceSubSection - {self.audience_body.section_body.name_city}"


class AudienceSubSectionDescription(models.Model):
    text = models.TextField()
    audience_subsection_model = models.ForeignKey(AudienceSubSection, on_delete=models.CASCADE,
                                                  related_name='paragraphs')

    def __str__(self):
        return f"AudienceSubSectionDescription - {self.audience_subsection_model.audience_body.section_body.name_city}"


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

    def __str__(self):
        return f"CampaignTypesSection - {self.model_city.name_city}"


# class CampaignTypesHeroSection(models.Model):
#     city_model = models.ForeignKey(CampaignTypesSection, on_delete=models.CASCADE,
#                                    related_name='section_campaign_types')
#     title = models.CharField(max_length=255)


class CampaignTypesSubSection(models.Model):
    subsection_body = models.ForeignKey(CampaignTypesSection, on_delete=models.CASCADE,
                                        related_name='subsection_campaign_types')
    title = models.CharField(max_length=255, verbose_name='subsection campaign types title')
    image_name = models.CharField(max_length=255)

    def __str__(self):
        return f"CampaignTypesSubSection - {self.subsection_body.model_city.name_city}"


class CampaignTypesSubSectionDescription(models.Model):
    description = models.TextField()
    subsection_model = models.ForeignKey(CampaignTypesSubSection, on_delete=models.CASCADE,
                                         related_name='subsection_campaign_types_description')

    def __str__(self):
        return f"CampaignTypesSubSectionDescription - {self.subsection_model.subsection_body.model_city.name_city}"


"""

Section: Media Solutions

    47. Digital Spectaculars Image (austin_airport_aus_advertising_digital_spectacular_image)
    48. Digital Large Format Image (austin_airport_aus_advertising_digital_large_format_image)

"""


class MediaSolutionsSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_media_solutions')

    def __str__(self):
        return f"MediaSolutionsSection - {self.model_city.name_city}"


class MediaSolutionsTabSection(models.Model):
    model_section = models.ForeignKey(MediaSolutionsSection, on_delete=models.CASCADE,
                                      related_name='media_solutions_tab')
    image_name = models.CharField(max_length=255)

    def __str__(self):
        return f"MediaSolutionsTabSection - {self.model_section.model_city.name_city}"


################################################################################################################
def get_dict(id_):
    dict_data_template = dict()
    obj_city = City.objects.filter(pk=id_).first()
    tabs = BodySection.objects.filter(city_model=id_).get().tabs.all()
    dict_data_template['name_city'] = obj_city.name_city
    dict_data_template['object_city'] = obj_city
    dict_data_template['object_hero'] = obj_city.section_hero.first()
    name_section = BodySection.objects.values_list('section_name', flat=True)
    dict_data_template['body_subsection_object'] = tabs

    # dict_data_template['object_why_city_airport'] = tabs[0]
    # dict_data_template['object_about_city_airport'] = tabs[1]
    # dict_data_template['object_about_city'] = tabs[2]

    dict_data_template['obj_why_city_airport'] = BodySection.objects.first()
    return dict_data_template


from django.template import loader
# @receiver(post_save)
# def get_create_html(sender, instance, created, **kwargs):
#         list_of_models = ('MediaSolutionsSection', 'MediaSolutionsTabSection')
#         if sender.__name__ in list_of_models:
#             context = get_dict(id_=1)
#             content = loader.render_to_string('app_air/index.html', context,
#                                               request=None, using=None)
#             with open('/home/vladimir/airoport_dir/airoport/probe.html', "w") as fh:
#                 fh.write(content)


# city_model = City.objects.first()
# name_city = city_model.name_city
#
# dict_data_template = dict()
# dict_data_template['object_city'] = city_model
# dict_data_template['object_hero'] = object_hero
# dict_data_template['object_why_city_airport'] = city_model.why_city_obj.first()
# dict_data_template['object_about_city_airport'] = city_model.about_airport.first()
# dict_data_template['object_about_city'] = city_model.about_city_obj.first()
# dict_data_template['name_city'] = name_city
# dict_data_template['cities'] = MediaSolutionsSection.objects.all()


# list_image_file = 'home-hero3.jpg', 'home-hero3.webp'
# for file in list_image_file:
#     copy_and_rename_file(filename=file, arg=name_city)
#
# name_template = settings.NAME_TEMPLATE
# from jinja2 import Environment, FileSystemLoader
# path = os.path.dirname(os.path.abspath(__file__))
# dict_fields = {f.name: getattr(instance, f.name) for f in instance._meta.get_fields() if f.name != 'id'}
# path_dir_template = "templates/app_air"
# env = Environment(
#     autoescape=False,
#     loader=FileSystemLoader(os.path.join(path, path_dir_template)),
#     trim_blocks=False)
# # name_file = instance.page_title
# directory = os.path.join(path)
# os.makedirs(directory, exist_ok=True)
# template = env.get_template(name_template)
# output_from_parsed_template = template.render(**dict_data_template)
# # to save the results
# print(f"{directory}")
# path_templates = f"{directory}/templates/app_air/{name_city}.html"
# with open(path_templates, "w") as fh:
#     fh.write(output_from_parsed_template)
# with open(f"{directory}/templates/app_air/includes/{name_city}.html", "w") as fh:
#     fh.write(output_from_parsed_template)
#
# with open(path_templates, 'r+') as f:
#     lines = f.readlines()
#     f.seek(0)
#     f.write('{% load static %}\n')
#     f.write(''.join(lines))
# parse_file_compile(path_templates)
# replace_static_urls_in_html_file(path_templates)

# @receiver(post_save)
# def get_create_html(sender, instance, created, **kwargs):
#     list_of_models = ('MediaSolutionsSection', 'MediaSolutionsTabSection')
#     if sender.__name__ in list_of_models:
#         if created:
#             model_name = sender.__name__.lower()
#             # получаем все поля связанные с моделью
#             related_fields = [field for field in instance._meta.get_fields() if field.is_relation]
#             # проходимся по всем связанным полям
#             for field in related_fields:
#                 related_model = field.related_model
#                 related_model_name = related_model.__name__.lower()
#                 # related_name = related_model._meta.get_field(related_model_name).related_name
#
#                 if hasattr(field, 'related_name'):
#                     related_objects = getattr(instance, field.related_name).all()
#                     print(related_objects)

# if hasattr(instance, 'model_section'):
#     # related_objects = getattr(instance, field.related_name).all()
#     print('model_section')
# related_name = related_model._meta.get_field(related_model_name).related_name
# if hasattr(instance, field.name):
#     # related_objects = getattr(instance, field.related_name).all()
#     print(field)

# related_name = Pet._meta.get_field('person').remote_field.get_accessor_name()
#
# related_query_name = Pet._meta.get_field('person').related_query_name()
# получаем все объекты связанные с текущим объектом instance
# related_objects = getattr(instance, related_model_name + '_set').all()
# city_model = instance.city_model
# name_city = city_model.name_city.lower()
# object_hero = city_model.hero_obj.first()
# dict_data_template = dict()
# dict_data_template['object_city'] = city_model
# dict_data_template['object_hero'] = object_hero
# dict_data_template['object_why_city_airport'] = city_model.why_city_obj.first()
# dict_data_template['object_about_city_airport'] = city_model.about_airport.first()
# dict_data_template['object_about_city'] = city_model.about_city_obj.first()
# dict_data_template['name_city'] = name_city
#
# list_image_file = 'home-hero3.jpg', 'home-hero3.webp'
# for file in list_image_file:
#     copy_and_rename_file(filename=file, arg=name_city)
#
# name_template = settings.NAME_TEMPLATE
# from jinja2 import Environment, FileSystemLoader
# path = os.path.dirname(os.path.abspath(__file__))
# dict_fields = {f.name: getattr(instance, f.name) for f in instance._meta.get_fields() if f.name != 'id'}
# path_dir_template = "templates/app_air"
# env = Environment(
#     autoescape=False,
#     loader=FileSystemLoader(os.path.join(path, path_dir_template)),
#     trim_blocks=False)
# # name_file = instance.page_title
# directory = os.path.join(path)
# os.makedirs(directory, exist_ok=True)
# template = env.get_template(name_template)
# output_from_parsed_template = template.render(**dict_data_template)
# # to save the results
# print(f"{directory}")
# path_templates = f"{directory}/templates/app_air/{name_city}.html"
# with open(path_templates, "w") as fh:
#     fh.write(output_from_parsed_template)
# with open(f"{directory}/templates/app_air/includes/{name_city}.html", "w") as fh:
#     fh.write(output_from_parsed_template)
#
# with open(path_templates, 'r+') as f:
#     lines = f.readlines()
#     f.seek(0)
#     f.write('{% load static %}\n')
#     f.write(''.join(lines))
# parse_file_compile(path_templates)
# replace_static_urls_in_html_file(path_templates)

# @receiver(post_save, sender=AboutCity)
# def get_create_html(sender, instance, created, **kwargs):
#     # list_of_models = ('AboutCity', 'AirportServedModel', 'City')
#     # if sender.__name__ in list_of_models:
#     #     return
#     if created:
#         city_model = instance.city_model
#         name_city = city_model.name_city.lower()
#         object_hero = city_model.hero_obj.first()
#         dict_data_template = dict()
#         dict_data_template['object_city'] = city_model
#         dict_data_template['object_hero'] = object_hero
#         dict_data_template['object_why_city_airport'] = city_model.why_city_obj.first()
#         dict_data_template['object_about_city_airport'] = city_model.about_airport.first()
#         dict_data_template['object_about_city'] = city_model.about_city_obj.first()
#         dict_data_template['name_city'] = name_city
#
#         list_image_file = 'home-hero3.jpg', 'home-hero3.webp'
#         for file in list_image_file:
#             copy_and_rename_file(filename=file, arg=name_city)
#
#         name_template = settings.NAME_TEMPLATE
#         from jinja2 import Environment, FileSystemLoader
#         path = os.path.dirname(os.path.abspath(__file__))
#         dict_fields = {f.name: getattr(instance, f.name) for f in instance._meta.get_fields() if f.name != 'id'}
#         path_dir_template = "templates/app_air"
#         env = Environment(
#             autoescape=False,
#             loader=FileSystemLoader(os.path.join(path, path_dir_template)),
#             trim_blocks=False)
#         # name_file = instance.page_title
#         directory = os.path.join(path)
#         os.makedirs(directory, exist_ok=True)
#         template = env.get_template(name_template)
#         output_from_parsed_template = template.render(**dict_data_template)
#         # to save the results
#         print(f"{directory}")
#         path_templates = f"{directory}/templates/app_air/{name_city}.html"
#         with open(path_templates, "w") as fh:
#             fh.write(output_from_parsed_template)
#         with open(f"{directory}/templates/app_air/includes/{name_city}.html", "w") as fh:
#             fh.write(output_from_parsed_template)
#
#         with open(path_templates, 'r+') as f:
#             lines = f.readlines()
#             f.seek(0)
#             f.write('{% load static %}\n')
#             f.write(''.join(lines))
#         parse_file_compile(path_templates)
#         replace_static_urls_in_html_file(path_templates)
