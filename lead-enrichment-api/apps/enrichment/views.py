from rest_framework.views import APIView
from rest_framework.response import Response
from apps.common.utils import rate_limit
from .models import Lead
from .tasks import enrich_lead
from django.db.models import Count

class EnrichLeadView(APIView):
    def post(self, request):
        ip = request.META.get("REMOTE_ADDR")
        if not rate_limit(f"rate:{ip}"):
            return Response({"error": "rate limit exceeded"}, status=429)

        idempotency_key = request.headers.get("Idempotency-Key")
        if idempotency_key:
            existing = Lead.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                return Response({"lead_id": existing.id, "status": existing.status, "idempotent": True})

        lead = Lead.objects.create(
            email=request.data.get("email"),
            idempotency_key=idempotency_key,
            status="pending"
        )
        enrich_lead.delay(str(lead.id))
        return Response({"lead_id": lead.id, "status": "accepted"})

class MonitoringView(APIView):
    def get(self, request):
        stats = Lead.objects.values("status").annotate(count=Count("id"))
        total = Lead.objects.count()
        return Response({"total_leads": total, "by_status": stats, "system": "healthy"})