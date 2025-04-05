from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timedelta

from notifications.email import send_email_reminder

scheduler = BackgroundScheduler()
scheduler.start()

def schedule_email(meeting_time, email, address):
    reminder_time_one = meeting_time - timedelta(minutes=180)
    reminder_time_two = meeting_time - timedelta(minutes=30)

    if reminder_time_one:
        scheduler.add_job(
            func=lambda: send_email_reminder(
                email,
                "Meeting Reminder",
                f"Your meeting at {address} is in 3 hours, scheduled at {meeting_time}."
            ),
            trigger='date',
            run_date=reminder_time_one
        )

    if reminder_time_two:
        scheduler.add_job(
            func=lambda: send_email_reminder(
                email,
                "Meeting Reminder",
                f"Your meeting at {address} is in 30 minutes, scheduled at {meeting_time}."
            ),
            trigger='date',
            run_date=reminder_time_two
        )

