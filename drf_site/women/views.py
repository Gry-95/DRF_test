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
        serializer.save()
        # post_new = Women.objects.create(
        #     title=request.data['title'],
        #     content=request.data['content'],
        #     cat_id=request.data['cat_id']
        # ) # Вместо этого написал метод create в serializers.py

        return Response({'post': serializer.data})

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': 'Method PUT NOT allowed'})

        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({'Error': 'Objects does NOT exists'})

        serializer = WomenSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'post': serializer.data})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({'Error': 'Method DELETE NOT allowed'})
        try:
            instance = Women.objects.get(pk=pk)
        except:
            return Response({'Error': 'Objects does NOT exists'})
        instance.delete()
        return Response({'post': 'delete post ' + str(pk)})
