from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse

from account.models import User
from account.utils import send_activation_code, _generate_activation_code
from user_profile.models import Profile


def ActivateEmail(request):
    email = request.session.get('email')
    name = request.session.get('name')
    password = request.session.get('password')

    if email:
        cache_key = f'activate_email_{email}'
        code = cache.get(cache_key)

        if not code:
            send_activation_code(request, email)
            code = cache.get(cache_key)
            cache.set(cache_key, code, timeout=300)

        if request.method == 'POST':
            input_code = request.POST.get('code')
            if input_code is not None and input_code != '':
                if int(input_code) == code:
                    user = User.objects.create_user(
                        username=email,
                        email=email,
                        first_name=name,
                        password=password
                    )
                    user.is_active = True
                    user.save()

                    Profile.objects.create(
                        user=user,
                    )

                    user = authenticate(request, email=email, password=password)
                    if user is not None:
                        login(request, user)
                        return redirect('/')
                    else:
                        messages.error(request, 'Invalid email or password.')
                        return redirect('sign-in')

                messages.info(request, 'Invalid code!')
                return redirect('activate-email')

        return render(request, 'account/activate.html')
    else:
        return redirect('sign-in')


def SignUp(request):
    if request.method == 'POST':
        name = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email is already registered')
            return redirect('sign-up')
        else:
            request.session['email'] = email
            request.session['name'] = name
            request.session['password'] = password

            return redirect(reverse('activate-email'))

    return render(request, 'account/sign-up.html')


def SignIn(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('sign-in')
        messages.error(request, 'Email is not registered.')
        return redirect('sign-in')

    return render(request, 'account/sign-in.html')


def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        if User.objects.filter(email=email).exists():
            send_activation_code(request, email)
            request.session['email'] = email
            return redirect('confirm-code')
        else:
            messages.error(request, 'Email is not registered.')
            return redirect('forgot-password')

    return render(request, 'account/forgot-password.html')


def ConfirmCode(request):
    if request.method == 'POST':
        email = request.session.get('email')
        input_code = request.POST.get('code')

        code = cache.get(f'activate_email_{email}')
        if code is not None:
            if int(input_code) == code:
                return redirect('reset-password')
            else:
                messages.info(request, 'Invalid code!')
                return redirect('confirm-code')
        else:
            messages.info(request, 'Code is expired!')
            return redirect('forgot-password')

    return render(request, 'account/confirm-code.html')


def ResetPassword(request):
    if request.method == 'POST':
        email = request.session.get('email')
        password = request.POST.get('password')

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        return redirect('sign-in')

    return render(request, 'account/reset-password.html')


def SignOut(request):
    request.session.pop('email', None)
    request.session.pop('name', None)
    request.session.pop('password', None)

    logout(request)
    return redirect('/')
