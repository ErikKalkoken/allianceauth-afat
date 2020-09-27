# -*- coding: utf-8 -*-

"""
admin pages configuration
"""

from django.contrib import admin

from .models import AFat, AFatLink, AFatLinkType


def custom_filter(title):
    """
    defining custom filter titles
    :param title:
    :return:
    """

    class Wrapper(admin.FieldListFilter):
        """
        Wrapper
        """

        def expected_parameters(self):
            """
            expected parameters
            """
            pass

        def choices(self, changelist):
            """
            choices
            :param changelist:
            """
            pass

        def __new__(cls, *args, **kwargs):
            instance = admin.FieldListFilter.create(*args, **kwargs)
            instance.title = title

            return instance

    return Wrapper


# Register your models here.
@admin.register(AFatLink)
class AFatLinkAdmin(admin.ModelAdmin):
    """
    config for fat link model
    """

    list_display = (
        "afattime",
        "creator",
        "fleet",
        "_link_type",
        "is_esilink",
        "hash",
        "deleted_at",
    )

    list_filter = (
        "is_esilink",
        ("link_type__name", custom_filter(title="fleet type")),
    )

    ordering = ("-afattime",)

    def _link_type(self, obj):
        if obj.link_type:
            return obj.link_type.name
        else:
            return "-"

    _link_type.short_description = "Fleet Type"
    _link_type.admin_order_field = "link_type__name"


@admin.register(AFat)
class AFatAdmin(admin.ModelAdmin):
    """
    config for fat model
    """

    list_display = ("character", "system", "shiptype", "afatlink", "deleted_at")

    list_filter = ("character", "system", "shiptype")

    ordering = ("-character",)


@admin.register(AFatLinkType)
class AFatLinkTypeAdmin(admin.ModelAdmin):
    """
    config for fatlinktype model
    """

    # list_select_related = True

    list_display = (
        "id",
        "_name",
        "_is_enabled",
    )

    list_filter = ("is_enabled",)

    ordering = ("name",)

    def _name(self, obj):
        return obj.name

    _name.short_description = "Fleet Type"
    _name.admin_order_field = "name"

    def _is_enabled(self, obj):
        return obj.is_enabled

    _is_enabled.boolean = True
    _is_enabled.short_description = "Is Enabled"
    _is_enabled.admin_order_field = "is_enabled"

    actions = (
        "mark_as_active",
        "mark_as_inactive",
    )

    def mark_as_active(self, request, queryset):
        """
        Mark fleet type as active
        :param request:
        :param queryset:
        """

        notifications_count = 0

        for obj in queryset:
            obj.is_enabled = True
            obj.save()

            notifications_count += 1

        self.message_user(
            request, "{} fleet types marked as active".format(notifications_count)
        )

    mark_as_active.short_description = "Activate selected fleet type(s)"

    def mark_as_inactive(self, request, queryset):
        """
        Mark fleet type as inactive
        :param request:
        :param queryset:
        """

        notifications_count = 0

        for obj in queryset:
            obj.is_enabled = False
            obj.save()

            notifications_count += 1

        self.message_user(
            request, "{} fleet types marked as inactive".format(notifications_count)
        )

    mark_as_inactive.short_description = "Deactivate selected fleet type(s)"
