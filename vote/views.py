import datetime

from django.db.models import Count
from rest_framework import generics, status, filters
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response

from internal_menu_selection.common_permissions import IsAuthorizedForListModel
from internal_menu_selection.pagination import CustomPagination
from restaurant.models import Menu
from vote.models import UserVote
from vote.serializers import VoteListCreateSerializer, VoteResultListSerializer


class VoteCreateView(generics.CreateAPIView):
    """
    View to Add vote
    """
    queryset = UserVote.objects.all()
    serializer_class = VoteListCreateSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        today = datetime.datetime.now(datetime.timezone.utc).date()
        menu_obj = Menu.objects.get(id=request.data['menu'])
        if menu_obj.date_time.day != today.day:
            return Response({"message": "Please select today's menu"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            UserVote.objects.get(date_time__day=today.day, user=request.user)
            return Response({"message": "Already voted"}, status=status.HTTP_400_BAD_REQUEST)
        except UserVote.DoesNotExist:
            pass

        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VoteListView(generics.ListAPIView):
    """
    View to list current day vote
    """
    queryset = UserVote.objects.all()
    serializer_class = VoteListCreateSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username']
    ordering_fields = ['id', 'user__username', '-id', '-user__username']
    permission_classes = [IsAuthenticated, IsAuthorizedForListModel]

    def get(self, request, *args, **kwargs):
        today = datetime.datetime.now(datetime.timezone.utc).date()
        votes = UserVote.objects.filter(date_time__day=today.day).values('menu').order_by('-menu__count').annotate(
            Count('menu'))
        return Response(votes, status=status.HTTP_200_OK)


class VoteResultListView(generics.ListAPIView):
    """
    View to list current day vote result
    """
    queryset = UserVote.objects.all()
    serializer_class = VoteResultListSerializer
    permission_classes = [IsAuthenticated, IsAuthorizedForListModel]

    def get(self, request, *args, **kwargs):
        today = datetime.datetime.now(datetime.timezone.utc).date()
        user_vote_obj = UserVote.objects.filter(date_time__day=today.day).values('menu').order_by(
            '-menu__count').annotate(Count('menu')).first()

        if not user_vote_obj:
            return Response({"message": "No votes"}, status=status.HTTP_404_NOT_FOUND)

        menu_obj = Menu.objects.prefetch_related("restaurant").get(id=user_vote_obj.get('menu'))
        serializer = self.get_serializer(menu_obj, context=user_vote_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)
