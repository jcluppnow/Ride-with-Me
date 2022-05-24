"""
Defines the application's HTTP routes.
"""

from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
                  path("accounts/register/", views.register, name="register"),
                  path('api/v1/events/attending', views.attending_events),
                  path('api/v1/events/organising', views.organising_events),
                  path('api/v1/events/nearby', views.nearby_events),
                  path('api/v1/events/search', views.event_search),
                  path('api/v1/events/<uuid:pk>.gpx', views.event_gpx),
                  path('api/v1/events/<uuid:pk>.kml', views.event_kml),
                  path('api/v1/events/<uuid:pk>/', views.EventDetail.as_view()),
                  path('api/v1/events/<uuid:pk>/participate', views.participate),
                  path('api/v1/events/<uuid:pk>/check_in', views.check_in),
                  path('api/v1/events/<uuid:pk>/start', views.start_event),
                  path('api/v1/events/<uuid:pk>/finish', views.finish_event),
                  path('api/v1/events/<uuid:pk>/chat', views.EventChatView.as_view()),
                  path('api/v1/events/chat', views.ChatView.as_view()),
                  path('api/v1/events/', views.Events.as_view()),
                  path('api/v1/users/<int:pk>/', views.user_details),
                  path('api/v1/profile', views.Profile.as_view()),
                  path('api/v1/csrf', views.get_csrf),
                  path('api/v1/weather', views.weather),
                  path('api/v1/traffic', views.traffic),
                  path('api/v1/notifications', views.notifications),
                  path('api/v1/notifications/<int:pk>', views.notification),
                  re_path(r'^(?!(api|auth|static|admin|uploads|__cypress__|ws|webpush)).*', views.spa),
              ] \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.UPLOADS_URL, document_root=settings.UPLOADS_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)
