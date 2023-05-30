import os
import shutil

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse

from airoport import settings
from app_air.utils_copy_file import copy_and_rename_file, parse_file_compile, replace_static_urls_in_html_file, \
    copy_and_full_rename, get_list_jpg_folder, get_jpg_default, get_jpg_default_bs4
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader

###########################################################################################################
"""Section Title: Hero

    1. Page Title: 
    2. Hero Image (austin_airport_advertising_hero_main)
    3. Hero Headline: title
    4. Hero Sub Headline: description"""


class MyModelMixin(object):
    @property
    def get_id_city_model(self):
        return self.model_section.model_city.id

    @property
    def get_name_city(self):
        return self.model_section.model_city.name_city.lower()

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     name_image = self.image_name
    #     if '{}' in name_image:
    #         template_name = name_image.format(self.model_section.model_city.name_city.lower(),
    #                                           self.model_section.model_city.code_city.lower())
    #     else:
    #         template_name = name_image
    #     self.image_name = template_name
    #     copy_and_full_rename(self.file_name, arg=template_name)
    #     return super().save(force_insert=force_insert, force_update=force_update, using=using,
    #                         update_fields=update_fields)
    def save(self, *args, **kwargs):
        if hasattr(self, 'text'):
            if '<p>' not in self.text:
                string_text = ''
                for paragraph in self.text.strip().split("\n"):
                    if not paragraph.strip():
                        continue
                    string_text += f'\n<p>{paragraph}</p>'
                self.text = string_text.strip()
            else:
                self.text = self.text.strip()
        is_new = not bool(self.pk)
        if not self.file_name and is_new:
            index = self.get_count_parent_model()
            path_template = os.path.join(settings.BASE_DIR, 'app_air/templates/')
            path_file = os.path.join(path_template, 'app_air/index_original.html')

            # folder_path = os.path.join(settings.BASE_DIR, 'static/img/home/articles', self.photo_folder)
            # patt_search = rf'img/home/articles/{self.photo_folder}'
            # patt_search = self.patt_search
            self.file_name = get_jpg_default_bs4(path_file=path_file, id_search=self.patt_search, index=index)

            self.image_name = self.get_image_name(self.image_name, self.file_name)
            copy_and_full_rename(self.file_name, arg=self.image_name)
        return super().save(*args, **kwargs)


# atlanta_airport_atl_advertising_business_image
class City(models.Model):
    name_city = models.CharField(max_length=255, verbose_name='name_city')
    code_city = models.CharField(max_length=255, verbose_name='code_city')
    page_title = models.CharField(max_length=255, verbose_name='Page Title')

    def save(self, *args, **kwargs):
        self.name_city = '-'.join(self.name_city.strip().split(' ')).lower()
        return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.name_city

    def __str__(self):
        return f'{self.name_city}'

    # class Meta:
    #     verbose_name = 'page title'
    #     verbose_name_plural = '1 Page Title'


