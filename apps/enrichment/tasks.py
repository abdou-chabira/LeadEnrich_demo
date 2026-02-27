from celery import shared_task
from .models import Lead
from .services import HubSpotSim, ClearbitSim, LinkedInSim, RiskScorer

@shared_task(bind=True, max_retries=3)
def enrich_lead(self, lead_id):
    lead = Lead.objects.get(id=lead_id)
    try:
        lead.status = "processing"
        lead.save()

        hub = HubSpotSim().enrich(lead.email)
        clear = ClearbitSim().enrich(lead.email)
        linkedin = LinkedInSim().enrich(lead.email)
        risk = RiskScorer().score(lead.email)

        lead.enrichment_data = {**hub, **clear, **linkedin, "risk_score": risk}
        lead.status = "completed"
        lead.enriched = True
        lead.save()
    except Exception as exc:
        lead.status = "failed"
        lead.retry_count += 1
        lead.save()
        raise self.retry(exc=exc, countdown=2 ** lead.retry_count)