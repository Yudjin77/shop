from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, render
from .forms import CustomUserCreationForm, CustomUserLoginForm, \
    CusstomUserUpdateForm
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print('work')
        if form.is_valid():
            print('work2')
            user = form.save()
            user = authenticate(request, email=user.email, password=form.cleaned_data['password1'])
            if user is not None:
                login(request, user)
            return JsonResponse({'success': True})
        else:
            print('send')
            return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)
    return JsonResponse({'error': 'POST method required'}, status=405)


def login_view(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors.get_json_data()}, status=400)
    return JsonResponse({'error': 'POST method required'}, status=405)


@login_required
def profile_view(request):
    form = CusstomUserUpdateForm(instance=request.user)
    return render(request, 'users/profile.html', {'form': form})

@login_required
def update_account_details(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        form = CusstomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def logout_view(request):
    logout(request)
    return redirect('products:index')