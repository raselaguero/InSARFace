from django.contrib import admin
from .models import Investigator, Study, Provincia, ConsejoPopular, CollectionLayer, Evidence, Title, Displacement
# Register your models here.


class StudyInline(admin.TabularInline):
    model = Study


@admin.register(Investigator)
class InvestigatorAdmin(admin.ModelAdmin):
    list_display = ('name', 'degree', 'country', 'email', 'phone')
    inlines = [StudyInline]


admin.site.register(Provincia)
admin.site.register(ConsejoPopular)
admin.site.register(CollectionLayer)
admin.site.register(Evidence)
admin.site.register(Title)
admin.site.register(Displacement)

