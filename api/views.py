from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.views import LogoutView
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.utils.dateparse import parse_date
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.db import models, connection
import logging
# Rate limiting is handled inline with graceful fallback

from api.models import User, AuctionItem, Bid, Question, Reply, Notification, ShareAnalytics
from api.forms import CustomAuthenticationForm, CustomUserCreationForm
from api.utils import create_and_send_notification

import json
from typing import Dict, Any
from decimal import Decimal, InvalidOperation
from django.db.models import Count, Q, F
from datetime import timedelta


@ensure_csrf_cookie
def get_csrf_token(request: HttpRequest) -> JsonResponse:
    """
    Endpoint to get CSRF token for subsequent requests.
    """
    return JsonResponse({'detail': 'CSRF cookie set'})


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



def login(request: HttpRequest) -> JsonResponse:
    """
    User login endpoint with rate limiting (5 attempts per minute).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    # Check rate limiting (fail gracefully if cache issues)
    try:
        from django_ratelimit.core import is_ratelimited
        if is_ratelimited(request, group='api_login', key='ip', rate='5/m', method='POST', increment=True):
            return JsonResponse({
                'error': 'Too many login attempts. Please wait a minute before trying again.'
            }, status=429)
    except Exception:
        pass  # Continue without rate limiting if there's an issue

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
        "category": item.category,
        "owner": {
            "id": item.owner.id,
            "email": item.owner.email,
            "first_name": item.owner.first_name,
            "last_name": item.owner.last_name,
        },
        "is_active": item.ends_at > timezone.now(),
    }


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
    GET /api/auctions/<id> - Get auction details
    PUT /api/auctions/<id> - Update auction
    DELETE /api/auctions/<id> - Delete auction
    """
    try:
        item = AuctionItem.objects.select_related("owner").get(id=item_id)
    except AuctionItem.DoesNotExist:
        return JsonResponse({"error": "Auction item not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({"item": auction_item_to_dict(request, item)}, status=200)
    
    elif request.method == "PUT":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        
        if item.owner != request.user:
            return JsonResponse({"error": "You can only edit your own auctions"}, status=403)
        
        # Check if auction has bids - if so, don't allow editing
        if item.bids.exists():
            return JsonResponse({"error": "Cannot edit auction with existing bids"}, status=400)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        starting_price = data.get('starting_price')
        end_date_str = data.get('end_date')
        category = data.get('category', '')
        
        # Validation
        if title:
            item.title = title
        if description:
            item.description = description
        if category:
            item.category = category
        if starting_price:
            try:
                starting_price_decimal = Decimal(starting_price)
                if starting_price_decimal <= 0:
                    return JsonResponse({'error': 'Starting price must be greater than 0'}, status=400)
                item.starting_price = starting_price_decimal
                item.current_price = starting_price_decimal
            except (ValueError, InvalidOperation):
                return JsonResponse({'error': 'Invalid starting price'}, status=400)
        if end_date_str:
            try:
                end_date = parse_datetime(end_date_str)
                if not end_date:
                    return JsonResponse({'error': 'Invalid end date format'}, status=400)
                now = timezone.now()
                if timezone.is_naive(end_date):
                    end_date = timezone.make_aware(end_date)
                if end_date <= now:
                    return JsonResponse({'error': 'End date must be in future'}, status=400)
                item.ends_at = end_date
            except ValueError:
                return JsonResponse({'error': 'Invalid end date format'}, status=400)
        
        item.save()
        
        return JsonResponse({
            "message": "Auction updated successfully",
            "item": auction_item_to_dict(request, item)
        }, status=200)
    
    elif request.method == "DELETE":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)
        
        if item.owner != request.user:
            return JsonResponse({"error": "You can only delete your own auctions"}, status=403)
        
        # Check if auction has bids - if so, don't allow deletion
        if item.bids.exists():
            return JsonResponse({"error": "Cannot delete auction with existing bids"}, status=400)
        
        item.delete()
        
        return JsonResponse({"message": "Auction deleted successfully"}, status=200)
    
    else:
        return JsonResponse({"error": "Method not allowed"}, status=405)


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

    # Find previous highest bidder to send outbid notification
    previous_bids = Bid.objects.filter(item=item).exclude(user=request.user).order_by('-bid_amount')
    if previous_bids.exists():
        previous_highest_bidder = previous_bids.first().user
        create_and_send_notification(
            previous_highest_bidder,
            'outbid',
            f'You have been outbid on "{item.title}". New bid: ${bid_amount:.2f}',
        )

    # Send notification to auction owner about new bid
    create_and_send_notification(
        item.owner,
        'new_bid',
        f'New bid of ${bid_amount:.2f} placed on your auction "{item.title}"',
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


def user_bids(request: HttpRequest) -> JsonResponse:
    """
    GET /api/user/bids
    Get all bids placed by the current user with auction details.
    Returns bid status (winning, outbid, won, lost) and time remaining.
    """
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    # Get all bids by the user, grouped by auction item
    user_bids_qs = Bid.objects.filter(user=request.user).select_related('item', 'item__owner').order_by('-timestamp')
    
    # Group bids by item to get the user's highest bid per item
    items_with_bids = {}
    for bid in user_bids_qs:
        item_id = bid.item.id
        if item_id not in items_with_bids:
            items_with_bids[item_id] = {
                'item': bid.item,
                'user_highest_bid': bid,
                'user_bid_amount': bid.bid_amount
            }
        elif bid.bid_amount > items_with_bids[item_id]['user_bid_amount']:
            items_with_bids[item_id]['user_highest_bid'] = bid
            items_with_bids[item_id]['user_bid_amount'] = bid.bid_amount

    bids_list = []
    now = timezone.now()

    for item_id, data in items_with_bids.items():
        item = data['item']
        user_bid = data['user_highest_bid']
        
        # Determine bid status
        auction_ended = item.ends_at <= now
        
        if auction_ended:
            # For ended auctions, check if user is the winner
            if hasattr(item, 'winner') and item.winner and item.winner.id == request.user.id:
                status = 'won'
                status_text = 'Won'
            else:
                status = 'lost'
                status_text = 'Lost'
            time_left = 'Ended'
        else:
            # For active auctions, check if user's bid is currently winning
            is_winning_bid = user_bid.is_winning
            if is_winning_bid:
                status = 'winning'
                status_text = 'Winning'
            else:
                status = 'outbid'
                status_text = 'Outbid'
            
            # Calculate time remaining
            time_diff = item.ends_at - now
            days = time_diff.days
            hours = time_diff.seconds // 3600
            if days > 0:
                time_left = f'{days}d {hours}h left'
            elif hours > 0:
                time_left = f'{hours}h left'
            else:
                minutes = time_diff.seconds // 60
                time_left = f'{minutes}m left'

        image_url = request.build_absolute_uri(item.image.url) if item.image else None

        bids_list.append({
            'id': item.id,
            'bid_id': user_bid.id,
            'title': item.title,
            'image': image_url,
            'yourBid': str(user_bid.bid_amount),
            'currentBid': str(item.current_price),
            'status': status,
            'statusText': status_text,
            'timeLeft': time_left,
            'endsAt': item.ends_at.isoformat(),
            'isActive': not auction_ended
        })

    return JsonResponse({'bids': bids_list}, status=200)


def questions(request: HttpRequest) -> JsonResponse:
    """
    GET  /api/questions?item_id=X -> list questions for an item (paginated, with nested replies)
    POST /api/questions -> create a question
    """
    if request.method == "GET":
        item_id = request.GET.get("item_id")
        if not item_id:
            return JsonResponse({"error": "item_id is required"}, status=400)

        try:
            item = AuctionItem.objects.get(id=item_id)
        except AuctionItem.DoesNotExist:
            return JsonResponse({"error": "Auction item not found"}, status=404)

        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 10))
        offset = (page - 1) * per_page

        questions_qs = Question.objects.filter(item=item).select_related("user").prefetch_related("replies__user")
        total = questions_qs.count()
        questions_list = questions_qs[offset:offset + per_page]

        result = []
        for q in questions_list:
            replies = []
            for r in q.replies.all():
                replies.append({
                    "id": r.id,
                    "reply_text": r.reply_text,
                    "timestamp": r.timestamp.isoformat(),
                    "user": {
                        "id": r.user.id,
                        "email": r.user.email,
                        "first_name": r.user.first_name,
                        "last_name": r.user.last_name,
                    }
                })
            result.append({
                "id": q.id,
                "question_text": q.question_text,
                "timestamp": q.timestamp.isoformat(),
                "user": {
                    "id": q.user.id,
                    "email": q.user.email,
                    "first_name": q.user.first_name,
                    "last_name": q.user.last_name,
                },
                "replies": replies
            })

        return JsonResponse({
            "questions": result,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": (total + per_page - 1) // per_page
            }
        }, status=200)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"error": "Authentication required"}, status=401)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        item_id = data.get("item_id")
        question_text = data.get("question_text", "").strip()

        if not item_id:
            return JsonResponse({"error": "item_id is required"}, status=400)

        if not question_text:
            return JsonResponse({"error": "question_text is required"}, status=400)

        try:
            item = AuctionItem.objects.get(id=item_id)
        except AuctionItem.DoesNotExist:
            return JsonResponse({"error": "Auction item not found"}, status=404)

        question = Question.objects.create(
            user=request.user,
            item=item,
            question_text=question_text
        )

        # Send notification to auction owner about new question
        create_and_send_notification(
            item.owner,
            'new_question',
            f'New question posted on your auction "{item.title}": "{question_text[:100]}..."',
        )

        return JsonResponse({
            "message": "Question created successfully",
            "question": {
                "id": question.id,
                "question_text": question.question_text,
                "timestamp": question.timestamp.isoformat(),
                "user": {
                    "id": request.user.id,
                    "email": request.user.email,
                    "first_name": request.user.first_name,
                    "last_name": request.user.last_name,
                },
                "replies": []
            }
        }, status=201)

    return JsonResponse({"error": "Method not allowed"}, status=405)


