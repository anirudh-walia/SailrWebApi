import logging
import sys

print("-------------->>>>", sys.path)
import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi_pagination import add_pagination
from router.wait_list_log_router import api_router as wait_list_log_router
from router.colleges_router import api_router as colleges_router
from settings import settings
from starlette.middleware.cors import CORSMiddleware

logging.basicConfig(
    filename="logs/api-location.log",
    encoding="utf-8",
    level=logging.DEBUG,
    format="%(asctime)s:%(levelname)s:%(pathname)s:%(message)s",
    datefmt=("%Y-%m-%d %H:%M:%S"),
)
logger = logging.getLogger(__name__)

# Initialize app
app = FastAPI(title=settings.PROJECT_NAME, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="1.0",
        description="",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {"url": ""}
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# ----------- Routers---------

app.include_router(
    colleges_router,
    prefix="/Colleges",
    tags=["Colleges"],
)

app.include_router(
    wait_list_log_router,
    prefix="/waitListLog",
    tags=["WaitListLog"],
)
add_pagination(app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9001)
