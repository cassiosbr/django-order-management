from rest_framework.views import APIView, Response
from opentelemetry import trace

from orders.serializers import OrderSerializer
from orders.services import OrderService

tracer = trace.get_tracer(__name__)

class OrdersView(APIView):

    def post(self, request):
        with tracer.start_as_current_span("orders.api.create_order") as span:
            serializer = OrderSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            order = OrderService().create_order(
                serializer.validated_data
            )

            span.set_attribute("order.id", order.id)
            span.set_attribute("http.method", request.method)
            span.set_attribute("http.route", request.path)

        return Response(
            {
                "id": order.id,
                "status": order.status
            },
            status=201
        )