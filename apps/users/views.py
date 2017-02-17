from django.contrib.auth import authenticate,login
from django.shortcuts import render


# Create your views here.
def login(request):
    if request.method == "POST":
        user_name = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(user_name, password)
        if user is not None:
            login(request,user)
            return render(request,"index.html")
    elif request.method == 'GET':
        return render(request, 'login.html', {})
