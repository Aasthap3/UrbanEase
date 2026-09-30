from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.amenities import router as amenities_router
from app.api.health import router as health_router
from app.api.locations import router as locations_router
from app.api.personalized_score import router as personalized_score_router
from app.api.preferences import router as preferences_router
from app.api.score import router as score_router

app = FastAPI(
    title='UrbanEase API',
    version='0.1.0',
    description='UrbanEase geospatial neighborhood discovery backend.',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173', 'http://127.0.0.1:5173'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health_router, prefix='/api')
app.include_router(auth_router, prefix='/api')
app.include_router(amenities_router, prefix='/api')
app.include_router(locations_router, prefix='/api')
app.include_router(score_router, prefix='/api')
app.include_router(preferences_router, prefix='/api')
app.include_router(personalized_score_router, prefix='/api')


@app.get('/')
async def root() -> dict[str, str]:
    return {'message': 'UrbanEase backend is running', 'status': 'ok'}