def question_reply(request: HttpRequest, question_id: int) -> JsonResponse:
    """
    POST /api/questions/:id/reply -> add a reply to a question
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        question = Question.objects.select_related("user", "item").get(id=question_id)
    except Question.DoesNotExist:
        return JsonResponse({"error": "Question not found"}, status=404)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    reply_text = data.get("reply_text", "").strip()

    if not reply_text:
        return JsonResponse({"error": "reply_text is required"}, status=400)

    reply = Reply.objects.create(
        question=question,
        user=request.user,
        reply_text=reply_text
    )

    # Send notification to the person who asked the question
    create_and_send_notification(
        question.user,
        'question_answered',
        f'Your question on "{question.item.title}" has been answered: "{reply_text[:100]}..."',
    )

    return JsonResponse({
        "message": "Reply created successfully",
        "reply": {
            "id": reply.id,
            "reply_text": reply.reply_text,
            "timestamp": reply.timestamp.isoformat(),
            "user": {
                "id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        }
    }, status=201)


def create_auction(request: HttpRequest) -> JsonResponse:
    """
    POST /api/auctions/create/ -> Create a new auction item
    """
    try:
        if request.method != 'POST':
            return JsonResponse({'error': 'Method not allowed'}, status=405)

        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)

        # Handle FormData (for file uploads) or JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            starting_price = request.POST.get('starting_price')
            end_date_str = request.POST.get('end_date')
            category = request.POST.get('category', 'electronics')
            image_file = request.FILES.get('image')
        else:
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON'}, status=400)

            title = data.get('title', '').strip()
            description = data.get('description', '').strip()
            starting_price = data.get('starting_price')
            end_date_str = data.get('end_date')
            category = data.get('category', 'electronics')
            image_file = None

        # Validation
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        if not description:
            return JsonResponse({'error': 'Description is required'}, status=400)
        if not starting_price:
            return JsonResponse({'error': 'Starting price is required'}, status=400)
        if not end_date_str:
            return JsonResponse({'error': 'End date is required'}, status=400)

        try:
            starting_price_decimal = Decimal(starting_price)
            if starting_price_decimal <= 0:
                return JsonResponse({'error': 'Starting price must be greater than 0'}, status=400)
        except (ValueError, InvalidOperation):
            return JsonResponse({'error': 'Invalid starting price'}, status=400)

        try:
            end_date = parse_datetime(end_date_str)
            if not end_date:
                return JsonResponse({'error': 'Invalid end date format'}, status=400)
            now = timezone.now()
            if timezone.is_naive(end_date):
                end_date = timezone.make_aware(end_date)
            if end_date <= now:
                return JsonResponse({'error': 'End date must be in future'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid end date format'}, status=400)

        # Create auction item
        auction = AuctionItem.objects.create(
            title=title,
            description=description,
            starting_price=starting_price_decimal,
            current_price=starting_price_decimal,
            ends_at=end_date,
            category=category,
            owner=request.user,
            image=image_file
        )

        return JsonResponse({
            'message': 'Auction created successfully',
            'auction': {
                'id': auction.id,
                'title': auction.title,
                'description': auction.description,
                'starting_price': float(auction.starting_price),
                'current_price': float(auction.current_price),
                'ends_at': auction.ends_at.isoformat(),
                'category': auction.category,
                'image': auction.image.url if auction.image else None,
                'owner': {
                    'id': auction.owner.id,
                    'username': auction.owner.username,
                    'first_name': auction.owner.first_name,
                    'last_name': auction.owner.last_name,
                }
            }
        }, status=201)

    except Exception as e:
        return JsonResponse({'error': f'Failed to create auction: {str(e)}'}, status=500)


def create_sample_auctions(request: HttpRequest) -> JsonResponse:
    """
    Create sample auction items for testing
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Create sample users first
        from api.models import User
        
        # Get or create sample users
        user, _ = User.objects.get_or_create(
            username='demo_seller',
            defaults={
                'email': 'demo@example.com',
                'first_name': 'Demo',
                'last_name': 'Seller'
            }
        )
        
        sample_auctions = [
            {
                'title': 'Vintage Camera',
                'description': 'Classic film camera from the 1960s. Excellent condition, fully functional. Great for photography enthusiasts and collectors.',
                'starting_price': '150.00',
                'current_price': '200.00',
                'category': 'electronics',
                'ends_at': (timezone.now() + timezone.timedelta(days=7)).isoformat(),
            },
            {
                'title': 'Designer Handbag',
                'description': 'Authentic designer handbag in excellent condition. Premium leather with gold hardware.',
                'starting_price': '250.00',
                'current_price': '300.00', 
                'category': 'fashion',
                'ends_at': (timezone.now() + timezone.timedelta(days=3)).isoformat(),
            },
            {
                'title': 'Modern Sofa',
                'description': 'Comfortable 3-seater sofa in pristine condition. Perfect for any living room.',
                'starting_price': '500.00',
                'current_price': '750.00',
                'category': 'home',
                'ends_at': (timezone.now() + timezone.timedelta(days=5)).isoformat(),
            },
            {
                'title': 'Mountain Bike',
                'description': 'High-performance mountain bike with recent servicing. Excellent trails.',
                'starting_price': '800.00',
                'current_price': '1200.00',
                'category': 'sports',
                'ends_at': (timezone.now() + timezone.timedelta(days=2)).isoformat(),
            },
            {
                'title': 'Abstract Painting',
                'description': 'Original abstract painting by emerging artist. Vibrant colors, museum quality.',
                'starting_price': '300.00',
                'current_price': '450.00',
                'category': 'art',
                'ends_at': (timezone.now() + timezone.timedelta(days=10)).isoformat(),
            },
            {
                'title': 'Classic Car',
                'description': 'Well-maintained classic car with low mileage. Reliable daily driver.',
                'starting_price': '5000.00',
                'current_price': '6500.00',
                'category': 'vehicles',
                'ends_at': (timezone.now() + timezone.timedelta(days=14)).isoformat(),
            }
        ]
        
        # Create sample auctions
        for auction_data in sample_auctions:
            auction = AuctionItem.objects.create(
                title=auction_data['title'],
                description=auction_data['description'],
                starting_price=Decimal(auction_data['starting_price']),
                current_price=Decimal(auction_data['current_price']),
                ends_at=parse_datetime(auction_data['ends_at']),
                category=auction_data['category'],
                owner=user,
            )
        
        return JsonResponse({
            'message': f'Created {len(sample_auctions)} sample auctions',
            'count': len(sample_auctions)
        }, status=201)
        
    except Exception as e:
        return JsonResponse({'error': f'Failed to create sample auctions: {str(e)}'}, status=500)
    
