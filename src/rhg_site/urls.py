from django.conf.urls import patterns, include, url
from headlines import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	url(r'^randomheadline', views.random_headline, name="random_headline")
)
