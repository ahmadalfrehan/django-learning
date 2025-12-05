from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import ListView

from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer
from products.forms import ProductForm
from .models import Product
from rest_framework import status
from django.views.generic.edit import CreateView
from rest_framework.decorators import api_view
# Create your views here.


class ProductList(ListView):
    model = Product
    paginate_by = 10

    def render_to_response(self, context, **response_kwargs):
        items = list(context["object_list"].values(
            "name", "price", "description", "username__username"))

        return JsonResponse({"products": items})


class ProductCreate(CreateView):
    model = Product

    fields = '__all__'


def home(request):
    return render(request=request, template_name='products/product.html', context={'name': 'ahmad'})


def myvi(request):
    # if request.method == 'GET':
    #
    # return render(request=request, template_name='products/product.html', context={"formProd": formProd})
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = ProductForm()
        return render(request=request, template_name='products/product.html', context={"formProd": form})


@api_view(['GET'])
def product_list_api(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE', 'POST'])
def product_create_api(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except product.DoesNotExist:
        return Response({'error': 'Product Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    elif request.method == 'PATCH':
        serializer = ProductSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
