from django.http import HttpRequest, JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from api.models import User
import json
from typing import Dict, Any


def signup(request: HttpRequest) -> JsonResponse:
    """
    User registration endpoint.
    Validates and creates new user account.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    username: str = request.POST["username"]
    email: str = request.POST["email"]
    password: str = request.POST["password"]

    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists"}, status=400)

    # Create user
    user: User = User.objects.create_user(
        username=username, email=email, password=password
    )

    auth_login(request, user)
    request.session["username"] = username

    return JsonResponse(
        {"message": "User created successfully", "username": username}, status=201
    )


def login(request: HttpRequest) -> JsonResponse:
    """
    User login endpoint.
    Authenticates user and creates session.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    username: str = request.POST["username"]
    password: str = request.POST["password"]

    user = authenticate(request, username=username, password=password)

    if user is not None:
        auth_login(request, user)
        request.session["username"] = username

        return JsonResponse(
            {"message": "Login successful", "username": username}, status=200
        )

    return JsonResponse({"error": "Invalid credentials"}, status=401)


def logout(request: HttpRequest) -> JsonResponse:
    """
    User logout endpoint.
    Destroys session.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    auth_logout(request)
    request.session.flush()

    return JsonResponse({"message": "Logout successful"}, status=200)


def current_user(request: HttpRequest) -> JsonResponse:
    """
    Get current authenticated user details.
    """
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if "username" in request.session and request.user.is_authenticated:
        return JsonResponse(
            {
                "username": request.user.username,
                "email": request.user.email,
                "is_authenticated": True,
            },
            status=200,
        )

    return JsonResponse({"is_authenticated": False}, status=401)