def health(request: HttpRequest) -> HttpResponse:
    """
    Health endpoint
    """
    return HttpResponse("OK")


def search_auctions(request: HttpRequest) -> JsonResponse:
    """
    GET /api/auctions/search?q=keyword&min_price=100&max_price=1000&status=active
    Search auctions with filters
    """
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    # Get query parameters
    query = request.GET.get('q', '').strip()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    status = request.GET.get('status', 'active')
    category = request.GET.get('category', '')
    owner = request.GET.get('owner', '')

    # Start with all auction items
    auctions = AuctionItem.objects.select_related('owner').all()

    # Filter by search query (case-insensitive search on title and description)
    if query:
        auctions = auctions.filter(
            models.Q(title__icontains=query) | 
            models.Q(description__icontains=query)
        )

    # Filter by category
    if category:
        auctions = auctions.filter(category__iexact=category)

    # Filter by owner
    if owner:
        auctions = auctions.filter(owner__username=owner)

    # Filter by price range
    if min_price:
        try:
            min_price_decimal = Decimal(min_price)
            auctions = auctions.filter(current_price__gte=min_price_decimal)
        except (ValueError, InvalidOperation):
            return JsonResponse({'error': 'Invalid min_price value'}, status=400)

    if max_price:
        try:
            max_price_decimal = Decimal(max_price)
            auctions = auctions.filter(current_price__lte=max_price_decimal)
        except (ValueError, InvalidOperation):
            return JsonResponse({'error': 'Invalid max_price value'}, status=400)

    # Filter by status
    if status == 'active':
        auctions = auctions.filter(ends_at__gt=timezone.now())
    elif status == 'ended':
        auctions = auctions.filter(ends_at__lte=timezone.now())
    elif status == 'ending_soon':
        # Ending in the next 24 hours
        auctions = auctions.filter(
            ends_at__gt=timezone.now(),
            ends_at__lte=timezone.now() + timezone.timedelta(hours=24)
        )

    # Order by relevance (for now, order by end time, then created time)
    if query:
        # If there's a search query, prioritise exact title matches
        auctions = auctions.annotate(
            title_match=models.Case(
                models.When(title__iexact=query, then=models.Value(0)),
                models.When(title__istartswith=query, then=models.Value(1)),
                default=models.Value(2),
                output_field=models.IntegerField(),
            )
        ).order_by('title_match', '-ends_at', '-created_at')
    else:
        auctions = auctions.order_by('-ends_at', '-created_at')

    # Prepare response data
    auction_data = []
    for auction in auctions:
        # Get bid count
        bid_count = auction.bids.count()
        
        # Calculate time left
        time_left = ""
        if auction.ends_at > timezone.now():
            time_delta = auction.ends_at - timezone.now()
            days = time_delta.days
            hours, remainder = divmod(time_delta.seconds, 3600)
            minutes = remainder // 60
            
            if days > 0:
                time_left = f"{days}d {hours}h"
            elif hours > 0:
                time_left = f"{hours}h {minutes}m"
            else:
                time_left = f"{minutes}m"
        else:
            time_left = "Ended"

        auction_data.append({
            'id': auction.id,
            'title': auction.title,
            'description': auction.description,
            'image': auction.image.url if auction.image else None,
            'starting_price': float(auction.starting_price),
            'current_price': float(auction.current_price),
            'bid_count': bid_count,
            'time_left': time_left,
            'ends_at': auction.ends_at.isoformat(),
            'category': auction.category,
            'owner': {
                'id': auction.owner.id,
                'username': auction.owner.username,
                'first_name': auction.owner.first_name,
                'last_name': auction.owner.last_name,
            }
        })

    return JsonResponse({
        'auctions': auction_data,
        'count': len(auction_data),
        'query': query,
        'filters': {
            'min_price': min_price,
            'max_price': max_price,
            'status': status,
            'category': category
        }
    })


