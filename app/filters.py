import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Task.STATUS_CHOICES)
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    project = django_filters.NumberFilter(field_name="project_id")
    assignee = django_filters.NumberFilter(field_name="assignee_id")

    due_date_from = django_filters.DateFilter(
        field_name="due_date", lookup_expr="gte"
    )
    due_date_to = django_filters.DateFilter(
        field_name="due_date", lookup_expr="lte"
    )

    class Meta:
        model = Task
        fields = [
            "status",
            "priority",
            "project",
            "assignee",
            "due_date_from",
            "due_date_to",
        ]