from django.contrib import admin

# Register your models here.
from .models import City, ImpactAudience, WhyAudience, AudienceSection, AudienceSubSection, CampaignSection, \
    CampaignSubSection, HeroSectionImageTwo, HeroSectionImageOne, AboutAudience, DigitalSection, ImageDigitalSection, MarketAudience

admin.site.register(City)
admin.site.register(ImpactAudience)
admin.site.register(WhyAudience)
admin.site.register(MarketAudience)
admin.site.register(AboutAudience)


class AudienceSubSectionInline(admin.StackedInline):
    model = AudienceSubSection
    extra = 6
    can_delete = False
    max_num = 6
    fields = ('title', 'text')


class AudienceSectionModelAdmin(admin.ModelAdmin):
    inlines = (AudienceSubSectionInline,)


admin.site.register(AudienceSection, AudienceSectionModelAdmin)


class CampaignTypesSubSectionInline(admin.StackedInline):
    model = CampaignSubSection
    extra = 12
    can_delete = False
    max_num = 12
    fields = ('tag_name', 'title', 'text')


class CampaignTypesSectionModelAdmin(admin.ModelAdmin):
    inlines = (CampaignTypesSubSectionInline,)


admin.site.register(CampaignSection, CampaignTypesSectionModelAdmin)
# admin.site.register(HeroSectionImageOne)
# admin.site.register(HeroSectionImageTwo)
# admin.site.register(ImageDigitalSection)
# admin.site.register(DigitalSection)

