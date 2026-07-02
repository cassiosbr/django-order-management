from rest_framework.views import APIView, Response

from orders.serializers import OrderSerializer


class OrdersView(APIView):

    def post(self, request):

        serializer = OrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            {
                "message": "Order created successfully",
            },
            status=201
        )