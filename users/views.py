from django.shortcuts import render, redirect
from users.forms import UsersForms
from django.views.decorators.csrf import csrf_exempt
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
