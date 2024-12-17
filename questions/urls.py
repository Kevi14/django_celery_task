from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, ChoiceViewSet

router = DefaultRouter()
router.register(r"questions", QuestionViewSet, basename="question")
router.register(r"choices", ChoiceViewSet, basename="choice")

urlpatterns = router.urls
