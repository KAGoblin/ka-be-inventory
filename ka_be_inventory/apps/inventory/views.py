from oscar.core.loading import get_class
from oscar.core.loading import get_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ka_be_inventory.apps.inventory.serializers import ValidateProductAvailabilitySerializer

Selector = get_class("partner.strategy", "Selector")

Product = get_model('catalogue', 'Product')

# Create your views here.


class ValidateProductAvailability(APIView):
    """
    POST(product_id, quantity)
    {
        "product_id": 209,
        "quantity": 6 -> # total qty same product many stockrecords
    }
    """
    serializer_class = ValidateProductAvailabilitySerializer

    def validate(self, request, product_id, quantity):
        product = Product.objects.get(id=product_id)
        strategy = Selector().strategy(request=request, user=request.user)
        availability = strategy.fetch_for_product(product).availability
        # check if product is available at all
        if not availability.is_available_to_buy:
            return False, availability.message

        # check if we can buy this quantity
        allowed, message = availability.is_purchase_permitted(quantity)
        if not allowed:
            return False, message

        # no check limit --> check on checkout
        # allowed, message = basket.is_quantity_allowed(desired_qty)
        # if not allowed:
        #     return False, message

        return True, None

    def post(self, request, *args, **kwargs):
        ser = self.serializer_class(data=request.data)
        if ser.is_valid():
            availability_valid, message = self.validate(
                request, ser.validated_data['product_id'], ser.validated_data['quantity'])
            if not availability_valid:
                return Response(
                    {"reason": message}, status=status.HTTP_406_NOT_ACCEPTABLE
                )
            return Response({"is_valid": True})
        return Response({"reason": ser.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
