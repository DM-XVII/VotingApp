from django.db.models import F
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Poll,Option,Vote
from .serializers import PollSetSerializer,OptionSerializer,DetailPollSerializer,VoteSerializer,PollStatisticSerializer
from .permissions import PollsPermission,OnlyManagerPermission,DetailPollPermission

from rest_framework.throttling import UserRateThrottle
from .throttles import ManagerThrottle

class PollsView(generics.ListCreateAPIView): #Display list of polls
    queryset = Poll.objects.all()
    serializer_class = PollSetSerializer
    permission_classes = [IsAuthenticated,PollsPermission]

    filterset_fields = ['id','title']
    search_fields = ['title']

    def get_throttles(self): 
        if self.request.user.groups.filter(name='Manager').exists():
            return [ManagerThrottle()]  
        else:
            return [UserRateThrottle()]  


class DetailPollView(generics.RetrieveUpdateDestroyAPIView): #Display certain poll and nested options
    queryset = Poll.objects.all()
    serializer_class = DetailPollSerializer
    permission_classes = [IsAuthenticated,DetailPollPermission]

    def patch(self, request, *args, **kwargs): # functionality of voting
        option_id = request.data['option']

        option = Option.objects.get(pk=option_id)
        option.vote_count = F('vote_count') + 1 #increse count of votes
        
        vote_data = {'user': request.user.id, 'poll': option.poll.id, 'vote': option.id} # create an instance of a vote
        vote_serializer = VoteSerializer(data=vote_data)
        
        if vote_serializer.is_valid():
            vote_serializer.save()
            option.save()
            return Response({"message": "Vote was created"})
        else:
            return Response({"message": vote_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_throttles(self):
        if self.request.user.is_staff:
            return [ManagerThrottle()]  
        else:
            return [UserRateThrottle()]  
      

class PollStatisticView(generics.RetrieveAPIView):
    queryset = Poll.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PollStatisticSerializer

class OptionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,OnlyManagerPermission]
    queryset = Option.objects.all()
    serializer_class = OptionSerializer
    filterset_fields = ['poll']

class DetailOptionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated,OnlyManagerPermission]
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class VoteView(generics.ListAPIView):
    permission_classes = [IsAuthenticated,OnlyManagerPermission]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    filterset_fields = ['user','poll']

class DetailVoteView(generics.RetrieveDestroyAPIView):
    permission_classes = [IsAuthenticated,OnlyManagerPermission]
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer

    def destroy(self, request, *args, **kwargs): # functionality of decreasing an amount of votes
        vote = Vote.objects.get(pk=kwargs.get('pk'))
        option = Option.objects.get(pk = vote.vote.id) 
        option.vote_count = F('vote_count') - 1

        option.save()
        vote.delete()
        return Response({"message":"vote was deleted"})


        
