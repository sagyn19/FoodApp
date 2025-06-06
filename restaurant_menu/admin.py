from django.contrib import admin
from .models import Item, Review

class menuItemAdmin(admin.ModelAdmin):
    list_display = ('meal', 'status')
    list_filter = ('status',)
    search_fields = ('meal', 'description')

admin.site.register(Item, menuItemAdmin)
admin.site.register(Review)