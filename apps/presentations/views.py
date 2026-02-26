from django.views.generic import TemplateView

# Create your views here.
class HomeView(TemplateView):
    template_name = "presentations/home.html" 

class Gallery(TemplateView):
    template_name = "presentations/gallery.html" 

class Contact(TemplateView):
    template_name = "presentations/contact.html" 



