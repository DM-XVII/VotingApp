from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import views
urlpatterns = [
    path('polls',views.PollsView.as_view()),
    path('polls/<int:pk>',views.DetailPollView.as_view()),
    path('polls/<int:pk>/statistic',views.PollStatisticView.as_view()),
    path('options/',views.OptionView.as_view()),
    path('options/<int:pk>',views.DetailOptionView.as_view()),
    path('votes/',views.VoteView.as_view()),
    path('votes/<int:pk>',views.DetailVoteView.as_view()),
    
]