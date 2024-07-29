from rest_framework import serializers
from comments.models import Comment

class CommentSerializer(serializers.ModelSerializer):
    # account = serializers.StringRelatedField(many=False)
    class Meta:
        model = Comment
        fields = ['id','post', 'account', 'body', 'created_on']
        read_only_fields = ['account',]