class HeroSection(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_hero')
    hero_image_name = models.CharField(max_length=255, verbose_name='hero image name',
                                       default='{}_airport_advertising_hero_main')
    title = models.CharField(max_length=255, verbose_name='Hero Headline: title')
    file_name = models.CharField(max_length=50, blank=True, default='home-hero3.jpg')

    def save(self, *args, **kwargs):
        if '{}' in self.hero_image_name:
            template_name = self.hero_image_name.format(self.city_model.name_city.lower(),
                                                        self.city_model.code_city.lower())
        else:
            template_name = self.hero_image_name
        self.hero_image_name = template_name
        copy_and_full_rename(self.file_name, arg=template_name)
        return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.city_model.name_city.lower()

    def __str__(self):
        return f"HeroHeadline - {self.city_model.name_city}"

    # class Meta:
    #     verbose_name = 'Hero Image '
    #     verbose_name_plural = '2. Hero Image'


class HeroSubHeadline(models.Model):
    section_hero = models.OneToOneField(HeroSection, on_delete=models.CASCADE, related_name='section_hero_subheading')
    description = models.TextField()

    @property
    def get_name_city(self):
        return self.section_hero.city_model.name_city.lower()

    def __str__(self):
        return f"HeroSubHeadline - {self.section_hero.city_model.name_city}"

    # def save(self, *args, **kwargs):
    #     string_text = ''
    #     if '<p>' not in self.description:
    #         for paragraph in self.description.strip().split("\n"):
    #             if not paragraph.strip():
    #                 continue
    #             string_text += f'\n<p>{paragraph}</p>'
    #         self.description = string_text.strip()
    #     return super().save(*args, **kwargs)
    # class Meta:
    #     verbose_name = 'Hero Sub Headline'
    #     verbose_name_plural = '3. Hero Sub Headlines'


'''
Section: Body

    5. Why Airport? (title and body fields)
    6. Airport (title and body fields)
    7. City (title and body fields)
    8. Main Body Image (austin_airport_aus_advertising_body_image)

'''


class BodySection(models.Model):
    city_model = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_body')
    body_image_name = models.CharField(max_length=255, verbose_name='main body image name',
                                       default='{}_airport_{}_advertising_body_image')
    section_name = models.CharField(max_length=255, verbose_name='WhyAirport?', default='WhyAirport?')
    file_name = models.CharField(max_length=50, blank=True, default='why_airport_advertising.jpg')

    def save(self, *args, **kwargs):
        name_image = self.body_image_name
        if '{}' in name_image:
            template_name = name_image.format(self.city_model.name_city.lower(),
                                              self.city_model.code_city.lower())
        else:
            template_name = name_image
        self.body_image_name = template_name
        copy_and_full_rename(self.file_name, arg=template_name)
        return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.city_model.name_city.lower()

    def __str__(self):
        return f"BodySection - {self.city_model.name_city}"


class BodySubSection(models.Model):
    section_body = models.ForeignKey(BodySection, on_delete=models.CASCADE, related_name='tabs')
    title = models.CharField(max_length=255, verbose_name='subsection body title')
    text = models.TextField()

    @property
    def get_name_city(self):
        return self.section_body.city_model.name_city.lower()

    def save(self, *args, **kwargs):
        string_text = ''
        if '<p>' not in self.text:
            for paragraph in self.text.strip().split("\n"):
                if not paragraph.strip():
                    continue
                string_text += f'\n<p>{paragraph}</p>'
            self.text = string_text.strip()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.section_body.city_model.name_city}"


class BodySubSectionDescription(models.Model):
    text = models.TextField()
    subsection_body = models.ForeignKey(BodySubSection, on_delete=models.CASCADE,
                                        related_name='paragraphs')

    def save(self, *args, **kwargs):
        string_text = ''
        if '<p>' not in self.text:
            for paragraph in self.text.strip().split("\n"):
                if not paragraph.strip():
                    continue
                string_text += f'\n<p>{paragraph}</p>'
            self.text = string_text.strip()
        return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.subsection_body.section_body.city_model.name_city.lower()

    @property
    def get_id_city_model(self):
        return self.subsection_body.section_body.city_model.id

    def __str__(self):
        return f"{self.subsection_body.title} - {self.subsection_body.section_body.city_model.name_city}"


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

    @property
    def get_name_city(self):
        return self.section_body.name_city.lower()

    def __str__(self):
        return f"AudienceSection- {self.section_body.name_city}"


