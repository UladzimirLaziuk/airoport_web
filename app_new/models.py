import json
import os
import shutil

from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.template.loader import get_template
from django.urls import reverse

from airoport import settings
from app_air.utils_copy_file import copy_and_rename_file, parse_file_compile, replace_static_urls_in_html_file, \
    copy_and_full_rename, get_list_jpg_folder, get_jpg_default, get_jpg_default_bs4, get_jpg_default_bs4_webp
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template import loader

###########################################################################################################
"""Section Title: Hero

    1. Page Title: 
    2. Hero Image (austin_airport_advertising_hero_main)
    3. Hero Headline: title
    4. Hero Sub Headline: description"""

default_text = """With over 21 years of collective experience, we are your trusted partner in the dynamic world of travel media. Our dedicated team is committed to ensuring your brand's success by elevating its presence and captivating millions of airport travelers worldwide.

From the initial stages of crafting customized strategies to the seamless execution of your campaign, we guide you every step of the way. Our goal is to deliver maximum impact and ROI for your brand, leaving a lasting impression on your target audience.

Understanding the unique needs and preferences of travelers, we specialize in creating unforgettable experiences at strategic touchpoints within airports. As your single-source solution, we take care of every aspect of your global airport advertising campaign.

From devising comprehensive strategies and negotiating prime placements to coordinating production, installation, and flawless execution, we ensure that your message reaches the right audience effectively. As an all-in-one solution for travel media, we have successfully propelled numerous renowned brands across 70+ airports and airlines worldwide.

Our collaborative partnerships with global concession owners empower us to optimize campaigns for maximum impact and effectiveness. With exceptional support and guidance throughout the entire process, we are dedicated to unlocking the full potential of airport advertising for your brand."""
class MyModelMixin(object):
    @property
    def get_id_city_model(self):
        return self.model_section.model_city.id

    @property
    def get_name_city(self):
        return self.model_section.model_city.name_city.lower()

    def save(self, *args, **kwargs):
        # if hasattr(self, 'text'):
        #     if '<p>' not in self.text:
        #         string_text = ''
        #         for paragraph in self.text.strip().split("\n"):
        #             if not paragraph.strip():
        #                 continue
        #             string_text += f'\n<p>{paragraph}</p>'
        #         self.text = string_text.strip()
        #     else:
        #         self.text = self.text.strip()
        is_new = not bool(self.pk)
        if not self.file_name and is_new:
            index = self.get_count_parent_model()
            path_template = os.path.join(settings.BASE_DIR, 'app_new/templates/')
            path_file = os.path.join(path_template, 'app_new/new_index_copy.html')

            # folder_path = os.path.join(settings.BASE_DIR, 'static/img/home/articles', self.photo_folder)
            # patt_search = rf'img/home/articles/{self.photo_folder}'
            # patt_search = self.patt_search
            self.file_name = get_jpg_default_bs4_webp(path_file=path_file, id_search=self.patt_search, index=index)

            self.image_name = self.get_image_name(self.image_name, self.file_name)
            copy_and_full_rename(self.file_name, arg=self.image_name)
        return super().save(*args, **kwargs)


class City(models.Model):
    name_city = models.CharField(max_length=255, verbose_name='name_city')
    code_city = models.CharField(max_length=255, verbose_name='code_city')
    page_title = models.CharField(max_length=255, verbose_name='Page Title')
    name_airport = models.CharField(max_length=255, verbose_name='Name Airport')

    def save(self, *args, **kwargs):
        self.name_city = '-'.join(self.name_city.strip().split(' ')).lower()
        return super().save(*args, **kwargs)

    @property
    def get_name_city(self):
        return self.name_city

    @property
    def get_name_city_capitalize(self):
        return self.name_city.capitalize()

    @property
    def get_name_city_title(self):
        return self.name_city.title()

    @property
    def get_name_template(self):
        return '{}-{}-airport-advertising.html'.format(self.get_name_city.lower().replace('-', '').replace(' ', ''),
                                                       self.code_city.lower())

    @property
    def get_upper_code(self):
        return self.code_city.upper()

    @property
    def get_name_airport(self):
        return self.name_airport.title()

    @property
    def get_title_page(self):
        template = '{} {} Airport Advertising - EAM'
        if 'Airport'.lower() in self.get_name_airport.lower():
            template = template.replace('Airport', '')
        if self.name_city.lower() in self.get_name_airport.lower():
            template = template.replace('{}', '', 1)

        return template.format(self.get_name_airport, self.name_city.title()).strip()

    @property
    def get_title_hero(self):
        template = '{} {} Airport Advertising'
        if 'Airport'.lower() in self.get_name_airport.lower():
            template = template.replace('Airport', '')
        if self.name_city.lower() in self.get_name_airport.lower():
            template = template.replace('{}', '', 1)

        return template.format(self.get_name_airport, self.name_city.title()).strip()
    def __str__(self):
        return f'{self.name_city}'


