from django.http import JsonResponse, HttpRequest, HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils import timezone
from django.utils.dateparse import parse_datetime, parse_date
from django.shortcuts import render
from django.db.models import Q

import json
from typing import Dict, Any, Optional
from decimal import Decimal, InvalidOperation
from datetime import datetime, timedelta, timezone as dt_timezone

import jwt
from django.conf import settings

from api.models import User, AuctionItem, Bid, Question, Reply


# ============================================================
# JWT helpers
# ============================================================

def generate_jwt_for_user(user: User) -> str:
    """
    Generate a signed JWT for a user.
    """
    now = datetime.now(dt_timezone.utc)
    payload = {
        "user_id": user.id,
        "email": user.email,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(hours=12)).timestamp()),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    # PyJWT may return bytes on some versions; normalize to str
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def get_user_from_token(request: HttpRequest) -> Optional[User]:
    """
    Try to authenticate the user from Authorization: Bearer <token> header.
    Returns a User or None.
    """
    auth_header = request.META.get("HTTP_AUTHORIZATION", "")
    if not auth_header.startswith("Bearer "):
        return None

    token = auth_header.split(" ", 1)[1].strip()
    if not token:
        return None

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

    user_id = payload.get("user_id")
    if not user_id:
        return None

    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


# ============================================================
# CSRF helper
# ============================================================

@ensure_csrf_cookie
def get_csrf_token(request: HttpRequest) -> JsonResponse:
    """
    Endpoint to get CSRF token for subsequent requests.
    """
    return JsonResponse({"detail": "CSRF cookie set"})


# ============================================================
# AUTH: Signup / Login / Logout / Current user / Update profile
# ============================================================

@csrf_exempt
def signup(request: HttpRequest) -> JsonResponse:
    """
    User registration endpoint.
    Returns a JWT token + user info on success.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    full_name: str = data.get("full_name", "").strip()
    email: str = data.get("email", "").strip().lower()
    password: str = data.get("password", "")
    date_of_birth_raw = data.get("date_of_birth")
    date_of_birth = None

    if date_of_birth_raw:
        date_of_birth = parse_date(date_of_birth_raw)
        if not date_of_birth:
            return JsonResponse({"error": "Invalid date_of_birth format"}, status=400)

    name_parts = full_name.split(" ", 1) if full_name else []
    first_name = name_parts[0] if len(name_parts) > 0 else ""
    last_name = name_parts[1] if len(name_parts) > 1 else ""

    if not email or not password:
        return JsonResponse({"error": "Email and password are required"}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({"error": "Email already exists"}, status=400)

    try:
        user: User = User.objects.create_user(
            username=email,  # using email as username
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
        )
    except ValueError:
        return JsonResponse({"error": "Invalid date_of_birth format"}, status=400)

    # Optional: also log them into a session (browser)
    auth_login(request, user)
    request.session["username"] = email

    token = generate_jwt_for_user(user)

    return JsonResponse(
        {
            "message": "User created successfully",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_of_birth": str(user.date_of_birth) if user.date_of_birth else None,
            },
        },
        status=201,
    )


@csrf_exempt
def login(request: HttpRequest) -> JsonResponse:
    """
    User login endpoint.
    Returns a JWT token + user info on success.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    email: str = data.get("email", "")
    password: str = data.get("password", "")

    user = authenticate(request, username=email, password=password)

    if user is not None:
        auth_login(request, user)  # session cookie for browser
        request.session["username"] = email

        token = generate_jwt_for_user(user)

        return JsonResponse(
            {
                "message": "Login successful",
                "token": token,
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=200,
        )

    return JsonResponse({"error": "Invalid credentials"}, status=401)


@csrf_exempt
def logout(request: HttpRequest) -> JsonResponse:
    """
    User logout endpoint.
    For JWT, the client should just discard the token.
    This only logs out the session.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    auth_logout(request)
    request.session.flush()

    return JsonResponse({"message": "Logout successful"}, status=200)


def current_user(request: HttpRequest) -> JsonResponse:
    """
    Get current authenticated user (from session OR JWT).
    """
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    if user:
        return JsonResponse(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_of_birth": str(user.date_of_birth)
                if getattr(user, "date_of_birth", None)
                else None,
                "profile_image": (
                    request.build_absolute_uri(user.profile_image.url)
                    if getattr(user, "profile_image", None)
                    else None
                ),
                "age": getattr(user, "age", None),
                "is_authenticated": True,
            },
            status=200,
        )

    return JsonResponse({"is_authenticated": False}, status=401)


@csrf_exempt
def update_profile(request: HttpRequest) -> JsonResponse:
    """
    Update user profile information (session or JWT auth).
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    first_name = request.POST.get("first_name", "")
    last_name = request.POST.get("last_name", "")
    email = request.POST.get("email", "")
    date_of_birth = request.POST.get("date_of_birth", "")
    current_password = request.POST.get("current_password", "")
    new_password = request.POST.get("new_password", "")

    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name

    if email and email != user.email:
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            return JsonResponse({"error": "Email already in use"}, status=400)
        user.email = email
        user.username = email

    if date_of_birth:
        dob = parse_date(date_of_birth)  # expects "YYYY-MM-DD"
        if not dob:
            return JsonResponse({"error": "Invalid date_of_birth format"}, status=400)
        user.date_of_birth = dob

    if current_password and new_password:
        if not user.check_password(current_password):
            return JsonResponse({"error": "Current password is incorrect"}, status=400)
        if len(new_password) < 6:
            return JsonResponse(
                {"error": "Password must be at least 6 characters"}, status=400
            )
        user.set_password(new_password)

    if "profile_image" in request.FILES:
        image = request.FILES["profile_image"]

        if image.size > 5 * 1024 * 1024:
            return JsonResponse(
                {"error": "Image size must be less than 5MB"}, status=400
            )

        allowed_types = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/gif",
            "image/webp",
        ]
        if image.content_type not in allowed_types:
            return JsonResponse({"error": "Invalid image type"}, status=400)

        if user.profile_image:
            try:
                user.profile_image.delete(save=False)
            except Exception:
                pass

        user.profile_image = image

    user.save()

    profile_image_url = (
        request.build_absolute_uri(user.profile_image.url)
        if user.profile_image
        else None
    )

    return JsonResponse(
        {
            "message": "Profile updated successfully",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_of_birth": str(user.date_of_birth)
                if user.date_of_birth
                else None,
                "profile_image": profile_image_url,
                "age": user.age if hasattr(user, "age") else None,
            },
        },
        status=200,
    )


