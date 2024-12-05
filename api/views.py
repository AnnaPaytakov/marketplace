from django.http import JsonResponse                                                                                #type:ignore                                                  
from rest_framework.decorators import api_view, permission_classes  #type:ignore
from rest_framework.response import Response  #type:ignore
from .serializers import ProductSerializer
from products.models import Product
from rest_framework.permissions import IsAuthenticated #type:ignore

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'api/products'},
        {'GET': 'api/product/id'},
        {'POST': 'api/product/id/add-to-cart/'},
        {'POST': 'api/product/id/subtract-from-cart/'},
    ]
    return Response(routes)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProducts(request):
    products =  Product.objects.all()
    serializer = ProductSerializer(products, many=True) #many=True елси несколько объектов, many=False для 1 объекта
    return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
    product =  Product.objects.get(id=pk)
    serializer = ProductSerializer(product, many=False) #many=True елси несколько объектов, many=False для 1 объекта
    return Response(serializer.data)