# Django Auth Views
def login_view(request):
    """Django login view"""
    # Check rate limiting (fail gracefully if cache issues)
    try:
        from django_ratelimit.core import is_ratelimited
        if is_ratelimited(request, group='login', key='ip', rate='5/m', method='POST', increment=True):
            messages.error(request, 'Too many login attempts. Please wait a minute before trying again.')
            form = CustomAuthenticationForm()
            return render(request, 'auth/login.html', {'form': form})
    except Exception:
        pass  # Continue without rate limiting if there's an issue
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                # Check if this is an AJAX request
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'redirect': 'http://localhost:5173/'})
                return redirect('http://localhost:5173/')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'auth/login.html', {'form': form})

def signup_view(request):
    """Django signup view with the same styling as Vue component"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in immediately after signup
            auth_login(request, user)
            # Check if this is an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect': 'http://localhost:5173/'})
            messages.success(request, 'Account created successfully!')
            return redirect('http://localhost:5173/')
        else:
            # Handle form errors
            error_messages = []
            for field, errors in form.errors.items():
                for error in errors:
                    error_messages.append(error)
            messages.error(request, ' '.join(error_messages))
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/signup.html', {'form': form})

class CustomLogoutView(LogoutView):
    """Custom logout view"""
    next_page = 'http://localhost:5173/login'

@require_http_methods(["POST"])
def api_login(request):
    """API endpoint for login (for AJAX requests)"""
    form = CustomAuthenticationForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                }
            })
        else:
            return JsonResponse({'success': False, 'error': 'Invalid email or password'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid email or password'})

@require_http_methods(["POST"])
def api_signup(request):
    """API endpoint for signup (for AJAX requests)"""
    form = CustomUserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        auth_login(request, user)
        return JsonResponse({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })
    else:
        # Return form errors
        errors = {}
        for field, field_errors in form.errors.items():
            errors[field] = field_errors
        return JsonResponse({'success': False, 'errors': errors})


# Notification Views
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


def spa(request: HttpRequest) -> HttpResponse:
    """
    Rendering build files
    """
    return render(request, "api/spa/index.html")


logger = logging.getLogger(__name__)


@require_http_methods(["GET"])
def database_health(request: HttpRequest) -> JsonResponse:
    """
    Check database connectivity and performance.
    Returns health status for monitoring systems.
    """
    try:
        # Test basic database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result[0] != 1:
            return JsonResponse({
                "status": "unhealthy",
                "database": "connection_failed",
                "error": "Database query returned unexpected result"
            }, status=503)
        
        # Get database stats for PostgreSQL
        db_stats = {}
        if connection.vendor == 'postgresql':
            with connection.cursor() as cursor:
                # Get connection count
                cursor.execute("""
                    SELECT count(*) FROM pg_stat_activity 
                    WHERE state = 'active'
                """)
                active_connections = cursor.fetchone()[0]
                
                # Get database size
                cursor.execute("""
                    SELECT pg_size_pretty(pg_database_size(current_database()))
                """)
                db_size = cursor.fetchone()[0]
                
                db_stats = {
                    "active_connections": active_connections,
                    "database_size": db_size,
                    "vendor": "postgresql"
                }
        else:
            db_stats = {
                "vendor": connection.vendor,
                "database": "sqlite_development"
            }
        
        return JsonResponse({
            "status": "healthy",
            "database": db_stats,
            "timestamp": connection.timezone
        })
        
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        return JsonResponse({
            "status": "unhealthy",
            "database": "connection_failed",
            "error": str(e)
        }, status=503)


@require_http_methods(["GET"])
def application_health(request: HttpRequest) -> JsonResponse:
    """
    Overall application health check including database.
    """
    health_data = {
        "status": "healthy",
        "application": "auction_site",
        "version": "1.0.0",
        "checks": {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            health_data["checks"]["database"] = "healthy"
    except Exception as e:
        health_data["status"] = "unhealthy"
        health_data["checks"]["database"] = f"unhealthy: {str(e)}"
    
    # Check environment
    import os
    health_data["checks"]["environment"] = os.getenv('DJANGO_ENV', 'development')
    
    # Determine HTTP status
    status_code = 200 if health_data["status"] == "healthy" else 503
    
    return JsonResponse(health_data, status=status_code)




@csrf_exempt
def set_currency(request: HttpRequest) -> JsonResponse:
    """
    POST /api/i18n/currency/
    Set user's preferred currency
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        data = json.loads(request.body)
        currency = data.get('currency', 'USD')
        
        # Validate currency code
        valid_currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CNY', 'INR', 'KRW', 'TRY', 'RUB', 'BRL', 'MXN', 'CAD', 'AUD']
        if currency not in valid_currencies:
            return JsonResponse({'error': 'Invalid currency'}, status=400)
        
        # Update user's preferred currency
        request.user.preferred_currency = currency
        request.user.save()
        
        return JsonResponse({'currency': currency})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["GET"])
