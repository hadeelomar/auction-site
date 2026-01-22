from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("csrf/", views.get_csrf_token, name="get_csrf_token"),
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("current-user/", views.current_user, name="current_user"),
    path("update-profile/", views.update_profile, name="update_profile"),

    # Auctions
    path("auctions/", views.auctions, name="auctions"),  # GET list / POST create
    path("auctions/search/", views.auction_search, name="auction_search"),
    path("auctions/<int:item_id>/", views.auction_detail, name="auction_detail"),
    path(
        "auctions/<int:item_id>/close/",
        views.close_auction,
        name="close_auction",
    ),

    # Watchlist
    path("watchlist/", views.watchlist, name="watchlist"),

    # Bidding
    path("bids/", views.place_bid, name="place_bid"),

    # Q&A
    path("questions/", views.questions, name="questions"),
    path(
        "questions/<int:question_id>/reply/",
        views.question_reply,
        name="question_reply",
    ),
]
