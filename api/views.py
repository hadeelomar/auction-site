from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.urls import reverse

from .models import AuctionItem
from .serializers import AuctionItemSerializer


class AuctionItemListView(generics.ListAPIView):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer


class AuctionItemCreateView(generics.CreateAPIView):
    queryset = AuctionItem.objects.all()
    serializer_class = AuctionItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def api_root(request):
    return Response({
        'items': request.build_absolute_uri(reverse('auctionitem-list')),
        'create': request.build_absolute_uri(reverse('auctionitem-create'))
    })
