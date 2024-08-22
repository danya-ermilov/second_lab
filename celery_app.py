from celery import Celery

celery_app = Celery(
    "booking_system",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

# Убедитесь, что задачи импортированы
import app.tasks  # Импорт задач для регистрации в Celery

celery_app.conf.update(
    task_routes={
        "app.tasks.remove_booking_after_end": {"queue": "bookings"},
    }
)


