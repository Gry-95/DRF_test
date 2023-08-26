from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins

from .models import Women, Category
from .permissions import IsAdminReadOnly
from .serializers import WomenSerializer


# Create your views here.
class WomenAPIListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 10000


class WomenViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):  # ModelViewSet
    serializer_class = WomenSerializer
    permission_classes = (IsAuthenticated,)  # В кортеж добавляем классы для ограничения доступа
    pagination_class = WomenAPIListPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')

        if not pk:
            return Women.objects.all()

        return Women.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)  # Добавляет маршрут /women/1/category/ , имя берется из названия метода
    def category(self, request, pk):
        cats = Category.objects.get(pk=pk)
        return Response({'cats': cats.name})

# class WomenAPIView(generics.ListAPIView):
# queryset = Women.objects.all()
# serializer_class = WomenSerializer

# class WomenAPIList(generics.ListCreateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
# class WomenAPIUpdate(generics.UpdateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

# class WomenAPIView(APIView):
#     def get(self, request):
#         w = Women.objects.all()
#         return Response({'posts': WomenSerializer(w,
#                                                   many=True).data})  # many для того чо бы сериализатор понимал, что будет обрабатывать множество записей, а не одну
#
#     def post(self, request):
#         serializer = WomenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)  # raise_exception=True вернет JSON с ошибкой, а не html с ошибкой
#         serializer.save()
#         # post_new = Women.objects.create(
#         #     title=request.data['title'],
#         #     content=request.data['content'],
#         #     cat_id=request.data['cat_id']
#         # ) # Вместо этого написал метод create в serializers.py
#
#         return Response({'post': serializer.data})
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'Error': 'Method PUT NOT allowed'})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({'Error': 'Objects does NOT exists'})
#
#         serializer = WomenSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({'post': serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get('pk', None)
#         if not pk:
#             return Response({'Error': 'Method DELETE NOT allowed'})
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({'Error': 'Objects does NOT exists'})
#         instance.delete()
#         return Response({'post': 'delete post ' + str(pk)})
