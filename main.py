from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.hazard import hazard_router
from routes.scoring import scoring_router
from routes.routing import routing_router

app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Safety-First Navigation API is running"}



# Include hazard reporting, scoring, and routing routers
app.include_router(hazard_router)
app.include_router(scoring_router)
app.include_router(routing_router)
