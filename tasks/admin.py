from django.contrib import admin

from .models import Bid, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "category",
        "budget",
        "created_by",
        "status",
        "created_at",
    )

    list_filter = (
        "category",
        "status",
        "created_at",
    )

    search_fields = (
        "title",
        "description",
        "created_by__username",
    )


@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):

    list_display = (
        "task",
        "freelancer",
        "amount",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "task__title",
        "freelancer__username",
        "message",
    )
