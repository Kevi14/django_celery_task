from rest_framework import serializers
from .models import Question,Choice
from django.db.models import Sum

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'votes', 'question_id']
        read_only_fields = ['question_id']

class QuestionSerializer(serializers.ModelSerializer):
    # Custom calculated fields
    total_choices = serializers.SerializerMethodField()
    total_votes = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'title', 'created_at', 'created_by', 'total_choices', 'total_votes']
        read_only_fields = ['created_by', 'created_at']

    def get_total_choices(self, obj):
        """Calculate the total number of choices for this question."""
        return obj.choices.count()

    def get_total_votes(self, obj):
        """Calculate the total number of votes across all choices."""
        return obj.choices.aggregate(total_votes=Sum('votes'))['total_votes'] or 0
