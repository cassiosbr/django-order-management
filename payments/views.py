from rest_framework import status
from rest_framework.views import APIView, Response

from payments.serializers import PaymentWebhookSerializer


class PaymentWebhookView(APIView):

    def post(self, request):

        serializer = PaymentWebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)


        return Response(status=status.HTTP_200_OK)
