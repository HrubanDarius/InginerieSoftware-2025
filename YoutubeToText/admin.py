from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ConvertedVideo

@admin.register(ConvertedVideo)
class ConvertedVideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'user')
    list_filter = ('created_at',)
    search_fields = ('title', 'content')
