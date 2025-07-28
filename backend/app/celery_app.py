from __future__ import annotations

from celery import Celery

celery_app = Celery(
    'ai_orchestrator',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.task_routes = {
    'backend.app.tasks.*': {'queue': 'default'},
}
