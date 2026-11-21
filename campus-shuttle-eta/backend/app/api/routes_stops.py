from fastapi import APIRouter

def create_stops_router(stops):
    router = APIRouter(prefix="/stops", tags=["Stops"])

    @router.get("")
    async def get_all_stops():
        return {"stops": stops}

    return router
