import re

from django.contrib import admin, messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.html import format_html

from .models import City, HeroSection, HeroSubHeadline, BodySection, \
    BodySubSection, BodySubSectionDescription, AudienceSection, AudienceSubSection, AudienceSubSectionDescription, \
    CampaignTypesSubSection, CampaignTypesSubSectionDescription, MediaSolutionsSection, \
    MediaSolutionsTabSection, CampaignTypesSection, StaticSolutions, StaticSolutionsTabSection, \
    AirlineClubLoungesSection, AirlineClubLoungesTabSection, SecurityAreaSection, SecurityAreaSectionTabSection, \
    WiFiSponsorShipsSection, WiFiSponsorShipsSectionTab, ExteriorsSection, ExteriorsTabSection, ExperientialSection, \
    ExperientialTabSection, InFlightVideoSection, InFlightVideoTabSection
from django import forms
from django.contrib.admin import ModelAdmin
from django.forms import CheckboxSelectMultiple, TextInput, BaseInlineFormSet
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.admin import site, AdminSite, ModelAdmin, TabularInline, StackedInline
from django.db import models
from django import forms
import os
from django.conf import settings


class MyAdminSite(AdminSite):
    def get_model_ordering(self, model):
        return None


admin_site = MyAdminSite()


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
from django.forms import FileInput, TextInput


class StaticFileInput(FileInput):
    def __init__(self, attrs=None):
        default_attrs = {'accept': '.jpg, .png, .webp, '}
        if attrs:
            default_attrs.update(attrs)
        default_attrs.update({'directory': '/static/'})
        super().__init__(default_attrs)


# InMemoryUploadedFile

class MyForm(forms.ModelForm):
    file_name = forms.FileField(widget=StaticFileInput())

    class Meta:
        model = City
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if 'file' in self.files:
            instance.file_name = self.files['file_name'].name
        if commit:
            instance.save()
        return instance


class MyFormBody(MyForm):
    class Meta:
        model = BodySection
        fields = '__all__'


class MyFormAudienceSubSection(forms.ModelForm):
    file_name = forms.FileField(widget=StaticFileInput())

    class Meta:
        model = AudienceSubSection
        fields = '__all__'


class AudienceSubSectionAdmin(admin.ModelAdmin):
    form = MyFormAudienceSubSection


class HeroAdmin(admin.ModelAdmin):
    form = MyForm


class BodyAdmin(admin.ModelAdmin):
    form = MyFormBody


class FileSelectWidget(forms.Select):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        files_path = os.path.join(settings.BASE_DIR, 'static', 'dir_basis_images')
        # self.choices = [(f, f) for f in os.listdir(files_path) if os.path.isfile(os.path.join(files_path, f))]
        self.choices = [(f, f) for f in os.listdir(files_path) if
                        os.path.isfile(os.path.join(files_path, f)) and not f.endswith('.png')]


# class FilesDropdownField(forms.ChoiceField):
#     def __init__(self, path, *args, **kwargs):
#         choices = []
#         for root, dirs, files in os.walk(path):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 choices.append((file_path, file_path.replace(path, "", 1)))
#         super().__init__(choices=choices, *args, **kwargs)
#
# class FilesDropdownWidget(forms.Select):
#     def __init__(self, attrs=None, choices=(), path=None):
#         self.path = path
#         super().__init__(attrs, choices)
#
#     def render(self, name, value, attrs=None, renderer=None):
#         if value:
#             value = value.replace("\\", "/")
#         return super().render(name, value, attrs, renderer)
#
#     def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
#         if value:
#             value = value.replace("\\", "/")
#         return super().create_option(name, value, label, selected, index, subindex, attrs)
#
#     def _get_choices(self):
#         return self._choices
#
#     def _set_choices(self, value):
#         self._choices = value
#
#     choices = property(_get_choices, _set_choices)
#
#     def build_attrs(self, attrs=None, extra_attrs=None, **kwargs):
#         attrs = super().build_attrs(attrs, extra_attrs, **kwargs)
#         attrs['path'] = self.path
#         return attrs


# Определяем новую форму
class HeroForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = HeroSection
        fields = '__all__'


# Определяем модель
class HeroModelAdmin(admin.ModelAdmin):
    form = HeroForm


class BodySectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = HeroSection
        fields = '__all__'


class BodySectionModelAdmin(admin.ModelAdmin):
    form = BodySectionForm


class AudienceSubSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = AudienceSubSection
        fields = '__all__'


class AudienceSubSectionModelAdmin(admin.ModelAdmin):
    form = AudienceSubSectionForm


class CampaignTypesSubSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = CampaignTypesSubSection
        fields = '__all__'


class CampaignTypesSubSectionModelAdmin(admin.ModelAdmin):
    form = CampaignTypesSubSectionForm


class MediaSolutionsTabSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = MediaSolutionsTabSection
        fields = '__all__'


# class MyAdminSite(AdminSite):
#     def get_model_order(self, models):
#         # получить список всех моделей в порядке их определения
#         all_models = [m for m in models.values()]
#         all_models = [m for sublist in all_models for m in sublist]
#
#         # добавить City и Country в начало списка
#         order = [City] + [m for m in all_models if m not in [City]]
#
#         return order
#
#
# admin_site = MyAdminSite(name='admin')


