import logging

from django.shortcuts import render
from django.views import View
from django.core.cache import cache

from .models import Visit

logger = logging.getLogger(__name__)


class BaseVisitView(View):
    def record_page_visit(self, request):
        """
        Record a page visit in the database.

        Creates a new PageVisit entry and invalidates related cache keys
        to ensure fresh data on next request.

        Args:
            request: The HTTP request object containing the path.
        """
        try:
            Visit.objects.create(path=request.path)
            # Invalidate cache after successfully recording the visit
            self._invalidate_visit_cache(request.path)
        except Exception as e:
            # Log the error but don't break the page rendering
            logger.error(f"Failed to record page visit: {e}", exc_info=True)

    def _invalidate_visit_cache(self, path):
        """
        Invalidate all cached visit statistics.

        Args:
            path (str): The page path for which to invalidate cache.
        """
        cache_keys = [
            "total_visit_count",
            f"page_visit_count_{path}",
            f"page_visit_percentage_{path}",
        ]
        cache.delete_many(cache_keys)

    def get_total_visit_count(self):
        """
        Get the total number of page visits across all pages.

        Uses caching to improve performance. Cache is invalidated when
        a new visit is recorded.

        Returns:
            int: Total number of page visits.
        """
        cache_key = "total_visit_count"
        count = cache.get(cache_key)

        if count is None:
            count = Visit.objects.count()
            cache.set(cache_key, count, self.cache_timeout)

        return count

    def get_page_visit_count(self, path):
        """
        Get the number of visits for a specific page path.

        Uses caching to improve performance for frequently accessed paths.

        Args:
            path (str): The page path to count visits for.

        Returns:
            int: Number of visits for the specified path.
        """
        cache_key = f"page_visit_count_{path}"
        count = cache.get(cache_key)

        if count is None:
            count = Visit.objects.filter(path=path).count()
            cache.set(cache_key, count, self.cache_timeout)

        return count

    def get_page_visit_percentage(self, path):
        """
        Calculate the percentage of visits for a specific page.

        Computes the ratio of visits to a specific path versus total visits.
        Returns 0.0 if there are no total visits to avoid division by zero.

        Args:
            path (str): The page path to calculate percentage for.

        Returns:
            float: Percentage of visits (0-100) for the specified path.
        """
        cache_key = f"page_visit_percentage_{path}"
        percentage = cache.get(cache_key)

        if percentage is None:
            total_count = self.get_total_visit_count()

            # Avoid division by zero
            if total_count == 0:
                percentage = 0.0
            else:
                page_count = self.get_page_visit_count(path)
                percentage = round((page_count / total_count) * 100, 2)

            cache.set(cache_key, percentage, self.cache_timeout)

        return percentage


class VisitsView(View):
    def get(self, request, *args, **kwargs):
        page_title = "Visits Home"
        context = {"page_title": page_title}
        template_name = "visits/home.html"
        return render(request, template_name=template_name, context=context)
