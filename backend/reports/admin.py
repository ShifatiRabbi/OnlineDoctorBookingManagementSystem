from django.contrib import admin
from .models import ReportCache

@admin.register(ReportCache)
class ReportCacheAdmin(admin.ModelAdmin):
    list_display = ('aggregation_key', 'period', 'updated_at')
    list_filter = ('period',)
    search_fields = ('aggregation_key',)