class MediaSolutionsTabSectionModelAdmin(admin.ModelAdmin):
    form = MediaSolutionsTabSectionForm
    order_with_respect_to = None


# admin_site.site.register(City)

# admin.site.register(HeroSection, HeroModelAdmin)
# admin.site.register(HeroSubHeadline)
# admin.site.register(BodySection, BodySectionModelAdmin)
# admin.site.register(BodySubSection)
# admin.site.register(BodySubSectionDescription)
# admin.site.register(AudienceSection)
# admin.site.register(AudienceSubSection, AudienceSubSectionModelAdmin)
# admin.site.register(AudienceSubSectionDescription)
# admin.site.register(CampaignTypesSection)
# # admin.site.register(CampaignTypesHeroSection)
# admin.site.register(CampaignTypesSubSection, CampaignTypesSubSectionModelAdmin)
# admin.site.register(CampaignTypesSubSectionDescription)
# admin.site.register(MediaSolutionsSection)
# admin.site.register(MediaSolutionsTabSection,
#                     MediaSolutionsTabSectionModelAdmin)


class MyAdminSite(admin.AdminSite):
    # def get_app_list(self, request):
    #     app_list = super().get_app_list(request)
    #     # reorder the app list as you like
    #     return app_list
    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        app_dict = self._build_app_dict(request, app_label)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        # Sort the models alphabetically within each app.
        # for app in app_list:
        #     app["models"].sort(key=lambda x: x["name"])

        return app_list


mysite = MyAdminSite()
admin.site = mysite
# from django.contrib.auth.models import User
#
# admin.site.register(User)

admin.site.register(City)

admin.site.register(HeroSection, HeroModelAdmin)
admin.site.register(HeroSubHeadline)
admin.site.register(BodySection, BodySectionModelAdmin)
admin.site.register(BodySubSection)
# admin.site.register(BodySubSectionDescription)
admin.site.register(AudienceSection)
admin.site.register(AudienceSubSection, AudienceSubSectionModelAdmin)
# admin.site.register(AudienceSubSectionDescription)
admin.site.register(CampaignTypesSection)
# admin.site.register(CampaignTypesHeroSection)
admin.site.register(CampaignTypesSubSection, CampaignTypesSubSectionModelAdmin)
# admin.site.register(CampaignTypesSubSectionDescription)
admin.site.register(MediaSolutionsSection)
admin.site.register(MediaSolutionsTabSection,
                    MediaSolutionsTabSectionModelAdmin)
admin.site.register(StaticSolutions)


class StaticSolutionsTabSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = StaticSolutionsTabSection
        fields = '__all__'


class StaticSolutionsTabSectionModelAdmin(admin.ModelAdmin):
    form = MediaSolutionsTabSectionForm
    order = 0


admin.site.register(StaticSolutionsTabSection, StaticSolutionsTabSectionModelAdmin)
admin.site.register(AirlineClubLoungesSection)


class AirlineClubLoungesTabSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = AirlineClubLoungesTabSection
        fields = '__all__'


class AirlineClubLoungesTabSectionModelAdmin(admin.ModelAdmin):
    form = AirlineClubLoungesTabSectionForm


admin.site.register(AirlineClubLoungesTabSection, AirlineClubLoungesTabSectionModelAdmin)
admin.site.register(SecurityAreaSection)


class SecurityAreaSectionTabSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = SecurityAreaSectionTabSection
        fields = '__all__'


class SecurityAreaSectionTabSectionModelAdmin(admin.ModelAdmin):
    form = SecurityAreaSectionTabSectionForm


admin.site.register(SecurityAreaSectionTabSection, SecurityAreaSectionTabSectionModelAdmin)
admin.site.register(WiFiSponsorShipsSection)


class WiFiSponsorShipsSectionTabForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = WiFiSponsorShipsSectionTab
        fields = '__all__'


class WiFiSponsorShipsSectionTabModelAdmin(admin.ModelAdmin):
    form = WiFiSponsorShipsSectionTabForm


admin.site.register(WiFiSponsorShipsSectionTab, WiFiSponsorShipsSectionTabModelAdmin)
admin.site.register(ExperientialSection)


class ExperientialTabSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = ExperientialTabSection
        fields = '__all__'


class ExperientialTabSectionModelAdmin(admin.ModelAdmin):
    form = ExperientialTabSectionForm


admin.site.register(ExperientialTabSection, ExperientialTabSectionModelAdmin)
admin.site.register(ExteriorsSection)


class ExteriorsTabSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = ExteriorsTabSection
        fields = '__all__'


class ExteriorsTabSectionModelAdmin(admin.ModelAdmin):
    form = ExteriorsTabSectionForm


admin.site.register(ExteriorsTabSection, ExteriorsTabSectionModelAdmin)
admin.site.register(InFlightVideoSection)


class InFlightVideoTabSectionForm(forms.ModelForm):
    file_name = forms.CharField(widget=FileSelectWidget)

    class Meta:
        model = InFlightVideoTabSection
        fields = '__all__'


class InFlightVideoTabSectionModelAdmin(admin.ModelAdmin):
    form = InFlightVideoTabSectionForm


admin.site.register(InFlightVideoTabSection, InFlightVideoTabSectionModelAdmin)
