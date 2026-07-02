from rest_framework.views import APIView, Response
from orders.serializers import OrderSerializer
from orders.services import OrderService

class OrdersView(APIView):

    def post(self, request):

        serializer = OrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        order = OrderService().create_order(
            serializer.validated_data
        )

        return Response(
            {
                "id": order.id,
                "status": order.status
            },
            status=201
        )