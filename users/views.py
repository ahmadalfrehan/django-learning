from django.shortcuts import render, redirect
from users.forms import UsersForms
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from users.serializers import RegisterSerializer


@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = UsersForms(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or any other page

    else:  # GET request
        form = UsersForms()

    return render(request, 'users.html', {'form': form})


@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
