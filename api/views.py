from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_date
from django.shortcuts import render

from api.models import User, AuctionItem, Bid

import json
from typing import Dict, Any
from decimal import Decimal, InvalidOperation


@ensure_csrf_cookie
def get_csrf_token(request: HttpRequest) -> JsonResponse:
    """
    Endpoint to get CSRF token for subsequent requests.
    """
    return JsonResponse({'detail': 'CSRF cookie set'})


@csrf_exempt
def signup(request: HttpRequest) -> JsonResponse:
    """
    User registration endpoint.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    full_name: str = data.get('full_name', '').strip()
    email: str = data.get('email', '').strip().lower()
    password: str = data.get('password', '')
    date_of_birth_raw = data.get('date_of_birth') 
    date_of_birth = None
    if date_of_birth_raw:
        date_of_birth = parse_date(date_of_birth_raw)
        if not date_of_birth:
            return JsonResponse({'error': 'Invalid date_of_birth format'}, status=400)

    name_parts = full_name.split(' ', 1) if full_name else []
    first_name = name_parts[0] if len(name_parts) > 0 else ''
    last_name = name_parts[1] if len(name_parts) > 1 else ''

    if not email or not password:
        return JsonResponse({'error': 'Email and password are required'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'Email already exists'}, status=400)

    try:
        user: User = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )
    except ValueError:
        return JsonResponse({'error': 'Invalid date_of_birth format'}, status=400)

    auth_login(request, user)
    request.session['username'] = email

    return JsonResponse({
        'message': 'User created successfully',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_of_birth': str(user.date_of_birth) if user.date_of_birth else None
        }
    }, status=201)



@csrf_exempt
def login(request: HttpRequest) -> JsonResponse:
    """
    User login endpoint.
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


@csrf_exempt
def logout(request: HttpRequest) -> JsonResponse:
    """
    User logout endpoint.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    auth_logout(request)
    request.session.flush()

    return JsonResponse({'message': 'Logout successful'}, status=200)


def current_user(request: HttpRequest) -> JsonResponse:
    """
    Get current authenticated user
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
            'date_of_birth': str(request.user.date_of_birth) if request.user.date_of_birth else None,
            'profile_image': request.build_absolute_uri(request.user.profile_image.url) if request.user.profile_image else None,
            'age': request.user.age,
            'is_authenticated': True
        }, status=200)

    return JsonResponse({'is_authenticated': False}, status=401)



