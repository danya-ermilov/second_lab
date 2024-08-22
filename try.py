from app.tasks import remove_booking_after_end

# Отправка задачи на выполнение
remove_booking_after_end.delay(booking_id=2, end_time="2024-08-22T14:21:00")