# ============================================================
# Auction helpers
# ============================================================

def finalize_auction_if_ended(item: AuctionItem) -> None:
    """
    If the auction has passed its ends_at time and is not yet closed,
    finalize it: set winner, final_price, closed_at.
    """
    now = timezone.now()
    if item.closed_at or not item.ends_at or item.ends_at > now:
        return

    highest_bid = item.bids.order_by("-amount", "placed_at").first()

    item.closed_at = now
    if highest_bid:
        item.winner = highest_bid.bidder
        item.final_price = highest_bid.amount
        item.current_price = highest_bid.amount
    else:
        item.winner = None
        item.final_price = None

    item.save(update_fields=["closed_at", "winner", "final_price", "current_price"])


def auction_item_to_dict(request: HttpRequest, item: AuctionItem) -> Dict[str, Any]:
    # auto-finalize if ended
    finalize_auction_if_ended(item)

    image_url = request.build_absolute_uri(item.image.url) if item.image else None

    # who is the current user?
    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    is_watching = False
    if user and user.is_authenticated:
        is_watching = item.watchers.filter(id=user.id).exists()

    winner_data = (
        {
            "id": item.winner.id,
            "email": item.winner.email,
            "first_name": item.winner.first_name,
            "last_name": item.winner.last_name,
        }
        if item.winner
        else None
    )

    return {
        "id": item.id,
        "title": item.title,
        "description": item.description,
        "starting_price": str(item.starting_price),
        "current_price": str(item.current_price),
        "image": image_url,
        "created_at": item.created_at.isoformat(),
        "ends_at": item.ends_at.isoformat() if item.ends_at else None,
        "owner": {
            "id": item.owner.id,
            "email": item.owner.email,
            "first_name": item.owner.first_name,
            "last_name": item.owner.last_name,
        },
        "status": item.status,  # uses property in models
        "is_active": item.status == "active",
        "winner": winner_data,
        "final_price": str(item.final_price) if item.final_price is not None else None,
        "closed_at": item.closed_at.isoformat() if item.closed_at else None,
        "watchers_count": item.watchers.count(),
        "is_watching": is_watching,
    }


# ============================================================
# Auctions: list / create
# ============================================================

