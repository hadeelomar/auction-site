from django.http import JsonResponse, HttpRequest
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import ensure_csrf_cookie
from api.models import User
import json
from typing import Dict, Any


@ensure_csrf_cookie
def get_csrf_token(request: HttpRequest) -> JsonResponse:
    """
    Endpoint to get CSRF token for subsequent requests.
    """
    return JsonResponse({'detail': 'CSRF cookie set'})


def signup(request: HttpRequest) -> JsonResponse:
    """
    User registration endpoint.
    Validates and creates new user account.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    full_name: str = data.get('full_name', '')
    email: str = data.get('email', '')
    password: str = data.get('password', '')
    
    # Split full name into first and last name
    name_parts = full_name.strip().split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    # Check if user with email already exists
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)
    
    user: User = User.objects.create_user(
        username=email,  # Use email as username
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name
    )
    
    auth_login(request, user)
    request.session['username'] = email
    
    return JsonResponse({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name
        }
    }, status=201)


def login(request: HttpRequest) -> JsonResponse:
    """
    User login endpoint.
    Authenticates user and creates session.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    
    email: str = data.get('email', '')
    password: str = data.get('password', '')
    
    user = authenticate(request, username=email, password=password)
    
    if user is not None:
        auth_login(request, user)
        request.session['username'] = email
        
        return JsonResponse({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        }, status=200)
    
    return JsonResponse({'error': 'Invalid credentials'}, status=401)


def logout(request: HttpRequest) -> JsonResponse:
    """
    User logout endpoint.
    Destroys session.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    auth_logout(request)
    request.session.flush()
    
    return JsonResponse({'message': 'Logout successful'}, status=200)


def current_user(request: HttpRequest) -> JsonResponse:
    """
    Get current authenticated user details.
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if request.user.is_authenticated:
        return JsonResponse({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_authenticated': True
        }, status=200)
    
    return JsonResponse({'is_authenticated': False}, status=401)
