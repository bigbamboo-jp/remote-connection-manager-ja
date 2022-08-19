from django.contrib import admin
from django.contrib.sites.admin import SiteAdmin
from django.contrib.sites.models import Site
from django.db.utils import OperationalError, ProgrammingError

from .models import *

# Register your models here.

try:
    current_site = Site.objects.get_current()
    # admin.site.site_title = current_site.name + ' administration'
    admin.site.site_title = current_site.name + ' サイト管理'
    # admin.site.site_header = current_site.name + ' administration'
    admin.site.site_header = current_site.name + ' 管理サイト'
except (OperationalError, ProgrammingError):
    pass


class CustomSiteAdmin(SiteAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class ActionLogAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('id', 'created_at', 'updated_at', 'created_by', 'execution_time', 'executed'),
            # 'description': 'This data is automatically managed by the system. Users generally cannot edit these.'
            'description': 'このデータはシステムによって自動で管理されています。通常、ユーザーはこれらの編集を行うことはできません。'
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


class AutomaticProcessingScheduleAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('id', 'created_by', 'run_at'),
            # 'description': 'This data is automatically managed by the system. Users generally cannot edit or delete these.'
            'description': 'このデータはシステムによって自動で管理されています。通常、ユーザーはこれらの編集や削除を行うことはできません。'
        }),
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.unregister(Site)
admin.site.register(Site, CustomSiteAdmin)
admin.site.register(ActionLog, ActionLogAdmin)
admin.site.register(AutomaticProcessingSchedule, AutomaticProcessingScheduleAdmin)
