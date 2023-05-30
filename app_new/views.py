from django.shortcuts import render
from app_new.models import City
from django.views.generic import TemplateView, DetailView


class ExampleView(TemplateView):
    template_name = 'app_new/new_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_city = City.objects.last()
        context['obj_city'] = obj_city
        context['digital_section'] = obj_city.digital_section.filter(name_section='digital').get()
        context['static_section'] = obj_city.digital_section.filter(name_section='static').get()
        context['other_section'] = obj_city.digital_section.filter(name_section='other').get()
        for name_section in obj_city.solution_section.values_list('name_section', flat=True):
            context[name_section.replace('-', '_')] = obj_city.solution_section.filter(
                name_section=name_section).first().images_solution.all()

        return context

class CityDetailView(DetailView):
    model = City
    template_name = 'app_new/new_template.html'
    # context_object_name = 'city'

    def get_object(self):
        name_city = self.kwargs['name_city']
        city = City.objects.filter(name_city=name_city).first()
        return city

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_city = self.get_object()
        context['obj_city'] = obj_city
        context['digital_section'] = obj_city.digital_section.filter(name_section='digital').get()
        context['static_section'] = obj_city.digital_section.filter(name_section='static').get()
        context['other_section'] = obj_city.digital_section.filter(name_section='other').get()
        for name_section in obj_city.solution_section.values_list('name_section', flat=True):
            context[name_section.replace('-', '_')] = obj_city.solution_section.filter(
                name_section=name_section).first().images_solution.all()

        return context