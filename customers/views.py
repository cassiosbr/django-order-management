from rest_framework import status
from rest_framework.views import APIView, Response

from customers.models import Customer
from customers.serializers import CustomerSerializer

from opentelemetry import trace

tracer = trace.get_tracer(__name__)

import time

class CustomersView(APIView):
    def get(self, request):
        with tracer.start_as_current_span("customers.api.get_customers") as span:            
            time.sleep(1)  # Simula um atraso de 1 segundo para demonstrar o cache
            queryset = Customer.objects.filter(is_active=True)
            serializer = CustomerSerializer(queryset, many=True)

            span.set_attribute("http.method", request.method)
            span.set_attribute("http.route", request.path)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        with tracer.start_as_current_span("customers.api.create_customer") as span:

            time.sleep(2)  # Simula um atraso de 2 segundos para demonstrar o cache
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.route", request.path)
            # Logic to create a new customer
            return Response({"message": "Customer created"}, status=status.HTTP_201_CREATED)