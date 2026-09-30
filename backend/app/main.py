from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.health import router as health_router

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


@app.get('/')
async def root() -> dict[str, str]:
    return {'message': 'UrbanEase backend is running', 'status': 'ok'}
