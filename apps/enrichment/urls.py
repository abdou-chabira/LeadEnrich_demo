from django.urls import path
from .views import index, results, EnrichLeadView, MonitoringView, MonitoringUI

urlpatterns = [
    path("", index, name="index"),
    path("results/", results, name="results"),
    path("api/enrich-lead/", EnrichLeadView.as_view()),
    path("api/monitoring/", MonitoringView.as_view()),
    path("monitoring/", MonitoringUI.as_view(), name="monitoring"),
]