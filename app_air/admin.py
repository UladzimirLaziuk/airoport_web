import re

from django.contrib import admin, messages
from django.contrib.sites.shortcuts import get_current_site
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import City, HeroModel, WhyCityAirport, AboutAirportCity, AboutCity
from django import forms
from django.contrib.admin import ModelAdmin
from django.forms import CheckboxSelectMultiple, TextInput, BaseInlineFormSet
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.admin import site, AdminSite, ModelAdmin, TabularInline, StackedInline
from django.db import models


class HeroModelInline(admin.StackedInline):
    model = HeroModel
    extra = 1
    can_delete = False
    max_num = 1


class WhyCityAirportInline(admin.StackedInline):
    model = WhyCityAirport
    extra = 1
    can_delete = False
    max_num = 1


class AboutAirportCityInline(admin.StackedInline):
    model = AboutAirportCity
    extra = 1
    can_delete = False
    max_num = 1


class NoDeleteInline(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.can_delete = False


class AboutCityInline(admin.StackedInline):
    model = AboutCity
    extra = 1
    max_num = 1
    can_delete = False


class AirportAdmin(admin.ModelAdmin):
    inlines = (HeroModelInline, WhyCityAirportInline, AboutAirportCityInline, AboutCityInline)


    def save_model(self, request, obj, form, change):
        current_site = get_current_site(request)
        super().save_model(request, obj, form, change)
        messages.add_message(request, messages.SUCCESS,
                             f"Object has been created successfully on the website {current_site}/city/{obj.name_city}")


@receiver(post_save, sender=City)
def do_something_on_save(sender, instance, created, **kwargs):
    if created:
        print("MyInlineModel with id {} has been created".format(instance.id))
    else:
        print("MyInlineModel with id {} has been updated".format(instance.id))


admin.site.register(City, AirportAdmin)


