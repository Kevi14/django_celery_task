from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import json

class Command(BaseCommand):
    help = "Sets up the periodic task to create random questions every hour"

    def handle(self, *args, **options):
        # Create interval schedule for every 1 hour
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.HOURS,
        )
        if created:
            self.stdout.write(self.style.SUCCESS("Interval schedule created: Every 1 hour"))
        else:
            self.stdout.write(self.style.WARNING("Interval schedule already exists: Every 1 hour"))

        # Create or update the periodic task
        task_name = "Create Random Question Every Hour"
        task, task_created = PeriodicTask.objects.get_or_create(
            interval=schedule,
            name=task_name,
            defaults={
                "task": "questions.tasks.create_random_question_with_choices",
                "args": json.dumps([]),
            }
        )

        if not task_created:
            task.task = "questions.tasks.create_random_question_with_choices"
            task.save()
            self.stdout.write(self.style.WARNING(f"Task '{task_name}' updated."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Task '{task_name}' created successfully."))

        self.stdout.write(self.style.SUCCESS("Periodic task setup completed successfully."))
