import json
from django.utils.dateparse import parse_datetime
from celery import shared_task
from .models import UserActivity
import redis


@shared_task
def save_user_activity_to_db():
    redis_client = redis.StrictRedis(host='redis', port=6379, db=0)
    activities = []

    while True:
        visit_data = redis_client.rpop("user_activity")
        if not visit_data:
            break
        visit = json.loads(visit_data)
        activities.append(UserActivity(
            user=visit["user"],
            path=visit["path"],
            method=visit["method"],
            timestamp=parse_datetime(visit["timestamp"]),
        ))

    if activities:
        UserActivity.objects.bulk_create(activities)
