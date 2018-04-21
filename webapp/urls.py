from django.conf.urls import url

from webapp import views

urlpatterns = [
    url(r'^my_profile/', views.my_profile),


]