def get_notifications(request):
    """Get user's notifications with read status"""
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    try:
        notifications = Notification.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:20]  # Get latest 20
        
        notifications_data = []
        for notif in notifications:
            notifications_data.append({
                'id': notif.id,
                'type': notif.type,
                'message': notif.message,
                'timestamp': notif.timestamp.isoformat(),
                'is_read': notif.is_read
            })
        
        return JsonResponse({
            'notifications': notifications_data
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@require_http_methods(["POST"])
def track_share(request: HttpRequest) -> JsonResponse:
    """
    Track when an auction is shared on any platform
    POST /api/shares/track
    """
    try:
        data = json.loads(request.body)
        auction_id = data.get('auction_id')
        platform = data.get('platform')
        url = data.get('url')
        
        if not all([auction_id, platform, url]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)
        
        # Validate auction exists
        try:
            auction = AuctionItem.objects.get(id=auction_id)
        except AuctionItem.DoesNotExist:
            return JsonResponse({'error': 'Auction not found'}, status=404)
        
        # Get client information
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create share analytics record
        ShareAnalytics.objects.create(
            auction=auction,
            platform=platform,
            url=url,
            ip_address=ip_address,
            user_agent=user_agent
        )
        
        return JsonResponse({'message': 'Share tracked successfully'}, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def get_analytics(request: HttpRequest, auction_id: int) -> JsonResponse:
    """
    Get sharing analytics for a specific auction
    GET /api/shares/analytics/<auction_id>
    """
    try:
        # Validate auction exists
        try:
            auction = AuctionItem.objects.get(id=auction_id)
        except AuctionItem.DoesNotExist:
            return JsonResponse({'error': 'Auction not found'}, status=404)
        
        # Get total shares
        total_shares = ShareAnalytics.objects.filter(auction=auction).count()
        
        # Get shares by platform
        platform_stats = (
            ShareAnalytics.objects
            .filter(auction=auction)
            .values('platform')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Get recent shares (last 7 days)
        seven_days_ago = timezone.now() - timedelta(days=7)
        recent_shares = ShareAnalytics.objects.filter(
            auction=auction,
            timestamp__gte=seven_days_ago
        ).count()
        
        # Calculate daily average for recent shares
        daily_average = recent_shares / 7 if recent_shares > 0 else 0
        
        # Get shares over time (last 30 days by day)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        shares_over_time = []
        
        for i in range(30):
            date = thirty_days_ago + timedelta(days=i)
            next_date = date + timedelta(days=1)
            
            day_shares = ShareAnalytics.objects.filter(
                auction=auction,
                timestamp__gte=date,
                timestamp__lt=next_date
            ).count()
            
            shares_over_time.append({
                'date': date.strftime('%Y-%m-%d'),
                'shares': day_shares
            })
        
        # Calculate conversion rate (this is a placeholder - you'd need to track actual clicks)
        total_clicks = total_shares * 1.5  # Estimated 1.5 clicks per share
        conversion_rate = round((total_clicks / total_shares * 100) if total_shares > 0 else 0, 1)
        
        analytics_data = {
            'totalShares': total_shares,
            'totalClicks': total_clicks,
            'conversionRate': conversion_rate,
            'recentShares': recent_shares,
            'dailyAverage': round(daily_average, 1),
            'platformStats': list(platform_stats),
            'sharesOverTime': shares_over_time
        }
        
        return JsonResponse(analytics_data, status=200)
        
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


@require_http_methods(["GET"])
def get_global_analytics(request: HttpRequest) -> JsonResponse:
    """
    Get global sharing analytics across all auctions
    GET /api/shares/analytics
    """
    try:
        # Get total shares across all auctions
        total_shares = ShareAnalytics.objects.count()
        
        # Get platform breakdown
        platform_stats = (
            ShareAnalytics.objects
            .values('platform')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Get top shared auctions
        top_auctions = (
            ShareAnalytics.objects
            .values('auction__id', 'auction__title')
            .annotate(share_count=Count('id'))
            .order_by('-share_count')[:10]
        )
        
        # Get recent activity
        recent_shares = ShareAnalytics.objects.filter(
            timestamp__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        analytics_data = {
            'totalShares': total_shares,
            'recentShares': recent_shares,
            'platformStats': list(platform_stats),
            'topAuctions': list(top_auctions)
        }
        
        return JsonResponse(analytics_data, status=200)
        
    except Exception as e:
        return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)


def get_client_ip(request: HttpRequest) -> str:
    """
    Get the client's IP address from the request
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip