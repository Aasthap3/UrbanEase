from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.core.database import engine

router = APIRouter()


@router.get('/health')
async def health_check() -> dict[str, str]:
    return {
        'status': 'ok',
        'service': 'UrbanEase Backend',
        'message': 'Healthy and ready for neighborhood analysis.',
    }


@router.get('/health/db')
async def database_health_check() -> dict[str, str]:
    try:
        with engine.connect() as connection:
            version = connection.execute(text('SELECT PostGIS_Version();')).scalar_one()
        return {
            'status': 'ok',
            'database': 'connected',
            'postgis': 'available',
            'version': version,
        }
    except Exception as exc:  # pragma: no cover - handled by FastAPI error
        raise HTTPException(status_code=503, detail='Database connection failed') from exc
