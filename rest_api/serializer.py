from web.models import *
from rest_framework import serializers


class QuestionAnswerSerializer(serializers.ModelSerializer):
    bank_name = serializers.CharField(source='bank.name')

    class Meta:
        model = QuestionAnswer
        fields = '__all__'



class BankSerializer(serializers.ModelSerializer):
    questionanswer_set = serializers.StringRelatedField(many=True)
    class Meta:
        model = Bank
        fields = '__all__'

