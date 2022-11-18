from rest_framework import serializers

from restaurant.models import Menu
from vote.models import UserVote


class VoteListCreateSerializer(serializers.ModelSerializer):
    """
        Serializer to View List of vote and add vote
    """
    user = serializers.SerializerMethodField('get_user')

    def get_user(self, user_vote_obj):
        return user_vote_obj.user.username

    class Meta:
        model = UserVote
        fields = ['id', 'user', 'menu', 'date_time']


class VoteResultListSerializer(serializers.ModelSerializer):
    """
        Serializer to View result of votes
    """

    restaurant = serializers.SerializerMethodField('get_restaurant')
    votes = serializers.SerializerMethodField('get_votes')

    def get_votes(self, obj):
        return self.context.get('menu__count')

    def get_restaurant(self, obj):
        return obj.restaurant.name

    class Meta:
        model = Menu
        fields = ['restaurant', 'votes']
