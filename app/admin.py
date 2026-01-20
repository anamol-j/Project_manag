from django.contrib import admin
from .models import (
    Organization,
    Membership,
    Project,
    Task,
    User
)

class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

class TaskInline(admin.TabularInline):
    model = Task
    extra = 1

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    search_fields = ("name", "owner__username")
    inlines = [MembershipInline]


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "organization", "role", "joined_at")
    list_filter = ("role", "organization")
    search_fields = ("user__username", "organization__name")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "created_by")
    list_filter = ("organization",)
    search_fields = ("title", "organization__name", "created_by__username")
    inlines = [TaskInline]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "assignee",
        "status",
        "priority",
        "due_date",
    )
    list_filter = ("status", "priority", "project")
    search_fields = ("title", "project__title", "assignee__username")

