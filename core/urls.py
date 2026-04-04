from django.urls import path
from core.views import index, lp

urlpatterns = [
    path("core/", index, name="core"),
    path("landing/", lp, name="landing page")

]