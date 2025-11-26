from django.shortcuts import render
from django.views import View


# Create your views here.
class VisitsView(View):
    def get(self, request, *args, **kwargs):
        page_title = "Visits Home"
        context = {"page_title": page_title}
        template_name = "visits/home.html"
        return render(request, template_name=template_name, context=context)
