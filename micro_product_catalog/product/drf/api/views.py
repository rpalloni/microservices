from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from .producer import publish

class ProductViewSet(viewsets.ViewSet):
    
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        publish('product_created', serializer.data) # create event to send
        print('product created!!!')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    ''' postman POST body example
    {
        "pr_title": "book X1",
        "pr_image": "book X1 image",
        "pr_catal": "1"
    }
    '''

    def retrieve(self, request, pk=None):
        product = Product.objects.get(pr_id = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        product = Product.objects.get(pr_id = pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # TODO: publish('product_updated', serializer.data) # update event to send
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        product = Product.objects.get(pr_id = pk)
        product.delete()
        # TODO: publish('product_deleted', pk) # delete event to send
        return Response('bye!', status=status.HTTP_204_NO_CONTENT)


