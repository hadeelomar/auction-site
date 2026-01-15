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
    
    # split full name into first and last name
    name_parts = full_name.strip().split(' ', 1)
    first_name = name_parts[0] if name_parts else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''
    
    # check if user with email already exists
    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)
    
    user: User = User.objects.create_user(
        username=email,  # use email as username
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


def update_profile(request: HttpRequest) -> JsonResponse:
    """
    Update user profile information including profile image.
    Handles multipart form data for image uploads.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    user: User = request.user
    
    # get data from POST (multipart form data)
    first_name: str = request.POST.get('first_name', '')
    last_name: str = request.POST.get('last_name', '')
    email: str = request.POST.get('email', '')
    date_of_birth: str = request.POST.get('date_of_birth', '')
    
    # update user fields
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if email and email != user.email:
        # Check if email already exists
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return JsonResponse({'error': 'Email already in use'}, status=400)
        user.email = email
        user.username = email  # Update username too since we use email as username
    
    if date_of_birth:
        user.date_of_birth = date_of_birth
    
    # handle profile image upload
    if 'profile_image' in request.FILES:
        profile_image = request.FILES['profile_image']
        
        # validate file size (max 5MB)
        if profile_image.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'Image size must be less than 5MB'}, status=400)
        
        # validate file type
        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if profile_image.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid image type. Allowed: JPEG, PNG, GIF, WebP'}, status=400)
        
        # delete old profile image if exists
        if user.profile_image:
            try:
                user.profile_image.delete(save=False)
            except Exception:
                pass  # ignore errors if file doesn't exist
        
        user.profile_image = profile_image
    
    user.save()
    
    # build profile image URL
    profile_image_url = None
    if user.profile_image:
        profile_image_url = request.build_absolute_uri(user.profile_image.url)
    
    return JsonResponse({
        'message': 'Profile updated successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': str(user.date_of_birth) if user.date_of_birth else None,
            'profile_image': profile_image_url,
            'age': user.age
        }
    }, status=200)
