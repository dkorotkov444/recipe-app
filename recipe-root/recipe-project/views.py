# recipe-project/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm

# 1. Login View
def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to 'next' if it exists, otherwise to recipes_list
                return redirect(request.GET.get('next', 'recipes:recipes_list'))
        else:
            error_message = 'Invalid username or password.'

    context = {
        'form': form, 
        'error_message': error_message
    }
    return render(request, 'login.html', context)

# 2. Logout View
def logout_view(request):
    logout(request)
    return redirect('logout_success')