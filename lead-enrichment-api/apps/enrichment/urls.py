from django.urls import path
from .views import EnrichLeadView, MonitoringView

urlpatterns = [
    path("enrich-lead/", EnrichLeadView.as_view()),
    path("monitoring/", MonitoringView.as_view()),
]