import json
import logging
import os
from urllib.parse import urlparse
from django.core.management import call_command

from django.core.management import BaseCommand
# from pyngrok import ngrok

from airoport import settings

logger = logging.getLogger('bot.logger')


def get_data_file(path_file=None):
    if not path_file:
        path_file = os.path.join(settings.BASE_DIR, 'airports.json')
    with open(path_file) as f:
        data = json.load(f)
    return data


def get_name_airoport(code_city):
    name_airoport = ''
    return name_airoport


class Command(BaseCommand):
    help = 'move base'

    def handle(self, *args, **options):
        from app_air import models as old
        from app_new import models as new
        code_dict = get_data_file()
        # dt = get_data_file('city_app.json')
        # print(code_dict)

        for object_old_model in old.City.objects.all():

            # query_object = old.City.objects.filter(name_city='atlanta')
            query_object_model = object_old_model
            #
            # obj_old = query_object.values('name_city', 'code_city', 'page_title')

            dict_model = {}
            code_city = object_old_model.code_city
            dict_model.update({'name_city': object_old_model.name_city})
            dict_model.update({'code_city': code_city})
            dict_model.update({'page_title': object_old_model.page_title})

            if code_city in code_dict.keys():
                name_airport = code_dict[code_city]['cityName']['en']
                dict_model.update({'name_airport': name_airport})
            else:
                dict_model.update({'name_airport': ''})

            obj = new.City.objects.create(**dict_model)
            if hasattr(query_object_model, 'section_body') and query_object_model.section_body.first():

                for text, model in zip(query_object_model.section_body.first().tabs.values('text'),
                                       (new.ImpactAudience, new.WhyAudience, new.MarketAudience)):
                    text.update({'model_city': obj})
                    obj_audience = model.objects.create(**text)

                    self.stdout.write(self.style.SUCCESS(f'obj_audience  {obj_audience=}'))
                obj_audience = new.AudienceSection.objects.create(section_body=obj)
                if query_object_model.section_audience.first():
                    for dict_audience in query_object_model.section_audience.first().accordions.values('title', 'text'):
                        dict_audience.update({'audience_body': obj_audience})
                        dict_audience['text'] = dict_audience['text'].replace('<p>', '').replace('</p>', '')

                        obj_audience_sub = new.AudienceSubSection.objects.create(**dict_audience)

                        self.stdout.write(self.style.SUCCESS(f'Successfully obj_audience_sub  {obj_audience_sub =}'))

                obj_campaign = new.CampaignSection.objects.create(model_city=obj)
                if query_object_model.campaign_types.first():
                    for dict_campaign in query_object_model. \
                            campaign_types.first().subsection_campaign_types.values('title', 'tag_name', 'text'):
                        dict_campaign.update({'subsection_body': obj_campaign})
                        object_new_campaign = new.CampaignSubSection.objects.create(**dict_campaign)
                        self.stdout.write(
                            self.style.SUCCESS(f'Successfully object_new_campaign  {object_new_campaign =}'))
