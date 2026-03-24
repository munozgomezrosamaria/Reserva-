from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = "presentations/home.html" 

class Gallery(TemplateView):
    template_name = "presentations/gallery.html" 

class Contact(TemplateView):
    template_name = "presentations/contact.html" 

class Reservations(TemplateView):
    template_name = "presentations/reservations.html"

from django.views.generic import TemplateView
from apps.services.models import Service

class Services(TemplateView):
    template_name = "presentations/services.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.all()
        return context



