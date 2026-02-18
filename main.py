
from fastapi import FastAPI

from routes.hazard import hazard_router

from routes.scoring import scoring_router
from routes.routing import routing_router

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Safety-First Navigation API is running"}



# Include hazard reporting, scoring, and routing routers
app.include_router(hazard_router)
app.include_router(scoring_router)
app.include_router(routing_router)
