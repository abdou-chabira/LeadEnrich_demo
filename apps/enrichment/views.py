from rest_framework.views import APIView
from rest_framework.response import Response
from apps.common.utils import rate_limit
from .models import Lead
from .tasks import enrich_lead
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views import View
import logging

logger = logging.getLogger(__name__)

def index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        logger.info(f"Received lead enrichment request for email: {email}")
        if email:
            lead = Lead.objects.create(email=email, status="pending")
            logger.info(f"Created Lead object with ID: {lead.id}")
            enrich_lead.delay(str(lead.id))
            logger.info(f"Triggered async enrichment for Lead ID: {lead.id}")
            return redirect("results")
    return render(request, "enrichment/index.html")

def results(request):
    leads = Lead.objects.order_by("-created_at")[:20]
    return render(request, "enrichment/results.html", {"leads": leads})

class EnrichLeadView(APIView):
    def post(self, request):
        ip = request.META.get("REMOTE_ADDR")
        logger.info(f"API enrichment request from IP: {ip}")
        if not rate_limit(f"rate:{ip}"):
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return Response({"error": "rate limit exceeded"}, status=429)

        idempotency_key = request.headers.get("Idempotency-Key")
        if idempotency_key:
            existing = Lead.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                logger.info(f"Idempotent request: returning existing Lead ID: {existing.id}")
                return Response({"lead_id": existing.id, "status": existing.status, "idempotent": True})

        lead = Lead.objects.create(
            email=request.data.get("email"),
            idempotency_key=idempotency_key,
            status="pending"
        )
        logger.info(f"Created Lead via API with ID: {lead.id}")
        enrich_lead.delay(str(lead.id))
        logger.info(f"Triggered async enrichment for Lead ID: {lead.id} via API")
        return Response({"lead_id": lead.id, "status": "accepted"})

class MonitoringView(APIView):
    def get(self, request):
        logger.info("Monitoring endpoint accessed.")
        stats = Lead.objects.values("status").annotate(count=Count("id"))
        total = Lead.objects.count()
        logger.info(f"System stats: total_leads={total}, by_status={list(stats)}")
        return Response({"total_leads": total, "by_status": stats, "system": "healthy"})

class MonitoringUI(View):
    def get(self, request):
        return render(request, "enrichment/monitoring.html")