class AudienceSubSection(MyModelMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='audiences')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='audience')
    image_name = models.CharField(max_length=255, verbose_name='audience subsection image name',
                                  default='{}_airport_{}_advertising_{}_image')
    audience_body = models.ForeignKey(AudienceSection, on_delete=models.CASCADE,
                                      related_name='accordions')
    text = models.TextField()
    file_name = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255)

    def get_count_parent_model(self):
        return self.audience_body.accordions.count()

    @staticmethod
    def get_first_element(filename):
        elements = filename.split('_')

        first_element = elements[0]

        if len(first_element) < 6 and len(elements) > 1:
            # first_element = '_'.join([first_element, elements[1]])
            return elements[1]

        return first_element

    @property
    def get_id_city_model(self):
        return self.audience_body.section_body.id

    def get_image_name(self, image_name, filename):
        filename = os.path.basename(filename)
        # name, file_extension = os.path.splitext(filename)
        part_name = self.get_first_element(filename)
        return image_name.format(self.get_name_city, self.get_code_city, part_name)

    # def save(self, *args, **kwargs):
    #     if not self.file_name:
    #         index = self.get_count_parent_model()
    #         path_template = os.path.join(settings.BASE_DIR, 'app_air/templates/')
    #         path_file = os.path.join(path_template, 'app_air/index_original.html')
    #
    #         # folder_path = os.path.join(settings.BASE_DIR, 'static/img/home/articles', self.photo_folder)
    #         patt_search = rf'img/home/articles/{self.photo_folder}'
    #         self.file_name = get_jpg_default(path_file=path_file, patt_search=patt_search, index=index)
    #
    #     name_image = self.image_name
    #     if '{}' in name_image:
    #         template_name = name_image.format(self.audience_body.section_body.name_city.lower(),
    #                                           self.audience_body.section_body.code_city.lower())
    #     else:
    #         template_name = name_image
    #     self.image_name = template_name
    #     copy_and_full_rename(self.file_name, arg=template_name)
    #     return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.audience_body.section_body.name_city.lower()

    @property
    def get_code_city(self):
        return self.audience_body.section_body.code_city.lower()

    def __str__(self):
        return f"AudienceSubSection - {self.audience_body.section_body.name_city}-" \
               f"{'-'.join(self.image_name.split('_')[-2:])}"


class AudienceSubSectionDescription(models.Model):
    text = models.TextField()
    audience_subsection_model = models.ForeignKey(AudienceSubSection, on_delete=models.CASCADE,
                                                  related_name='paragraphs')

    def save(self, *args, **kwargs):
        string_text = ''
        if '<p>' not in self.text:
            for paragraph in self.text.strip().split("\n"):
                string_text += f'\n<p>{paragraph}</p>'
            self.text = string_text.strip()
        return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.audience_subsection_model.audience_body.section_body.name_city.lower()

    def __str__(self):
        return f"AudienceSubSectionDescription -" \
               f" {self.audience_subsection_model.audience_body.section_body.name_city}"


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
                             default='An advertisers by category')

    @property
    def get_name_city(self):
        return self.model_city.name_city.lower()

    def __str__(self):
        return f"CampaignTypesSection - {self.model_city.name_city}"


# class CampaignTypesHeroSection(models.Model):
#     city_model = models.ForeignKey(CampaignTypesSection, on_delete=models.CASCADE,
#                                    related_name='section_campaign_types')
#     title = models.CharField(max_length=255)


class CampaignTypesSubSection(MyModelMixin, models.Model):
    B2B = 'b2b'
    CONFERENCE_PARTICIPANTS = 'conference_participants'
    B2C = 'b2c'
    Education = 'education'
    Tourism = 'tourism'
    Government = 'government'
    Luxury = 'luxury'
    Events = 'events'
    Entertainment = 'entertainment'
    Financial_and_Crypto = 'financial_and_crypto'
    PSA___Non_Profits = 'psa_non_profits'
    Healthcare = 'healthcare'

    MY_CHOICES = (
        (B2B, 'B2B'),
        (CONFERENCE_PARTICIPANTS, 'Conference Participants'),
        (B2C, 'B2C'),
        (Education, 'Education'),
        (Tourism, 'Tourism'),
        (Government, 'Government'),
        (Luxury, 'Luxury'),
        (Events, 'Events'),
        (Entertainment, 'Entertainment'),
        (Financial_and_Crypto, 'Financial and Crypto'),
        (PSA___Non_Profits, 'PSA & Non-Profits'),
        (Healthcare, 'Healthcare'),

    )
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='advertisers')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='advertisers')
    tag_name = models.CharField(max_length=100, choices=MY_CHOICES)

    text = models.TextField()
    subsection_body = models.ForeignKey(CampaignTypesSection, on_delete=models.CASCADE,
                                        related_name='subsection_campaign_types')
    title = models.CharField(max_length=255, verbose_name='subsection campaign types title')

    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')
    file_name = models.CharField(max_length=50, blank=True)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     name_image = self.image_name
    #     if '{}' in name_image:
    #         template_name = name_image.format(self.subsection_body.model_city.name_city.lower(),
    #                                           self.subsection_body.model_city.code_city.lower())
    #     else:
    #         template_name = name_image
    #     self.image_name = template_name
    #     copy_and_full_rename(self.file_name, arg=template_name)
    #     return super().save(force_insert=False, force_update=False, using=None, update_fields=None)

    @property
    def get_tag_name_html_display(self):
        return self.get_tag_name_display()

    @property
    def get_name_city(self):
        return self.subsection_body.model_city.name_city.lower()

    def get_count_parent_model(self):
        return self.subsection_body.subsection_campaign_types.count()

    @property
    def get_id_city_model(self):
        return self.subsection_body.model_city.id

    @property
    def get_code_city(self):
        return self.subsection_body.model_city.code_city.lower()

    @staticmethod
    def get_first_element(filename):
        elements = filename.split('_')

        first_element = elements[0]

        if len(first_element) < 6 and len(elements) > 1:
            # first_element = '_'.join([first_element, elements[1]])
            return elements[1]

        return first_element

    def get_image_name(self, image_name, *args):
        return image_name.format(self.get_name_city, self.get_code_city, self.tag_name)

    def __str__(self):
        return f"CampaignTypesSubSection - {self.subsection_body.model_city.name_city}-" \
               f"{'-'.join(self.image_name.split('_')[-2:])}"


