from django.contrib import admin

from .models import Creator


class CreatorAdmin(admin.ModelAdmin):
    list_display = ['username', 'gender','last_login', 'is_active']


admin.site.register(Creator, CreatorAdmin)
