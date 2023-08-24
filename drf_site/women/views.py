from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Women
from .serializers import WomenSerializer


# Create your views here.
# class WomenAPIView(generics.ListAPIView):
# queryset = Women.objects.all()
# serializer_class = WomenSerializer


class WomenAPIView(APIView):
    def get(self, request):
        w = Women.objects.all()
        return Response({'posts': WomenSerializer(w,
                                                  many=True).data})  # many для того чо бы сериализатор понимал, что будет обрабатывать множество записей, а не одну

    def post(self, request):
        serializer = WomenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # raise_exception=True вернет JSON с ошибкой, а не html с ошибкой

        post_new = Women.objects.create(
            title=request.data['title'],
            content=request.data['content'],
            cat_id=request.data['cat_id']
        )

        return Response({'post': WomenSerializer(post_new).data})
