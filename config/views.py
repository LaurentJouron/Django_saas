from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.db.models import Count, Q

from apps.visits.models import PageVisit


class HomePageView(View):
    """
    Home page view with visit tracking and analytics.

    This view handles GET requests to the home page, records each visit,
    and provides visit statistics using optimized database queries and caching.

    Attributes:
        template_name (str): Template file path for rendering.
        page_title (str): Title displayed on the page.
        cache_timeout (int): Cache duration in seconds (default: 300 = 5 minutes).
    """

    template_name = "home/home.html"
    page_title = "Home Page"
    cache_timeout = 300  # 5 minutes cache

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to add CSRF protection and disable caching.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: The HTTP response from the parent dispatch method.
        """
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to the home page.

        Records the page visit and renders the template with context data.

        Args:
            request: The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: Rendered template with context data.
        """
        # Record the visit asynchronously for better performance
        self.record_page_visit(request)

        # Prepare and return the context
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def record_page_visit(self, request):
        """
        Record a page visit in the database.

        Creates a new PageVisit entry and invalidates related cache keys
        to ensure fresh data on next request.

        Args:
            request: The HTTP request object containing the path.
        """
        PageVisit.objects.create(path=request.path)

        # Invalidate cache after recording a new visit
        self._invalidate_visit_cache(request.path)

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
            count = PageVisit.objects.count()
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
            count = PageVisit.objects.filter(path=path).count()
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

    def get_context_data(self, **kwargs):
        """
        Prepare the context dictionary for template rendering.

        Gathers all visit statistics for the current page and combines
        them with any additional keyword arguments.

        Args:
            **kwargs: Additional context variables to include.

        Returns:
            dict: Context dictionary containing page statistics and metadata.
        """
        current_path = self.request.path

        context = {
            "page_title": self.page_title,
            "page_visit_count": self.get_page_visit_count(current_path),
            "total_visit_count": self.get_total_visit_count(),
            "page_visit_percentage": self.get_page_visit_percentage(
                current_path
            ),
        }
        context.update(kwargs)
        return context
