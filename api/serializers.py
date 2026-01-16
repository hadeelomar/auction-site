from rest_framework import serializers
from .models import AuctionItem

class AuctionItemSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = AuctionItem
        fields = [
            'id', 'title', 'description', 'image',
            'starting_price', 'current_price',
            'created_at', 'ends_at', 'owner'
        ]

        read_only_fields = ['id', 'current_price', 'created_at', 'owner']
