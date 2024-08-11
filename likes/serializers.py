from rest_framework import serializers
from likes.models import Like
class LikeSerializer(serializers.ModelSerializer):
    # post = serializers.StringRelatedField(many=False)
    # account = serializers.StringRelatedField(many=False)
    class Meta:
        model = Like
        fields = ['post','account']
        read_only_fields = ['account',]