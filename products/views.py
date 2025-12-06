from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import redirect, render
from django.views.generic import ListView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

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


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def product_list_api(request):
    # ✅ Anyone logged in can view products
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products,many=True)
        return Response(serializer.data)

    # ✅ Only ADMIN can create
    elif request.method == 'POST':
        if not request.user.is_staff:
            return Response(
                {"error": "Only admins can create products"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def product_create_api(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response({'error': 'Product Not Found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    if not request.user.is_staff:
        return Response({"error": "only admin can do this"}, status=status.HTTP_403_FORBIDDEN)

    elif request.method == 'PATCH':
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response({"message": "Product deleted"}, status=status.HTTP_204_NO_CONTENT)
