from django.contrib import admin
from rango.models import Category, Page, UserProfile, DemandForecast

class PageAdmin(admin.ModelAdmin):
    list_display = ('title','category','url')

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

class DemandForecastAdmin(admin.ModelAdmin):
    list_display = ('name', 'demand')

# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(UserProfile)
admin.site.register(DemandForecast, DemandForecastAdmin)

