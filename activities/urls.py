from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from activities import views

urlpatterns = [
    url(r'^activities/$', views.ActivityList.as_view()),
    url(r'^activities/(?P<pk>[0-9]+)/$', views.ActivityDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