@csrf_exempt
def auctions(request: HttpRequest) -> JsonResponse:
    """
    GET  /api/auctions -> list ACTIVE auctions
    POST /api/auctions -> create auction (auth via session or JWT)
    """
    if request.method == "GET":
        items = AuctionItem.objects.filter(closed_at__isnull=True, ends_at__gt=timezone.now()).order_by(
            "-created_at"
        )

        return JsonResponse(
            {"items": [auction_item_to_dict(request, item) for item in items]},
            status=200,
        )

    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    if not user:
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
        return JsonResponse(
            {"error": "starting_price must be greater than 0"}, status=400
        )

    ends_at = parse_datetime(ends_at_raw)
    if not ends_at:
        return JsonResponse(
            {"error": "ends_at must be valid ISO datetime"}, status=400
        )

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
        owner=user,
    )

    if "image" in request.FILES:
        image = request.FILES["image"]

        if image.size > 5 * 1024 * 1024:
            return JsonResponse({"error": "Image too large"}, status=400)

        allowed_types = [
            "image/jpeg",
            "image/jpg",
            "image/png",
            "image/gif",
            "image/webp",
        ]
        if image.content_type not in allowed_types:
            return JsonResponse({"error": "Invalid image type"}, status=400)

        item.image = image

    item.save()

    return JsonResponse(
        {
            "message": "Auction created successfully",
            "item": auction_item_to_dict(request, item),
        },
        status=201,
    )


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


# ============================================================
# Auction search & filtering
# ============================================================

@csrf_exempt
def auction_search(request: HttpRequest) -> JsonResponse:
    """
    GET /api/auctions/search?q=&min_price=&max_price=&status=active|finished|closed
    """
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    queryset = AuctionItem.objects.all()

    q_param = request.GET.get("q", "").strip()
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    status_param = request.GET.get("status")

    if q_param:
        queryset = queryset.filter(
            Q(title__icontains=q_param) | Q(description__icontains=q_param)
        )

    if min_price:
        try:
            min_price_dec = Decimal(min_price)
            queryset = queryset.filter(current_price__gte=min_price_dec)
        except (InvalidOperation, TypeError):
            return JsonResponse({"error": "Invalid min_price"}, status=400)

    if max_price:
        try:
            max_price_dec = Decimal(max_price)
            queryset = queryset.filter(current_price__lte=max_price_dec)
        except (InvalidOperation, TypeError):
            return JsonResponse({"error": "Invalid max_price"}, status=400)

    now = timezone.now()

    if status_param == "active":
        queryset = queryset.filter(closed_at__isnull=True, ends_at__gt=now)
    elif status_param == "finished":
        queryset = queryset.filter(
            Q(closed_at__isnull=False) | Q(ends_at__lte=now)
        )
    elif status_param == "closed":
        queryset = queryset.filter(closed_at__isnull=False)

    items = [
        auction_item_to_dict(request, item) for item in queryset.order_by("ends_at")
    ]

    return JsonResponse({"items": items}, status=200)


# ============================================================
# Close auction (manual)
# ============================================================

