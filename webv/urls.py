from django.conf.urls import url

from webv.views import show_r

urlpatterns = [
    url(r'^', show_r)
]

