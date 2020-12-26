from rest_framework import serializers
from streams.models import Stream

class StreamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Stream
        fields = [
            'name', 'username', 'user_id', 'stream_id', 'service', 'is_live',
            'start_time', 'end_time'
        ]
