from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache

from apps.visits.views import BaseVisitView


class HomeView(BaseVisitView, View):
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