@csrf_exempt
def close_auction(request: HttpRequest, item_id: int) -> JsonResponse:
    """
    POST /api/auctions/<id>/close
    Owner-only: manually close auction and set winner/final_price.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    try:
        item = AuctionItem.objects.select_related("owner").get(id=item_id)
    except AuctionItem.DoesNotExist:
        return JsonResponse({"error": "Auction item not found"}, status=404)

    if item.owner != user:
        return JsonResponse({"error": "Only the owner can close this auction"}, status=403)

    if item.closed_at:
        return JsonResponse({"error": "Auction is already closed"}, status=400)

    # finalize (re-use helper)
    finalize_auction_if_ended(item)

    # If not ended yet, we still allow manual close right now
    if not item.closed_at:
        highest_bid = item.bids.order_by("-amount", "placed_at").first()
        now = timezone.now()
        item.closed_at = now
        if highest_bid:
            item.winner = highest_bid.bidder
            item.final_price = highest_bid.amount
            item.current_price = highest_bid.amount
        else:
            item.winner = None
            item.final_price = None
        item.save(update_fields=["closed_at", "winner", "final_price", "current_price"])

    return JsonResponse(
        {"message": "Auction closed", "item": auction_item_to_dict(request, item)},
        status=200,
    )


# ============================================================
# Watchlist (Task 11)
# ============================================================

@csrf_exempt
def watchlist(request: HttpRequest) -> JsonResponse:
    """
    GET  /api/watchlist          -> list items current user is watching
    POST /api/watchlist          -> toggle/add/remove watch status
       body: { "item_id": <id>, "action": "add"|"remove"|"toggle" }
    """
    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    if not user:
        return JsonResponse({"error": "Authentication required"}, status=401)

    if request.method == "GET":
        items = AuctionItem.objects.filter(watchers=user).select_related("owner")
        data = [auction_item_to_dict(request, item) for item in items]
        return JsonResponse({"items": data}, status=200)

    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        item_id = data.get("item_id")
        action = data.get("action", "toggle")

        if not item_id:
            return JsonResponse({"error": "item_id is required"}, status=400)

        try:
            item = AuctionItem.objects.get(id=item_id)
        except AuctionItem.DoesNotExist:
            return JsonResponse({"error": "Auction item not found"}, status=404)

        if action == "add":
            item.watchers.add(user)
        elif action == "remove":
            item.watchers.remove(user)
        elif action == "toggle":
            if item.watchers.filter(id=user.id).exists():
                item.watchers.remove(user)
            else:
                item.watchers.add(user)
        else:
            return JsonResponse({"error": "Invalid action"}, status=400)

        return JsonResponse(
            {
                "message": "Watchlist updated",
                "item": auction_item_to_dict(request, item),
            },
            status=200,
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)


# ============================================================
# Bidding
# ============================================================

@csrf_exempt
def place_bid(request: HttpRequest) -> JsonResponse:
    """
    POST /api/bids
    Place a bid on an auction item.
    Validates bid_amount > current_price and auction hasn't ended.
    Updates Item.current_price.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    if not user:
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

    # finalize if already ended
    finalize_auction_if_ended(item)
    if item.closed_at or (item.ends_at and item.ends_at <= timezone.now()):
        return JsonResponse({"error": "Auction has ended"}, status=400)

    if item.owner == user:
        return JsonResponse({"error": "Cannot bid on your own auction"}, status=400)

    if bid_amount <= item.current_price:
        return JsonResponse(
            {
                "error": f"Bid must be greater than current price (${item.current_price})"
            },
            status=400,
        )

    # Create new bid using updated field names
    bid = Bid.objects.create(
        bidder=user,  # renamed from user -> bidder
        item=item,
        amount=bid_amount,  # renamed from bid_amount -> amount
    )

    item.current_price = bid_amount
    item.save(update_fields=["current_price"])

    return JsonResponse(
        {
            "message": "Bid placed successfully",
            "bid": {
                "id": bid.id,
                "bid_amount": str(bid.amount),
                "timestamp": bid.placed_at.isoformat(),  # renamed from timestamp -> placed_at
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            "item": auction_item_to_dict(request, item),
        },
        status=201,
    )


# ============================================================
# Questions & Replies (Q&A)
# ============================================================

@csrf_exempt
def questions(request: HttpRequest) -> JsonResponse:
    """
    GET  /api/questions?item_id=X -> list questions for an item (with nested replies)
    POST /api/questions -> create a question (auth via session or JWT)
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

        questions_qs = (
            Question.objects.filter(item=item)
            .select_related("user")
            .prefetch_related("replies__user")
        )
        total = questions_qs.count()
        questions_list = questions_qs[offset : offset + per_page]

        result = []
        for q in questions_list:
            replies_data = []
            for r in q.replies.all():
                replies_data.append(
                    {
                        "id": r.id,
                        "reply_text": r.text,  # renamed from reply_text -> text
                        "timestamp": r.created_at.isoformat(),  # renamed from timestamp -> created_at
                        "user": {
                            "id": r.user.id,
                            "email": r.user.email,
                            "first_name": r.user.first_name,
                            "last_name": r.user.last_name,
                        },
                    }
                )
            result.append(
                {
                    "id": q.id,
                    "question_text": q.text,  # renamed from question_text -> text
                    "timestamp": q.created_at.isoformat(),  # renamed from timestamp -> created_at
                    "user": {
                        "id": q.user.id,
                        "email": q.user.email,
                        "first_name": q.user.first_name,
                        "last_name": q.user.last_name,
                    },
                    "replies": replies_data,
                }
            )

        return JsonResponse(
            {
                "questions": result,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": total,
                    "total_pages": (total + per_page - 1) // per_page,
                },
            },
            status=200,
        )

    elif request.method == "POST":
        user = request.user
        if not user.is_authenticated:
            user = get_user_from_token(request)

        if not user:
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
            user=user,
            item=item,
            text=question_text,  # renamed from question_text -> text
        )

        return JsonResponse(
            {
                "message": "Question created successfully",
                "question": {
                    "id": question.id,
                    "question_text": question.text,
                    "timestamp": question.created_at.isoformat(),
                    "user": {
                        "id": user.id,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                    },
                    "replies": [],
                },
            },
            status=201,
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def question_reply(request: HttpRequest, question_id: int) -> JsonResponse:
    """
    POST /api/questions/:id/reply -> add a reply to a question (auth via session or JWT)
    """
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    user = request.user
    if not user.is_authenticated:
        user = get_user_from_token(request)

    if not user:
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
        user=user,
        text=reply_text,  # renamed from reply_text -> text
    )

    return JsonResponse(
        {
            "message": "Reply created successfully",
            "reply": {
                "id": reply.id,
                "reply_text": reply.text,
                "timestamp": reply.created_at.isoformat(),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
        },
        status=201,
    )


# ============================================================
# Health & SPA
# ============================================================

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
