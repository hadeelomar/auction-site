from rest_framework import serializers
from django.utils import timezone
from .models import User, AuctionItem, Bid, Question, Reply


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
        ]


class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Reply
        fields = [
            "id",
            "text",
            "created_at",
            "user",
        ]


class QuestionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = ReplySerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "created_at",
            "user",
            "replies",
        ]


class BidSerializer(serializers.ModelSerializer):
    bidder = UserSerializer(read_only=True)

    class Meta:
        model = Bid
        fields = [
            "id",
            "amount",
            "placed_at",
            "bidder",
        ]


class AuctionItemSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    bids = BidSerializer(many=True, source="bid_set", read_only=True)
    questions = QuestionSerializer(many=True, source="question_set", read_only=True)

    class Meta:
        model = AuctionItem
        fields = [
            "id",
            "title",
            "description",
            "starting_price",
            "current_price",
            "created_at",
            "ends_at",
            "image",
            "owner",
            "bids",
            "questions",
            "is_active",
        ]
