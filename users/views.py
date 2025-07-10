from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.views.decorators.csrf import csrf_exempt


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
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    return JsonResponse({'error': 'POST method required'}, status=405)


@login_required
def profile_view(request):
    return JsonResponse({'success': True, 'message': 'Profile page'})