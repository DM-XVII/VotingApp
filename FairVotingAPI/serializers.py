from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import Poll,Option,Vote
class PollSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id','title']

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id','value','poll','vote_count']

class DetailPollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True,read_only=True,source='option_set')
    class Meta:
        model = Poll
        fields = ['id','title','options']


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id','user','poll','vote']
        validators = [
            UniqueTogetherValidator(
                queryset=Vote.objects.all(),
                fields=['user', 'poll']
            )
        ]

class OptionCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['value','vote_count']
        
class PollStatisticSerializer(serializers.ModelSerializer):
    option_statistic = OptionCountSerializer(many=True, read_only=True, source='option_set')
    class Meta:
        model = Poll
        fields = ['title','option_statistic']
    
