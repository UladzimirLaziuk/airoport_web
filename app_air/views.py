from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
def home(request):
    return render(request, 'app_air/index.html', {})


def home_title(context=None, name_html=None):
    return render(name_html, context=context)


class CityView(TemplateView):
    template_name = 'app_air/{}.html'

    def get(self, request, *args, **kwargs):
        city_name = kwargs.get('city_name')
        self.template_name = self.template_name.format(city_name)
        return super().get(request, *args, **kwargs)
