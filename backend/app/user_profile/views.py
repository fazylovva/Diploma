from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash

from article.models import Article
from .models import Profile
from account.models import User


def UserProfile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.filter(user=request.user).first()
        if not profile:
            Profile.objects.create(user=request.user)

        articles = Article.objects.filter(author=request.user).order_by('-created_date')

        context = {
            'profile': profile,
            'empty_fields': profile.empty_fields(),
            'completion_percentage': int(100 - (profile.empty_fields() / 5 * 100)),
            'articles': articles
        }

        return render(request, 'user_profile/profile.html', context)
    else:
        return HttpResponse('', status=404)


def EditProfile(request):
    profile = Profile.objects.filter(user=request.user.id).first()
    articles = Article.objects.filter(author=request.user).order_by('-created_date')

    # POST DATA: Profile contacts
    if request.method == 'POST' and 'first_name' in request.POST:
        avatar = request.FILES.get('avatar')
        first_name = request.POST.get('first_name')
        phone_number = request.POST.get('phone_number')
        country = request.POST.get('country')

        if not first_name:
            messages.error(request, 'First name is required.')
        else:
            if avatar:
                profile.avatar = avatar
            profile.phone_number = phone_number
            profile.country = country
            profile.save()

            User.objects.filter(id=request.user.id).update(
                first_name=first_name
            )

        return redirect('edit_profile')

    # POST DATA: Change Email contacts
    if request.method == 'POST' and 'new_email' in request.POST:
        new_email = request.POST.get('new_email')
        confirm_password = request.POST.get('confirm_password')

        if profile.user.check_password(confirm_password):
            # Check if email is already in use by another user
            if User.objects.filter(Q(email=new_email) & ~Q(id=request.user.id)).exists():
                messages.error(request, 'Email address already in use.')
            else:
                User.objects.filter(id=request.user.id).update(email=new_email)
        else:
            messages.error(request, 'Invalid password')

        return redirect('edit_profile')

    # POST DATA: Change Password contacts
    if request.method == 'POST' and 'new_password' in request.POST:
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')

        if profile.user.check_password(current_password):
            user = User.objects.get(id=request.user.id)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # update session
        else:
            messages.error(request, 'Invalid password.')

        return redirect('edit_profile')

    context = {
        'profile': profile,
        'empty_fields': profile.empty_fields() if profile else 0,
        'completion_percentage': int(100 - (profile.empty_fields() / 5 * 100)) if profile else 0,
        'articles': articles
    }

    return render(request, 'user_profile/edit_profile.html', context)
