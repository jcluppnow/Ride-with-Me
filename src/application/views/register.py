"""
Contains the registration views
"""

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from rest_framework import serializers as rules

from ..forms import RegisterForm
from ..validator import Validator


def register(request):
    """
    Display register form to user, create account and log them in
    """
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        # Verifies if two passwords are the same by calling validate_password()
        # then calls set_password() to hash and save our password into the database
        if form.is_valid():
            user = form.save()
            # logs user in
            login(request, user)
            # redirects to home
            return redirect("/")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@require_http_methods(["POST"])
@login_required(login_url='/accounts/login/')
def update_user_details(request):
    """
    Update user details
    """

    validator = Validator({
        'email': rules.EmailField(required=True),
        'full_name': rules.CharField(required=True),
        'username': rules.CharField(required=True)
    }, request).validate()

    user = request.user

    for key, value in validator.validated_fields.items():
        setattr(user, key, value)

    user.save()
    return JsonResponse({'first_name': user.first_name, 'email': user.email})
