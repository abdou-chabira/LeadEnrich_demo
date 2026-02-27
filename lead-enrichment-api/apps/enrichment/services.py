import time
import random

class HubSpotSim:
    def enrich(self, email):
        time.sleep(1)
        return {"company": "ACME Corp", "job_title": "Software Engineer"}

class ClearbitSim:
    def enrich(self, email):
        time.sleep(1)
        return {"first_name": "John", "last_name": "Doe"}

class LinkedInSim:
    def enrich(self, email):
        time.sleep(1)
        return {"linkedin_profile": f"https://linkedin.com/in/{email.split('@')[0]}"}

class RiskScorer:
    def score(self, email):
        return random.randint(1, 100)