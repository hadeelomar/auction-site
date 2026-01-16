from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),

    path('items/', views.AuctionItemListView.as_view(), name='auctionitem-list'),
    path('items/create/', views.AuctionItemCreateView.as_view(), name='auctionitem-create'),
]
