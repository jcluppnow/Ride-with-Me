"""
Defines the application's HTTP routes.
"""

from django.urls import path

from . import views

urlpatterns = [
                  path('seed', views.cypress_seed, name='cypress_seed'),
                  path('create_event', views.create_event, name='create_event'),
                  path('create_message', views.create_message, name='create_message'),
                  path('create_message_batch', views.create_message_batch, name='create_message_batch'),
              ]