class HeroSectionImage(models.Model):
    image_target = models.CharField(
        max_length=100, default='target_impact.jpg'
    )
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='section_hero')


class AudienceMixin(object):
    def save(self, *args, **kwargs):
        copy_and_full_rename(filename=self.image_target, arg=self.get_image_name,
                             path_target='static/img/specific-page', path_static='static/img/specific-page', webp=False)
        return super().save(*args, **kwargs)

    @property
    def get_html_description(self):
        string_text = ''
        for paragraph in str(self.text).strip().split("\n"):
            string_text += f'\n<p>{paragraph}</p>'

        return string_text.strip()

    @property
    def get_image_name(self):
        return self.image_name.format(self.model_city.name_city, self.model_city.code_city.lower())


class HeroSectionImageOne(AudienceMixin, models.Model):
    image_target = models.CharField(
        max_length=100, default='hero_1.webp'
    )
    model_city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='section_hero_one')
    image_name = models.CharField(max_length=150, default='{}_airport_{}_advertising_{}')

    @property
    def get_image_name(self):
        return self.image_name.format(self.model_city.name_city.lower(), self.model_city.code_city.lower(),
                                      os.path.splitext(self.image_target)[0])

    def get_alt(self):
        return ' '.join(map(str.title, self.get_image_name.split('_')))


class HeroSectionImageTwo(AudienceMixin, models.Model):
    image_target = models.CharField(
        max_length=100, default='hero_2.webp'
    )
    image_name = models.CharField(max_length=150, default='{}_airport_{}_advertising_{}')
    model_city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='section_hero_two')

    @property
    def get_image_name(self):
        return self.image_name.format(self.model_city.name_city.lower(), self.model_city.code_city.lower(),
                                      os.path.splitext(self.image_target)[0])

    def get_alt(self):
        return ' '.join(map(str.title, self.get_image_name.split('_')))


class ImpactAudience(AudienceMixin, models.Model):
    model_city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='section_audience_impact')

    image_name = models.CharField(max_length=255, verbose_name='audience impact image name',
                                  default='{}_airport_{}_advertising_body_impact_image')
    image_target = models.CharField(max_length=100, default='target_impact.jpg')

    text = models.TextField()

    def __str__(self):
        return f'ImpactAudience - {self.model_city.name_city}-{self.model_city.code_city}'


class WhyAudience(AudienceMixin, models.Model):
    model_city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='section_audience_why')

    image_name = models.CharField(max_length=255, verbose_name='audience impact image name',
                                  default='{}_airport_{}_advertising_body_why_image')
    image_target = models.CharField(
        max_length=100, default='why_target.jpg'
    )
    text = models.TextField()

    def __str__(self):
        return f'WhyAudience - {self.model_city.name_city}-{self.model_city.code_city}'


class MarketAudience(AudienceMixin, models.Model):
    model_city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='section_audience_market')

    image_target = models.CharField(
        max_length=100, default='target_market.jpg'
    )
    image_name = models.CharField(max_length=255, verbose_name='audience market image name',
                                  default='{}_airport_{}_advertising_market_image')

    text = models.TextField()

    def __str__(self):
        return f'MarketAudience - {self.model_city.name_city}-{self.model_city.code_city}'