def update_profile(request: HttpRequest) -> JsonResponse:
    """
    Update user profile information.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    user: User = request.user

    first_name = request.POST.get('first_name', '')
    last_name = request.POST.get('last_name', '')
    email = request.POST.get('email', '')
    date_of_birth = request.POST.get('date_of_birth', '')
    current_password = request.POST.get('current_password', '')
    new_password = request.POST.get('new_password', '')

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    if email and email != user.email:
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return JsonResponse({'error': 'Email already in use'}, status=400)
        user.email = email
        user.username = email

    if date_of_birth:
        dob = parse_date(date_of_birth)  # expects "YYYY-MM-DD"
        if not dob:
            return JsonResponse({'error': 'Invalid date_of_birth format'}, status=400)
        user.date_of_birth = dob


    if current_password and new_password:
        if not user.check_password(current_password):
            return JsonResponse({'error': 'Current password is incorrect'}, status=400)
        if len(new_password) < 6:
            return JsonResponse({'error': 'Password must be at least 6 characters'}, status=400)
        user.set_password(new_password)

    if 'profile_image' in request.FILES:
        image = request.FILES['profile_image']

        if image.size > 5 * 1024 * 1024:
            return JsonResponse({'error': 'Image size must be less than 5MB'}, status=400)

        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if image.content_type not in allowed_types:
            return JsonResponse({'error': 'Invalid image type'}, status=400)

        if user.profile_image:
            try:
                user.profile_image.delete(save=False)
            except Exception:
                pass

        user.profile_image = image

    user.save()

    profile_image_url = (
        request.build_absolute_uri(user.profile_image.url)
        if user.profile_image else None
    )

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


def auction_item_to_dict(request: HttpRequest, item: AuctionItem) -> Dict[str, Any]:
    image_url = request.build_absolute_uri(item.image.url) if item.image else None

    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "starting_price": str(item.starting_price),
        "current_price": str(item.current_price),
        "image": image_url,
        "created_at": item.created_at.isoformat(),
        "ends_at": item.ends_at.isoformat(),
        "owner": {
            "id": item.owner.id,
            "email": item.owner.email,
            "first_name": item.owner.first_name,
            "last_name": item.owner.last_name,
        },
        "is_active": item.ends_at > timezone.now(),
    }


@csrf_exempt
def auctions(request: HttpRequest) -> JsonResponse:
    """
    GET  /api/auctions -> list ACTIVE auctions
    POST /api/auctions -> create auction
    """
    if request.method == "GET":
        items = AuctionItem.objects.filter(ends_at__gt=timezone.now()).order_by(
            "-created_at"
        )

        return JsonResponse(
            {"items": [auction_item_to_dict(request, item) for item in items]},
            status=200,
        )

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    title = request.POST.get("title", "").strip()
    description = request.POST.get("description", "").strip()
    starting_price_raw = request.POST.get("starting_price", "")
    ends_at_raw = request.POST.get("ends_at", "")

    if not title:
        return JsonResponse({"error": "title is required"}, status=400)

    try:
        starting_price = Decimal(starting_price_raw)
    except (InvalidOperation, TypeError):
        return JsonResponse({"error": "Invalid starting_price"}, status=400)

    if starting_price <= 0:
        return JsonResponse({"error": "starting_price must be greater than 0"}, status=400)

    ends_at = parse_datetime(ends_at_raw)
    if not ends_at:
        return JsonResponse({"error": "ends_at must be valid ISO datetime"}, status=400)

    if timezone.is_naive(ends_at):
        ends_at = timezone.make_aware(ends_at)

    if ends_at <= timezone.now():
        return JsonResponse({"error": "ends_at must be in the future"}, status=400)

    item = AuctionItem(
        title=title,
        description=description,
        starting_price=starting_price,
        current_price=starting_price,
        ends_at=ends_at,
        owner=request.user
    )

    if "image" in request.FILES:
        image = request.FILES["image"]

        if image.size > 5 * 1024 * 1024:
            return JsonResponse({"error": "Image too large"}, status=400)

        allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
        if image.content_type not in allowed_types:
            return JsonResponse({"error": "Invalid image type"}, status=400)

        item.image = image

    item.save()

    return JsonResponse({
        "message": "Auction created successfully",
        "item": auction_item_to_dict(request, item)
    }, status=201)


def auction_detail(request: HttpRequest, item_id: int) -> JsonResponse:
    """
    GET /api/auctions/<id>
    """
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        item = AuctionItem.objects.select_related("owner").get(id=item_id)
    except AuctionItem.DoesNotExist:
        return JsonResponse({"error": "Auction item not found"}, status=404)

    return JsonResponse({"item": auction_item_to_dict(request, item)}, status=200)


@csrf_exempt
def place_bid(request: HttpRequest) -> JsonResponse:
    """
    POST /api/bids
    Place a bid on an auction item.
    Validates bid_amount > current_price and auction hasn't ended.
    Updates Item.current_price and marks previous bids as not winning.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    item_id = data.get("item_id")
    bid_amount_raw = data.get("bid_amount")

    if not item_id:
        return JsonResponse({"error": "item_id is required"}, status=400)

    if not bid_amount_raw:
        return JsonResponse({"error": "bid_amount is required"}, status=400)

    try:
        bid_amount = Decimal(str(bid_amount_raw))
    except (InvalidOperation, TypeError):
        return JsonResponse({"error": "Invalid bid_amount"}, status=400)

    try:
        item = AuctionItem.objects.select_related("owner").get(id=item_id)
    except AuctionItem.DoesNotExist:
        return JsonResponse({"error": "Auction item not found"}, status=404)

    if item.ends_at <= timezone.now():
        return JsonResponse({"error": "Auction has ended"}, status=400)

    if item.owner == request.user:
        return JsonResponse({"error": "Cannot bid on your own auction"}, status=400)

    if bid_amount <= item.current_price:
        return JsonResponse({
            "error": f"Bid must be greater than current price (${item.current_price})"
        }, status=400)

    Bid.objects.filter(item=item, is_winning=True).update(is_winning=False)

    bid = Bid.objects.create(
        user=request.user,
        item=item,
        bid_amount=bid_amount,
        is_winning=True
    )

    item.current_price = bid_amount
    item.save()

    return JsonResponse({
        "message": "Bid placed successfully",
        "bid": {
            "id": bid.id,
            "bid_amount": str(bid.bid_amount),
            "timestamp": bid.timestamp.isoformat(),
            "is_winning": bid.is_winning,
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        },
        "item": auction_item_to_dict(request, item)
    }, status=201)


def health(request: HttpRequest) -> HttpResponse:
    """
    Health endpoint
    """
    return HttpResponse("OK")

def spa(request: HttpRequest) -> HttpResponse:
    """
    Rendering build files
    """
    return render(request, "api/spa/index.html")