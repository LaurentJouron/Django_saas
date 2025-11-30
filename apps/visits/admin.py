from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Visit


class PathTypeFilter(admin.SimpleListFilter):
    """Filtre personnalisé pour filtrer les visites par type de page."""

    title = _("Type de page")
    parameter_name = "path_type"

    def lookups(self, request, model_admin):
        return (
            ("home", _("Accueil")),
            ("admin", _("Administration")),
            ("visits", _("Visit")),
            ("other", _("Autre")),
        )

    def queryset(self, request, queryset):
        if self.value() == "home":
            return queryset.filter(path__in=["/", ""])
        elif self.value() == "admin":
            return queryset.filter(path__contains="/admin")
        elif self.value() == "visits":
            return queryset.filter(path__contains="/visit")
        elif self.value() == "other":
            return (
                queryset.exclude(path__contains="/admin")
                .exclude(path__contains="/visit")
                .exclude(path__in=["/", ""])
            )


@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    """
    Interface d'administration avancée pour le modèle Visit.
    Affiche les visites avec des statistiques et des filtres puissants.
    """

    # ==================
    # Configuration list
    # ==================
    list_display = [
        "id",
        "colored_path",
        "formatted_timestamp",
        "time_ago",
        "day_of_week",
    ]

    list_display_links = ["id", "colored_path"]

    list_filter = [
        ("timestamp", admin.DateFieldListFilter),
        PathTypeFilter,
    ]

    search_fields = ["path", "id"]

    # Default order (newest first)
    ordering = ["-timestamp"]

    # Pagination
    list_per_page = 50
    list_max_show_all = 1000

    # Actions available
    actions = ["export_as_json", "delete_selected"]

    # Read-only fields
    readonly_fields = [
        "id",
        "path",
        "timestamp",
        "formatted_timestamp",
        "time_ago",
        "full_url_display",
    ]

    # ==================
    # form configuration
    # ==================
    fieldsets = (
        (
            _("Informations de visite"),
            {"fields": ("id", "path", "full_url_display")},
        ),
        (
            _("Horodatage"),
            {
                "fields": ("timestamp", "formatted_timestamp", "time_ago"),
                "description": "Date et heure de la visite",
            },
        ),
    )

    # ===========
    # Permissions
    # ============
    def has_add_permission(self, request):
        """Désactive l'ajout manuel de visites."""
        return False

    def has_change_permission(self, request, obj=None):
        """Désactive la modification des visites."""
        return False

    # ======================
    # Custom display methods
    # ======================

    @admin.display(description="Chemin", ordering="path")
    def colored_path(self, obj):
        """Affiche le chemin avec une couleur selon le type."""
        if not obj.path:
            return format_html('<span style="color: #999;">N/A</span>')

        # Coloration according to the path
        color = "#0066cc"  # Blue by default
        if "/admin" in obj.path:
            color = "#dc3545"  # Red for admin
        elif "/api" in obj.path:
            color = "#28a745"  # Green for API
        elif obj.path == "/" or obj.path == "":
            color = "#6c757d"  # Gray for home

        # Truncate if too long
        display_path = (
            obj.path if len(obj.path) <= 60 else obj.path[:57] + "..."
        )

        return format_html(
            '<code style="color: {}; background: #f5f5f5; padding: 2px 6px; '
            'border-radius: 3px; font-size: 12px;">{}</code>',
            color,
            display_path,
        )

    @admin.display(description="Date et heure", ordering="timestamp")
    def formatted_timestamp(self, obj):
        """Displays the formatted date with icon."""
        if not obj.timestamp:
            return "-"

        date_str = obj.timestamp.strftime("%d/%m/%Y à %H:%M:%S")
        return format_html(
            '<span style="white-space: nowrap;">📅 {}</span>', date_str
        )

    @admin.display(description="Il y a")
    def time_ago(self, obj):
        """Display the elapsed time since the visit."""
        from django.utils.timezone import now

        if not obj.timestamp:
            return "-"

        diff = now() - obj.timestamp

        if diff.days > 365:
            years = diff.days // 365
            return format_html(
                '<span style="color: #999;">il y a {} an{}</span>',
                years,
                "s" if years > 1 else "",
            )
        elif diff.days > 30:
            months = diff.days // 30
            return format_html(
                '<span style="color: #666;">il y a {} mois</span>', months
            )
        elif diff.days > 0:
            return format_html(
                '<span style="color: #333;">il y a {} jour{}</span>',
                diff.days,
                "s" if diff.days > 1 else "",
            )
        elif diff.seconds > 3600:
            hours = diff.seconds // 3600
            return format_html(
                '<span style="color: #0066cc;">il y a {} heure{}</span>',
                hours,
                "s" if hours > 1 else "",
            )
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return format_html(
                '<span style="color: #28a745;">il y a {} minute{}</span>',
                minutes,
                "s" if minutes > 1 else "",
            )
        else:
            return format_html(
                '<span style="color: #dc3545; font-weight: bold;">à l\'instant</span>'
            )

    @admin.display(description="Jour")
    def day_of_week(self, obj):
        """Displays the day of the week."""
        if not obj.timestamp:
            return "-"

        days = {
            0: "🌙 Lundi",
            1: "🔥 Mardi",
            2: "💼 Mercredi",
            3: "🎯 Jeudi",
            4: "🎉 Vendredi",
            5: "🌴 Samedi",
            6: "☀️ Dimanche",
        }

        return days.get(obj.timestamp.weekday(), "-")

    @admin.display(description="URL complète")
    def full_url_display(self, obj):
        """Display the full URL with a clickable link."""
        if not obj.path:
            return "-"

        # Construction of the complete URL
        from django.contrib.sites.models import Site

        try:
            current_site = Site.objects.get_current()
            full_url = f"https://{current_site.domain}{obj.path}"
        except:
            full_url = f"http://localhost:8000{obj.path}"

        return format_html(
            '<a href="{}" target="_blank" style="color: #0066cc;">'
            '{} <span style="font-size: 10px;">🔗</span></a>',
            full_url,
            full_url,
        )

    # ==============
    # Custom actions
    # ==============

    @admin.action(description="Exporter la sélection en JSON")
    def export_as_json(self, request, queryset):
        """Exports selected visits to JSON."""
        from django.http import JsonResponse

        data = list(queryset.values("id", "path", "timestamp"))

        # Conversion of datetimes into strings
        for item in data:
            if item["timestamp"]:
                item["timestamp"] = item["timestamp"].isoformat()

        response = JsonResponse(
            data, safe=False, json_dumps_params={"indent": 2}
        )
        response["Content-Disposition"] = (
            'attachment; filename="visits_export.json"'
        )
        return response

    # =======================
    # Personalized Changelist
    # =======================

    def changelist_view(self, request, extra_context=None):
        """Adds statistics in the list view."""
        extra_context = extra_context or {}

        # Aggregate statistics
        total_visits = Visit.objects.count()

        from django.utils.timezone import now
        from datetime import timedelta

        today = now().date()
        visits_today = Visit.objects.filter(timestamp__date=today).count()
        visits_week = Visit.objects.filter(
            timestamp__gte=now() - timedelta(days=7)
        ).count()
        visits_month = Visit.objects.filter(
            timestamp__gte=now() - timedelta(days=30)
        ).count()

        # Top 5 of the most visited paths
        top_paths = (
            Visit.objects.values("path")
            .annotate(count=Count("id"))
            .order_by("-count")[:5]
        )

        extra_context["total_visits"] = total_visits
        extra_context["visits_today"] = visits_today
        extra_context["visits_week"] = visits_week
        extra_context["visits_month"] = visits_month
        extra_context["top_paths"] = top_paths

        return super().changelist_view(request, extra_context=extra_context)
