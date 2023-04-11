import re

from django.contrib import admin, messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html

from .models import City,  HeroSection, HeroSubHeadline, BodySection, \
    BodySubSection, BodySubSectionDescription, AudienceSection, AudienceSubSection, AudienceSubSectionDescription, \
    CampaignTypesSubSection, CampaignTypesSubSectionDescription, MediaSolutionsSection, \
    MediaSolutionsTabSection, CampaignTypesSection
from django import forms
from django.contrib.admin import ModelAdmin
from django.forms import CheckboxSelectMultiple, TextInput, BaseInlineFormSet
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.admin import site, AdminSite, ModelAdmin, TabularInline, StackedInline
from django.db import models


# class HeroModelInline(admin.StackedInline):
#     model = HeroModel
#     extra = 1
#     can_delete = False
#     max_num = 1
#     exclude = ('image_hero_url_jpg', 'image_hero_url_webp')


# class WhyCityAirportInline(admin.StackedInline):
#     model = WhyCityAirport
#     extra = 1
#     can_delete = False
#     max_num = 1
#

# class AboutAirportCityInline(admin.StackedInline):
#     model = AboutAirportCity
#     extra = 1
#     can_delete = False
#     max_num = 1
#

class NoDeleteInline(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.can_delete = False


# class AboutCityInline(admin.StackedInline):
#     model = AboutCity
#     extra = 1
#     max_num = 1
#     can_delete = False


# class AirportAdmin(admin.ModelAdmin):
#     inlines = (WhyCityAirportInline, AboutAirportCityInline, AboutCityInline)
#     list_display = ('name_city', 'my_field_link')
#
#     def my_field_link(self, obj):
#         # url = reverse('my_view_name', args=[obj.id])
#         self.current_site = get_current_site(self.request)
#         # absolute_url = self.request.build_absolute_uri(reverse('myapp:another-page'))
#         # return format_html('<a href="/{}/city/{}">Link page</a>', self.current_site, obj.name_city.lower())
#
#         return format_html('<a href="{}/city/{}">My Custom Link</a>', self.request._current_scheme_host,
#                            obj.name_city.lower())
#
#     my_field_link.short_description = 'My Field Link'
#     my_field_link.admin_order_field = 'my_field'
#
#     # def three_tags(self, obj):
#     #
#     #     return '<a href="{}/city/{}"></a>'.format(self.current_site, obj.name_city)
#     def get_queryset(self, request):
#         self.request = request
#         return super().get_queryset(request)
#
#     def save_model(self, request, obj, form, change):
#         current_site = get_current_site(request)
#         super().save_model(request, obj, form, change)
#         messages.add_message(request, messages.SUCCESS,
#                              f"Object has been created successfully on the website {current_site}/city/{str(obj.name_city).lower()}")
#

# @receiver(post_save, sender=City)
# def do_something_on_save(sender, instance, created, **kwargs):
#     if created:
#         print("MyInlineModel with id {} has been created".format(instance.id))
#     else:
#         print("MyInlineModel with id {} has been updated".format(instance.id))


admin.site.register(City)
admin.site.register(HeroSection)
admin.site.register(HeroSubHeadline)
admin.site.register(BodySection)
admin.site.register(BodySubSection)
admin.site.register(BodySubSectionDescription)
admin.site.register(AudienceSection)
admin.site.register(AudienceSubSection)
admin.site.register(AudienceSubSectionDescription)
admin.site.register(CampaignTypesSection)
# admin.site.register(CampaignTypesHeroSection)
admin.site.register(CampaignTypesSubSection)
admin.site.register(CampaignTypesSubSectionDescription)
admin.site.register(MediaSolutionsSection)
admin.site.register(MediaSolutionsTabSection)