class AboutAudience(AudienceMixin, models.Model):
    model_city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='section_audience_about')

    title = models.CharField(max_length=255, default='Our Expertise in Airport Advertising')

    image_target = models.CharField(
        max_length=100, default='target_about_eam.jpg'
    )
    image_name = models.CharField(max_length=255, verbose_name='audience impact image name',
                                  default='{}_airport_{}_advertising_about_eam_image')

    text = models.TextField(default=default_text)

    def __str__(self):
        return f'AboutAudience - {self.model_city.name_city}-{self.model_city.code_city}'


class AudienceSection(models.Model):
    section_body = models.OneToOneField(City, on_delete=models.CASCADE, related_name='section_audience')
    title = models.CharField(max_length=255, verbose_name='subsection body title',
                             default='An audience for any campaign')

    @property
    def get_name_city(self):
        return self.section_body.name_city.lower()

    def __str__(self):
        return f"AudienceSection- {self.section_body.name_city}"


dict_audience = {
    'path_to_images': os.path.join(settings.BASE_DIR, 'static/img/articles/audience'),
    'Business Decision Makers': 'business_decision_makers_a1.webp',
    'Affluent Travelers': 'affluent_travelers_a1.webp',
    'Early Tech Adopters': 'early_tech_adopters_a1.webp',
    'Leisure Travelers': 'leisure_travel_a1.webp',
    'Families': 'families_a1.webp',
    'Students and Alumni': 'student_a1.webp',

}


class AudienceSubMixin(object):
    def save(self, *args, **kwargs):
        copy_and_full_rename(filename=dict_audience[self.get_title_display()], arg=self.get_image_name,
                             path_target=dict_audience['path_to_images'], path_static=dict_audience['path_to_images'],
                             webp=False)
        return super().save(*args, **kwargs)


class AudienceSubSection(AudienceSubMixin, models.Model):
    MY_CHOICES = ((i.replace(' ', '_').lower(), i) for i in dict_audience.keys() if i != 'path_to_images')

    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='audiences')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='audience')
    image_name = models.CharField(max_length=255, verbose_name='audience subsection image name',
                                  default='{}_airport_{}_advertising_{}_image')
    audience_body = models.ForeignKey(AudienceSection, on_delete=models.CASCADE,
                                      related_name='accordions')
    text = models.TextField()
    file_name = models.CharField(max_length=50, blank=True, null=True)
    title = models.CharField(max_length=255, choices=MY_CHOICES)

    def get_count_parent_model(self):
        return self.audience_body.accordions.count()

    @property
    def get_image_base(self):
        return self.image_name.lower()

    @property
    def get_html_description(self):
        string_text = ''
        for paragraph in str(self.text).strip().split("\n"):
            string_text += f'\n<p class="text-md c-grey">{paragraph}</p>'

        return string_text.strip()

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

    @property
    def get_image_name(self):
        return self.image_name.format(self.audience_body.get_name_city.lower(),
                                      self.audience_body.section_body.code_city.lower(),
                                      self.title.lower())



class CampaignSection(models.Model):
    model_city = models.OneToOneField(City, on_delete=models.CASCADE, related_name='campaign_types')
    title = models.CharField(max_length=255, verbose_name='section CampaignTypes title',
                             default='An advertisers by category')

    @property
    def get_name_city(self):
        return self.model_city.name_city.lower()

    def __str__(self):
        return f"CampaignTypesSection - {self.model_city.name_city}"


dict_images = {
    "path_to_images": os.path.join(settings.BASE_DIR, 'static/img/articles/ads'),
    "b2b": 'business_to_business_a1.webp',
    "conference_participants": 'conference_participants_a1.webp',
    'b2c': 'business_to_consumers.webp',
    'education': 'universities_a1.webp',
    'tourism': 'tourism_a1.webp',
    'government': 'government_organizations_a1.webp',
    'luxury': 'luxury_brand_a1.webp',
    'events': 'sporting_events_a1.webp',
    'entertainment': 'entertainment_a1.webp',
    'financial_and_crypto': 'financial_services_a1.webp',
    'psa_non_profits': 'nonprofit_psa_a1.webp',
    'healthcare': 'healthcare_a1.webp',
}


class CampaignMixin(object):
    def save(self, *args, **kwargs):
        copy_and_full_rename(filename=dict_images[self.tag_name], arg=self.get_image_name,
                             path_target=dict_images['path_to_images'], path_static=dict_images['path_to_images'],
                             webp=False)
        return super().save(*args, **kwargs)