class CampaignTypesSubSectionDescription(models.Model):
    description = models.TextField()
    subsection_model = models.ForeignKey(CampaignTypesSubSection, on_delete=models.CASCADE,
                                         related_name='subsection_campaign_types_description')

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     self.count_paragraphs += self.subsection_model.subsection_campaign_types_description.count()
    #     return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
    def save(self, *args, **kwargs):
        string_text = ''
        if '<p>' not in self.description:
            for paragraph in self.description.strip().split("\n"):
                string_text += f'\n<p>{paragraph}</p>'
            self.description = string_text.strip()
        return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.subsection_model.subsection_body.model_city.name_city.lower()

    def __str__(self):
        return f"CampaignTypesSubSectionDescription -" \
               f" {self.subsection_model.subsection_body.model_city.name_city}" \
               f"-{'-'.join(self.subsection_model.image_name.split('_')[-2:])}"


"""

Section: Media Solutions

    47. Digital Spectaculars Image (austin_airport_aus_advertising_digital_spectacular_image)
    48. Digital Large Format Image (austin_airport_aus_advertising_digital_large_format_image)

"""


class MediaSolutionsSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_media_solutions')

    @property
    def get_name_city(self):
        return self.model_city.name_city.lower()

    def __str__(self):
        return f"MediaSolutionsSection - {self.model_city.name_city}"


class SolutionMixin:

    def get_image_name(self, image_name, *args):
        basename = os.path.basename(self.file_name)
        name_part = basename.split('a1')[0]
        return image_name.format(self.get_name_city, self.get_code_city, name_part)

    @property
    def get_code_city(self):
        return self.model_section.model_city.code_city.lower()

    @property
    def get_name_city(self):
        return self.model_section.model_city.name_city.lower()

    @property
    def get_id_city_model(self):
        return self.model_section.model_city.id

    # def get_count_parent_model(self):
    #     return self.model_section.media_solutions_tab.count()


