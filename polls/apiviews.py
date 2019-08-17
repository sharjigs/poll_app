from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
import json

from .models import Question, Choice
#from .serializers import QuestionSerializer,ChoiceSerializer
from .serializers import QuestionListPageSerializer,ChoiceSerializer,QuestionDetailPageSerializer


@api_view(['GET', 'POST'])
def questions_view(request):
    if request.method == 'GET':
        # questions = []
        # for question in Question.objects.all():
        #     question_representation = {'question_text': question.question_text, 'pub_date': question.pub_date.strftime("%Y-%m-%d")}
        #     questions.append(question_representation)
        questions = Question.objects.all()
        serializer = QuestionListPageSerializer(questions, many=True)
        return Response(serializer.data)
        #return HttpResponse(json.dumps(questions), content_type='application/json')
    elif request.method == 'POST':
        serializer = QuestionListPageSerializer(data=request.data)
        if serializer.is_valid():
            # question_text = serializer.data['question_text']
            # pub_date = serializer.data['pub_date']
            # Question.objects.create(question_text=question_text, pub_date=pub_date)
            # Question.objects.create(**serializer.validated_data)
            # return Response("Question created", status=status.HTTP_201_CREATED)
            question = serializer.save()
            return Response(QuestionListPageSerializer(question).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PATCH', 'DELETE'])
def question_detail_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'GET':
        serializer = QuestionDetailPageSerializer(question)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = QuestionDetailPageSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionDetailPageSerializer(question).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        question.delete()
        return Response("Question deleted", status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def choices_view(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = ChoiceSerializer(data=request.data)
    if serializer.is_valid():
        choice = serializer.save(question=question)
        return Response(ChoiceSerializer(choice).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    