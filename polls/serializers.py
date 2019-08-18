from rest_framework import serializers

from .models import Question, Choice
#  Old Way Implemetation
# class QuestionSerializer(serializers.Serializer):
#     question_text = serializers.CharField(max_length=200)
#     pub_date = serializers.DateTimeField()
#     was_published_recently = serializers.BooleanField(read_only=True)
#     # Add following to QuestionSerializer
#     verbose_question_text = serializers.CharField(read_only=True)
#     choices = ChoiceSerializer(many=True, read_only=True)

#     # DRF serializer.save() calls self.create(self.validated_data)
#     def create(self, validated_data):
#         return Question.objects.create(**validated_data)

#     # Add update() implementation on QuestionSerializer
#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance


class ChoiceSerializer(serializers.Serializer):
    choice_text = serializers.CharField(max_length=200)
    
    def create(self, validated_data):
        return Choice.objects.create(**validated_data)


class QuestionListPageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    question_text = serializers.CharField(max_length=200)
    pub_date = serializers.DateTimeField()
    was_published_recently = serializers.BooleanField(read_only=True) # Serializer is smart enough to understand that was_published_recently is a method on Question

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class QuestionDetailPageSerializer(QuestionListPageSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)


class VoteSerializer(serializers.Serializer):
    choice_id = serializers.IntegerField()
