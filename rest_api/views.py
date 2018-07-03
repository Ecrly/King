from django.shortcuts import render
from rest_framework import viewsets
from rest_api.serializer import *
from rest_framework.response import Response
# Create your views here.


class QuestionAnswerViews(viewsets.ModelViewSet):

    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer


class BankViews(viewsets.ModelViewSet):

    queryset = Bank.objects.all()
    serializer_class = BankSerializer

class QuestionSearchViews(viewsets.ModelViewSet):
    queryset = QuestionAnswer.objects.all()
    serializer_class = QuestionAnswerSerializer


    # 核心部分就是list方法
    def list(self, request):

        keyword = request.GET.get('bank') # 获取参数
        print(keyword)
        if keyword is not None: # 如果参数不为空
            # 执行filter()方法
            queryset = QuestionAnswer.objects.filter(bank=keyword)
        else:
            # 如果参数为空，执行all()方法
            queryset = QuestionAnswer.objects.all()
        # queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            print(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        # serializer = self.get_serializer(queryset, many=True)
        serializer = QuestionAnswerSerializer(queryset, many=True)
        data = {}
        data['count'] = len(serializer.data)
        data['results'] = serializer.data
        return Response(data) # 最后返回经过序列化的数据


