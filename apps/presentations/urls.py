from django.urls import path
from .views import Gallery
from .views import Contact
from .views import HomeView

app_name = 'presentations'

urlpatterns = [
    path("gallery/", Gallery.as_view(), name="gallery"),
    path("contact/", Contact.as_view(), name="contact"),
    path("home/", HomeView.as_view(), name="home"),
]


