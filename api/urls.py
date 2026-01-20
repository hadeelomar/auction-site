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

app_name = 'api'

urlpatterns = [
    path('auth/csrf/', views.get_csrf_token, name='csrf'),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/login/', views.login, name='login'),
    path('auth/logout/', views.logout, name='logout'),
    path('auth/user/', views.current_user, name='current-user'),
    path('profile/update/', views.update_profile, name='update-profile'),
    path("auctions/", views.auctions, name="auctions"),
    path("auctions/<int:item_id>/", views.auction_detail, name="auction-detail"),
    path("bids/", views.place_bid, name="place-bid"),
    path("questions/", views.questions, name="questions"),
    path("questions/<int:question_id>/reply/", views.question_reply, name="question-reply"),
]