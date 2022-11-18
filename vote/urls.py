from django.urls import path

from vote.views import VoteCreateView, VoteListView, VoteResultListView

urlpatterns = [
    path('current-day/', VoteCreateView.as_view(), name="Add_Vote"),
    path('current-day-votes/', VoteListView.as_view(), name="List_Vote"),
    path('current-day-result/', VoteResultListView.as_view(), name="List_Result_Vote"),
]
