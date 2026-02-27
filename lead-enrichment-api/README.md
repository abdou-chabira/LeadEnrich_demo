![Lead Enrichment API](leadEnrichapi.png)
![Lead Enrich UI](leadenrich_ui.png)

# Lead Enrichment API

## Features

- Async lead enrichment using Celery
- Multiple simulated providers: HubSpot, Clearbit, LinkedIn
- Risk/Fraud scoring simulation
- Idempotency support with Idempotency-Key header
- Rate limiting using Redis
- Monitoring endpoint for system stats
- Dockerized & production-ready

## Run locally

1. `docker-compose up --build`
2. POST `/api/enrich-lead/` with JSON `{"email":"test@example.com"}` and optional `Idempotency-Key` header
3. GET `/api/monitoring/` for stats
