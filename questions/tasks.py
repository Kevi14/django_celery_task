# questions/tasks.py
import random
from celery import shared_task
from django.utils import timezone
from questions.models import Question, Choice
from custom_auth.models import CustomUser, ObjectPermission
from custom_auth.constants import ActionEnum


@shared_task
def create_random_question_with_choices():
    """
    Create a new Question with random Choices. Set 'created_by' as the admin user
    and grant view permissions to a single random non-admin user.
    """
    admin_user = CustomUser.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("No admin user available.")
        return

    other_users = CustomUser.objects.filter(is_superuser=False)
    if not other_users.exists():
        print("No non-admin users to assign view permissions.")
        return

    random_user = random.choice(other_users)

    question_title = f"Auto-Generated Question {timezone.now().strftime('%Y-%m-%d %H:%M:%S')}"
    question = Question.objects.create(title=question_title, created_by=admin_user)

    num_choices = random.randint(2, 5)
    for i in range(num_choices):
        Choice.objects.create(
            question=question,
            text=f"Choice {i+1}",
            votes=0
        )

    ObjectPermission.objects.create(
        user=random_user,
        action=ActionEnum.VIEW.value,
        object_id=question.id
    )

    print(f"Created Question '{question.title}' with {num_choices} choices, created by admin '{admin_user.email}'.")
    print(f"View permissions granted to user '{random_user.email}'.")
