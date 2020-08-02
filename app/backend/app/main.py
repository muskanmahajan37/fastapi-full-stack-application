from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette_exporter import PrometheusMiddleware, handle_metrics

from app.api.api.api import api_router
from app.core import config
from app.core.celery_app import celery_app
from app.core.config import PROJECT_NAME, DEBUG, DOCS_URL, OPENAPI_URL, ALLOWED_HOSTS, VERSION, API_PORT
from app.db.session import SessionLocal


def get_application() -> FastAPI:
    app = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION, docs_url=DOCS_URL, openapi_url=OPENAPI_URL)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


app = get_application()
app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", handle_metrics)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response


@app.get("/api/v1")
def root_def():
    return {"OK": "OK"}


@app.get("/api/task")
async def example_task():
    celery_app.send_task("app.task.example_task", args=["Hello World"])
    return {"message": "success"}


app.include_router(api_router, prefix=config.API_V1_PREFIX)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=API_PORT)
