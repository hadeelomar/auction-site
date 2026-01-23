"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from api import views
from api import i18n

app_name = 'api'

urlpatterns = [
    path('auth/csrf/', views.get_csrf_token, name='csrf'),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/user/', views.current_user, name='current-user'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path("auctions/", views.auctions, name="auctions"),
    path("auctions/create/", views.create_auction, name="create-auction"),
    path("auctions/create-sample/", views.create_sample_auctions, name="create-sample-auctions"),
    path("auctions/search/", views.search_auctions, name="search-auctions"),
    path("auctions/<int:item_id>/", views.auction_detail, name="auction-detail"),
    path("bids/", views.place_bid, name="place-bid"),
    path("user/bids/", views.user_bids, name="user-bids"),
    path("questions/", views.questions, name="questions"),
    path("questions/<int:question_id>/reply/", views.question_reply, name="question-reply"),
    # i18n endpoints
    path("i18n/languages/", i18n.get_supported_languages, name="languages"),
    path("i18n/currencies/", i18n.get_supported_currencies, name="currencies"),
    path("i18n/convert/", i18n.convert_currency, name="convert-currency"),
    path("i18n/language/", i18n.set_language, name="set-language"),
    path("i18n/currency/", views.set_currency, name="set-currency"),
    path("i18n/locale/", i18n.get_locale_data, name="locale-data"),
    # notification endpoints
    path("notifications/", views.notifications, name="notifications"),
    path("notifications/<int:notification_id>/mark-read/", views.mark_notification_read, name="mark-notification-read"),
    path("notifications/mark-all-read/", views.mark_all_notifications_read, name="mark-all-notifications-read"),
]