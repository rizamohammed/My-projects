from unicodedata import name
from django.urls import path
from . import views

app_name = 'polls'
urlpatterns = [
    path('createPoll/', views.createPoll, name='createPoll'),
    path('getPoll/',views.getPoll, name='fetchingPollData'),
    path('filterPoll/', views.filterByTags, name="filterPolls"),
    path('tags/', views.allTags, name="tags"),
    path('pollDetail/<int:id>/',views.pollDetail, name="pollDetail"),
    path('<int:question_id>', views.getQuest_Vote, name="QuestById"),
    path('pollDetail/<int:question_id>/vote/',views.votePoll, name="vote"),
    path('', views.home, name='home'),
    
]