# Digital Spectaculars Image (austin_airport_aus_advertising_digital_spectacular_image)
class MediaSolutionsTabSection(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='digital-solutions0')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(MediaSolutionsSection, on_delete=models.CASCADE,
                                      related_name='media_solutions_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     name_image = self.image_name
    #     if '{}' in name_image:
    #         template_name = name_image.format(self.model_section.model_city.name_city.lower(),
    #                                           self.model_section.model_city.code_city.lower())
    #     else:
    #         template_name = name_image
    #     self.image_name = template_name
    #     copy_and_full_rename(self.file_name, arg=template_name)
    #     return super().save(force_insert=False, force_update=False, using=None, update_fields=None)
    # def get_image_name(self, image_name):
    #     name_part = self.file_name.split('a1')[0] + 'image'
    #     return image_name.format(self.get_name_city, self.get_code_city, name_part)
    #
    # def get_code_city(self):
    #     return self.subsection_body.model_city.code_city
    #
    # @property
    # def get_name_city(self):
    #     return self.model_section.model_city.name_city
    #
    # def get_id_city_model(self):
    #     return self.model_section.model_city.id
    #
    def get_count_parent_model(self):
        return self.model_section.media_solutions_tab.count()

    def __str__(self):
        return f"MediaSolutionsTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"

    # class Meta:
    #     abstract=True


#

class StaticSolutions(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_static_solutions')

    @property
    def get_name_city(self):
        return self.model_city.name_city.lower()

    def __str__(self):
        return f"StaticSolutionsSection - {self.model_city.name_city}"


class StaticSolutionsTabSection(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='static-solutions1')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(StaticSolutions, on_delete=models.CASCADE,
                                      related_name='static_solutions_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    def get_count_parent_model(self):
        return self.model_section.static_solutions_tab.count()

    def __str__(self):
        return f"StaticSolutionsTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"


class AirlineClubLoungesSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_airline_club_lounges')

    @property
    def get_name_city(self):
        return self.model_city.name_city

    def __str__(self):
        return f"AirlineClubLoungesSection - {self.model_city.name_city}"


class AirlineClubLoungesTabSection(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='airline-club-lounges2')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(AirlineClubLoungesSection, on_delete=models.CASCADE,
                                      related_name='airline_club_lounges_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    def get_count_parent_model(self):
        return self.model_section.airline_club_lounges_tab.count()

    def __str__(self):
        return f"AirlineClubLoungesTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"


class SecurityAreaSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_security_area')

    @property
    def get_name_city(self):
        return self.model_city.name_city

    def __str__(self):
        return f"SecurityAreaSection - {self.model_city.name_city}"


class SecurityAreaSectionTabSection(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='security-area3')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(SecurityAreaSection, on_delete=models.CASCADE,
                                      related_name='section_security_area_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    def get_count_parent_model(self):
        return self.model_section.section_security_area_tab.count()

    def __str__(self):
        return f"SecurityAreaSectionTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"


class WiFiSponsorShipsSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_wifi_sponsorships')

    @property
    def get_name_city(self):
        return self.model_city.name_city

    def __str__(self):
        return f"WiFiSponsorshipsSection - {self.model_city.name_city}"


class WiFiSponsorShipsSectionTab(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='wifi-sponsorships4')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(WiFiSponsorShipsSection, on_delete=models.CASCADE,
                                      related_name='section_wifi_sponsorships_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    def get_count_parent_model(self):
        return self.model_section.section_wifi_sponsorships_tab.count()

    def __str__(self):
        return f"WiFiSponsorshipsTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"


class ExperientialSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_experiential')

    @property
    def get_name_city(self):
        return self.model_city.name_city

    def __str__(self):
        return f"SecurityAreaSection - {self.model_city.name_city}"


class ExperientialTabSection(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='experiential5')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(ExperientialSection, on_delete=models.CASCADE,
                                      related_name='section_experiential_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    def get_count_parent_model(self):
        return self.model_section.section_experiential_tab.count()

    def __str__(self):
        return f"ExperientialTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"


# Exteriors


class ExteriorsSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_exteriors')

    @property
    def get_name_city(self):
        return self.model_city.name_city

    def __str__(self):
        return f"ExteriorsSection - {self.model_city.name_city}"


class ExteriorsTabSection(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='exteriors6')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(ExteriorsSection, on_delete=models.CASCADE,
                                      related_name='section_exteriors_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    def get_count_parent_model(self):
        return self.model_section.section_exteriors_tab.count()

    def __str__(self):
        return f"ExteriorsTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"


#
# # In-Flight Video
#
class InFlightVideoSection(models.Model):
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_in_flight_video')

    @property
    def get_name_city(self):
        return self.model_city.name_city

    def __str__(self):
        return f"ExteriorsSection - {self.model_city.name_city}"


class InFlightVideoTabSection(MyModelMixin, SolutionMixin, models.Model):
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='in-flight-video7')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='solutions')
    model_section = models.ForeignKey(InFlightVideoSection, on_delete=models.CASCADE,
                                      related_name='section_in_flight_video_tab')
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')

    file_name = models.CharField(max_length=50, blank=True)

    def get_count_parent_model(self):
        return self.model_section.section_in_flight_video_tab.count()

    def __str__(self):
        return f"InFlightVideoTabSection - {self.model_section.model_city.name_city}" \
               f"-{'-'.join(self.image_name.split('_')[-2:])}"


#

################################################################################################################
def get_dict(id_):
    dict_data_template = dict()
    obj_city = City.objects.filter(pk=id_).first()  # TODO

    dict_data_template['name_city'] = obj_city.name_city.lower()
    dict_data_template['object_city'] = obj_city
    dict_data_template['object_hero'] = obj_city.section_hero.first()
    name_section = BodySection.objects.values_list('section_name', flat=True)

    body = BodySection.objects.filter(city_model=id_)
    if body.exists():
        tabs = body.get().tabs.all()[:3]
        dict_data_template['body_subsection_object'] = tabs
        dict_data_template['body_image_name'] = body.get().body_image_name
        for name, tab in zip(tabs, ('object_why_city_airport', 'object_about_city_airport', 'object_about_city')):
            dict_data_template[name] = tab
            print(dict_data_template)
    # dict_data_template['object_why_city_airport'] = tabs[0]
    # dict_data_template['object_about_city_airport'] = tabs[1]
    # dict_data_template['object_about_city'] = tabs[2]

    dict_data_template['obj_why_city_airport'] = BodySection.objects.first()

    # AudienceSection
    audience_section = AudienceSection.objects.filter(section_body=id_)
    if audience_section.exists():
        audiencesection = audience_section.first()
        dict_data_template['audience_section_title'] = audiencesection.title

        dict_data_template['list_accordions'] = audiencesection.accordions.all()
    # model_campaign_types = CampaignTypesSection.objects.filter(model_city=id_).first()
    camp = CampaignTypesSection.objects.filter(model_city=id_)
    if camp.exists():
        model_campaign_types = camp.first()

        list_tags_campaign_types = CampaignTypesSection.objects.values_list('subsection_campaign_types__tag_name',
                                                                            flat=True)

        dict_data_template['list_title_campaign_types'] = list_tags_campaign_types
        dict_data_template['objects_subsection_campaign_types'] = model_campaign_types.subsection_campaign_types.all()

    solutions_models = MediaSolutionsSection.objects.filter(model_city=id_)
    if solutions_models.exists():
        dict_data_template['solutions_list'] = solutions_models.first().media_solutions_tab.all()
        dict_data_template.update(
            {f'tab{index}': obj.image_name for index, obj in
             enumerate(solutions_models.first().media_solutions_tab.all())})

    static_solutions = StaticSolutions.objects.filter(model_city=id_)
    if static_solutions.exists():
        dict_data_template['static_solutions_list'] = static_solutions.first().static_solutions_tab.all()
        dict_data_template.update(
            {f'tab_static_solutions{index}': obj.image_name for index, obj in
             enumerate(static_solutions.first().static_solutions_tab.all())})

    section_airline_club = AirlineClubLoungesSection.objects.filter(model_city=id_)
    if section_airline_club.exists():
        dict_data_template['airline_club_lounges_list'] = section_airline_club.first().airline_club_lounges_tab.all()
        dict_data_template.update(
            {f'tab_airline_club_lounges{index}': obj.image_name for index, obj in
             enumerate(section_airline_club.first().airline_club_lounges_tab.all())})

    section_security_area = SecurityAreaSection.objects.filter(model_city=id_)
    if section_security_area.exists():
        dict_data_template['section_security_area_list'] = section_security_area.first().section_security_area_tab.all()
        dict_data_template.update(
            {f'tab_section_security_area{index}': obj.image_name for index, obj in
             enumerate(section_security_area.first().section_security_area_tab.all())})
    section_wifi_sponsorships = WiFiSponsorShipsSection.objects.filter(model_city=id_)
    if section_wifi_sponsorships.exists():
        dict_data_template[
            'section_wifi_sponsorships_list'] = section_wifi_sponsorships.first().section_wifi_sponsorships_tab.all()
        dict_data_template.update(
            {f'tab_section_wifi_sponsorships{index}': obj.image_name for index, obj in
             enumerate(section_wifi_sponsorships.first().section_wifi_sponsorships_tab.all())})
    section_experiential = ExperientialSection.objects.filter(model_city=id_)
    if section_experiential.exists():
        dict_data_template[
            'section_experiential_list'] = section_experiential.first().section_experiential_tab.all()
        dict_data_template.update(
            {f'tab_section_experiential{index}': obj.image_name for index, obj in
             enumerate(section_experiential.first().section_experiential_tab.all())})
    section_exteriors = ExteriorsSection.objects.filter(model_city=id_)
    if section_exteriors.exists():
        dict_data_template[
            'section_exteriors_list'] = section_exteriors.first().section_exteriors_tab.all()
        dict_data_template.update(
            {f'tab_section_exteriors{index}': obj.image_name for index, obj in
             enumerate(section_exteriors.first().section_exteriors_tab.all())})

    section_in_flight_video = InFlightVideoSection.objects.filter(model_city=id_)
    if section_in_flight_video.exists():
        dict_data_template[
            'section_in_flight_video_list'] = section_in_flight_video.first().section_in_flight_video_tab.all()
        dict_data_template.update(
            {f'tab_section_in_flight_video{index}': obj.image_name for index, obj in
             enumerate(section_in_flight_video.first().section_in_flight_video_tab.all())})
    return dict_data_template


# @receiver(post_save)
# def get_create_html(sender, instance, created, **kwargs):
#     list_of_models = ('CampaignTypesSubSection', 'CampaignTypesSection', 'AudienceSubSection'
#                       # 'InFlightVideoTabSection', 'ExperientialTabSection', 'WiFiSponsorShipsSectionTab',
#                       # 'SecurityAreaSectionTabSection',
#                       'AirlineClubLoungesTabSection',)
#     # 'StaticSolutionsTabSection', 'MediaSolutionsTabSection')
#     if sender.__name__ in list_of_models:
#
#         if not hasattr(sender, 'get_id_city_model'):
#             return
#
#         context = get_dict(id_=instance.get_id_city_model)
#         path_dir_template = "templates/app_air"
#         path = os.path.dirname(os.path.abspath(__file__))
#         directory = os.path.join(path)
#         path_templates = f"{directory}/templates/app_air/{instance.get_name_city.lower()}.html"
#         content = loader.render_to_string('app_air/index.html', context,
#                                           request=None, using=None)
#         with open(f"{directory}/templates/app_air/cities_html/{instance.get_name_city.lower()}.html", "w") as fh:
#             fh.write(content)
#         with open(path_templates, "w") as fh:
#             fh.seek(0)
#             fh.write('{% load static %}\n')
#             fh.write(content)
#
#         parse_file_compile(path_templates)
#         replace_static_urls_in_html_file(path_templates)


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
@receiver(post_save, sender=City)
def get_create_hero(sender, instance, created, **kwargs):
    if created:
        HeroSection.objects.create(city_model=instance)
        BodySection.objects.create(city_model=instance)
        CampaignTypesSection.objects.create(model_city=instance)
        obj_media_solutions = MediaSolutionsSection.objects.create(model_city=instance)
        for i in range(7):
            MediaSolutionsTabSection.objects.create(model_section=obj_media_solutions)

        obj_static_solution = StaticSolutions.objects.create(model_city=instance)
        for i in range(7):
            StaticSolutionsTabSection.objects.create(model_section=obj_static_solution)
        obj_in_fly = InFlightVideoSection.objects.create(model_city=instance)
        for i in range(4):
            InFlightVideoTabSection.objects.create(model_section=obj_in_fly)
        obj_exterior = ExteriorsSection.objects.create(model_city=instance)
        for i in range(2):
            ExteriorsTabSection.objects.create(model_section=obj_exterior)
        obj_experiential = ExperientialSection.objects.create(model_city=instance)
        for i in range(1):
            ExperientialTabSection.objects.create(model_section=obj_experiential)
        obj_wifi = WiFiSponsorShipsSection.objects.create(model_city=instance)
        for i in range(1):
            WiFiSponsorShipsSectionTab.objects.create(model_section=obj_wifi)
        obj_security = SecurityAreaSection.objects.create(model_city=instance)
        for i in range(2):
            SecurityAreaSectionTabSection.objects.create(model_section=obj_security)

        obj_airline = AirlineClubLoungesSection.objects.create(model_city=instance)
        for i in range(5):
            AirlineClubLoungesTabSection.objects.create(model_section=obj_airline)
