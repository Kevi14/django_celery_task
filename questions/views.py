from rest_framework import viewsets, permissions
from .models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer
from custom_auth.helpers import HasObjectPermission
from custom_auth.constants import ActionEnum
from custom_auth.models import ObjectPermission
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from custom_auth.models import CustomUser

class QuestionViewSet(viewsets.ModelViewSet):
    """
    A viewset for performing CRUD operations on Questions.
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated, HasObjectPermission]

    def perform_create(self, serializer):
        """
        Override create to set the currently authenticated user as the creator
        and grant full CRUD permissions to the user.
        """
        # Save the Question instance and set the user as created_by
        question = serializer.save(created_by=self.request.user)

        # Grant full permissions (CRUD) to the user
        actions = [ActionEnum.VIEW, ActionEnum.CREATE, ActionEnum.EDIT, ActionEnum.DELETE]
        for action in actions:
            ObjectPermission.objects.create(
                user=self.request.user,
                action=action.value,
                object_id=question.id
            )


    def get_queryset(self):
        """
        Filter the queryset based on object-level or global permissions.
        """
        queryset = super().get_queryset()
        object_ids = ObjectPermission.objects.filter(
            user=self.request.user,
            action=ActionEnum.VIEW.value
        ).values_list("object_id", flat=True)

        has_global_permission = ObjectPermission.objects.filter(
            user=self.request.user,
            action=ActionEnum.VIEW.value,
            object_id__isnull=True
        ).exists()

        if has_global_permission:
            return queryset

        # Otherwise, filter based on specific object permissions
        return queryset.filter(id__in=object_ids)

class ChoiceViewSet(viewsets.ModelViewSet):
    """
    A viewset for performing CRUD operations on Choices.
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAuthenticated, HasObjectPermission]

    def get_queryset(self):
        """
        Filter the queryset based on related Question's permissions,
        including global view permissions.
        """
        queryset = super().get_queryset()
        object_ids = ObjectPermission.objects.filter(
            user=self.request.user,
            action=ActionEnum.VIEW.value
        ).values_list("object_id", flat=True)

        has_global_permission = ObjectPermission.objects.filter(
            user=self.request.user,
            action=ActionEnum.VIEW.value,
            object_id__isnull=True
        ).exists()

        if has_global_permission:
            return queryset

        # Otherwise, filter choices based on specific Question permissions
        return queryset.filter(question__id__in=object_ids)

class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "questions/question_list.html"
    context_object_name = "questions"

    def get_queryset(self):
        """
        Filter questions based on user permissions.
        If admin, allow filtering by user via GET parameter `user_id`.
        """
        user = self.request.user
        queryset = Question.objects.all()

        # Admins see all questions; others see filtered based on VIEW permission
        if not user.is_superuser:
            permitted_ids = ObjectPermission.objects.filter(
                user=user, action=ActionEnum.VIEW.value
            ).values_list("object_id", flat=True)
            queryset = queryset.filter(id__in=permitted_ids)

        # Additional filtering for admin users
        if user.is_superuser and "user_id" in self.request.GET:
            user_id = self.request.GET.get("user_id")
            if user_id and len(user_id) > 7:
                queryset = queryset.filter(created_by_id=user_id)

        return queryset

    def get_context_data(self, **kwargs):
        """
        Add users list for admin filtering in the template.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_superuser:
            context["users"] = CustomUser.objects.all()
        return context
