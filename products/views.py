from django.core.cache import cache
from rest_framework import pagination, status
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product
from products.serializers import ProductCreateSerializer, ProductSerializer

class CustomSetPagination(pagination.PageNumberPagination):
    page_size = 50
    page_query_param = 'page'
    max_page_size = 4000
    page_size_query_param = 'limit'



class ProductsView(APIView):
    def get(self, request):
        page = request.query_params.get('page', '1')
        limit = request.query_params.get('limit', str(CustomSetPagination.page_size))
        cache_version = cache.get('products:list:version', 1)
        cache_key = f'products:list:v:{cache_version}:page:{page}:limit:{limit}'

        cached_response = cache.get(cache_key)
        if cached_response is not None:
            return Response(cached_response, status=status.HTTP_200_OK)

        queryset = Product.objects.filter(is_active=True).order_by('created_at')
        paginator = CustomSetPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(paginated_queryset, many=True)
        response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key, response.data, timeout=60)
        return response

    def post(self, request):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Invalide o cache da lista paginada rotacionando a versão.
            version_key = 'products:list:version'
            if cache.get(version_key) is None:
                cache.set(version_key, 1, timeout=None)
            try:
                cache.incr(version_key)
            except ValueError:
                current_version = cache.get(version_key, 1)
                cache.set(version_key, current_version + 1, timeout=None)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
