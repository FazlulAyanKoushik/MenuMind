from app.tasks.celery_app import celery_app


@celery_app.task
def aggregate_daily_stats():
    return "Daily stats aggregated"