class CampaignSubSection(CampaignMixin, models.Model):
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
    patt_search = models.CharField(max_length=255, verbose_name='patt_search_html', default='segments')
    photo_folder = models.CharField(max_length=255, verbose_name='photo_folder', default='static/img/articles/ads')
    tag_name = models.CharField(max_length=100, choices=MY_CHOICES)

    text = models.TextField()
    subsection_body = models.ForeignKey(CampaignSection, on_delete=models.CASCADE,
                                        related_name='subsection_campaign_types')
    title = models.CharField(max_length=255, verbose_name='subsection campaign types title')

    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}_image')
    file_name = models.CharField(max_length=50, blank=True)

    @property
    def get_html_description(self):
        string_text = ''
        for paragraph in str(self.text).strip().split("\n"):
            string_text += f'\n<p>{paragraph}</p>'

        return string_text.strip()

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

    @property
    def get_image_name(self):
        return self.image_name.format(self.get_name_city, self.get_code_city, self.tag_name)

    def __str__(self):
        return f"CampaignTypesSubSection - {self.subsection_body.model_city.name_city}-" \
               f"{'-'.join(self.image_name.split('_')[-2:])}"


class CampaignSubSectionDescription(models.Model):
    description = models.TextField()
    subsection_model = models.ForeignKey(CampaignSubSection, on_delete=models.CASCADE,
                                         related_name='subsection_campaign_types_description')

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


class MixinImages(object):
    @property
    def get_name_image(self):
        model_city = self.model_digital.model_city
        name_file, _ = os.path.splitext(self.image_target)
        return self.image_name.format(model_city.get_name_city, model_city.code_city.lower(), name_file)

    @property
    def get_alt(self):
        return ' '.join(self.get_name_image.split('_')).title()

    def save(self, *args, **kwargs):
        copy_and_full_rename(filename=self.image_target, arg=self.get_name_image,
                             path_target=self.image_dir, path_static=self.image_dir,
                             webp=False)
        return super().save(*args, **kwargs)


class DigitalSection(models.Model):
    name_section = models.CharField(max_length=25)
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='digital_section')


class ImageDigitalSection(MixinImages, models.Model):
    model_digital = models.ForeignKey(DigitalSection, on_delete=models.CASCADE, related_name='images_digital')
    image_dir = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}')
    image_target = models.CharField(max_length=100)


class SolutionSection(models.Model):
    name_section = models.CharField(max_length=25)
    model_city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='solution_section')


class ImageSolutionSection(MixinImages, models.Model):
    model_digital = models.ForeignKey(SolutionSection, on_delete=models.CASCADE, related_name='images_solution')
    image_dir = models.CharField(max_length=255)
    image_name = models.CharField(max_length=255, default='{}_airport_{}_advertising_{}')
    image_target = models.CharField(max_length=100)


@receiver(post_save, sender=City)
def create_digital_section(sender, instance, created, **kwargs):
    if created:
        HeroSectionImageOne.objects.create(model_city=instance)
        HeroSectionImageTwo.objects.create(model_city=instance)
        AboutAudience.objects.create(model_city=instance)
        with open('example_section.json', 'r') as file:
            digital_dict = json.load(file)

        for key, values in digital_dict.items():
            obj_digital = DigitalSection.objects.create(name_section=key, model_city=instance)
            for file_path in values:
                image_dir = os.path.dirname(file_path)
                full_path = os.path.join(settings.BASE_DIR, 'static', image_dir)
                name_file = os.path.basename(file_path)
                ImageDigitalSection.objects.create(model_digital=obj_digital, image_dir=full_path,
                                                   image_target=name_file)
        with open('solutions_section.json', 'r') as file:
            digital_dict = json.load(file)

        for key, values in digital_dict.items():
            obj_solution = SolutionSection.objects.create(name_section=key, model_city=instance)
            for file_path in values:
                image_dir = os.path.dirname(file_path)
                full_path = os.path.join(settings.BASE_DIR, 'static', image_dir)
                name_file = os.path.basename(file_path)
                ImageSolutionSection.objects.create(model_digital=obj_solution, image_dir=full_path,
                                                    image_target=name_file)
