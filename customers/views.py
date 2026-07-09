from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView, Response

from customers.models import Customer
from customers.serializers import CustomerSerializer

import time

class CustomersView(APIView):
    def get(self, request):
        # time.sleep(1)  # Simula um atraso de 1 segundo para demonstrar o cache
        queryset = Customer.objects.filter(is_active=True)
        serializer = CustomerSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Logic to create a new customer
        return JsonResponse({"message": "Customer created"})